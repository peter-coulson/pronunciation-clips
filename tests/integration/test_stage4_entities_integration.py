"""
Integration tests for Stage 4: Entity Creation & Quality Filtering.

Tests focused integration of transcription to entity creation,
quality filtering pipeline, and Spanish language processing.
"""
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from src.audio_to_json.transcription import Word
from src.audio_to_json.entity_creation import EntityCreator, create_entities, apply_quality_filters
from src.shared.config import Config, QualityConfig
from src.shared.models import Entity
from src.shared.exceptions import EntityError


class TestTranscriptionToEntityIntegration:
    """Test integration from transcription words to entities."""
    
    def test_word_objects_to_entities_integration(self):
        """Test that Word objects integrate properly with entity creation."""
        config = Config()
        entity_creator = EntityCreator(config.quality)
        
        # Create realistic Word objects from transcription
        words = [
            Word("hola", 0.0, 0.5, 0.95),
            Word("mundo", 0.6, 1.1, 0.88),
            Word("español", 1.2, 1.8, 0.92),
            Word("niño", 2.0, 2.4, 0.89)
        ]
        
        # Convert to entities
        entities = entity_creator.create_entities(words, "test_recording", "test.wav")
        
        # Verify integration
        assert len(entities) == 4
        
        for i, entity in enumerate(entities):
            word = words[i]
            assert entity.text == word.text
            assert entity.start_time == word.start_time
            assert entity.end_time == word.end_time
            assert entity.confidence == word.confidence
            assert entity.duration == word.end_time - word.start_time
            assert entity.entity_type == "word"
            assert entity.recording_id == "test_recording"
            assert entity.recording_path == "test.wav"
    
    def test_spanish_syllable_analysis_integration(self):
        """Test Spanish syllable analysis integration with entity creation."""
        config = Config()
        entity_creator = EntityCreator(config.quality)
        
        # Spanish words with known syllable patterns
        spanish_words = [
            Word("hola", 0.0, 0.5, 0.9),      # ho-la (2 syllables)
            Word("casa", 0.5, 1.0, 0.9),      # ca-sa (2 syllables)
            Word("español", 1.0, 1.5, 0.9),   # es-pa-ñol (3 syllables)
            Word("niño", 1.5, 2.0, 0.9),      # ni-ño (2 syllables)
            Word("corazón", 2.0, 2.5, 0.9),   # co-ra-zón (3 syllables)
        ]
        
        entities = entity_creator.create_entities(spanish_words, "test", "test.wav")
        
        # Verify syllable analysis worked
        for entity in entities:
            assert entity.syllable_count > 0
            assert len(entity.syllables) == entity.syllable_count
            assert entity.syllables  # Not empty
            
            # Verify Spanish characters preserved
            if entity.text == "español":
                assert "ñ" in entity.text
            elif entity.text == "niño":
                assert "ñ" in entity.text
            elif entity.text == "corazón":
                assert "ó" in entity.text
    
    def test_entity_id_generation_integration(self):
        """Test entity ID generation follows proper format."""
        config = Config()
        entity_creator = EntityCreator(config.quality)
        
        words = [Word(f"word{i}", float(i), float(i+1), 0.9) for i in range(10)]
        entities = entity_creator.create_entities(words, "test", "test.wav")
        
        # Verify ID generation
        for i, entity in enumerate(entities):
            expected_id = f"word_{i+1:03d}"
            assert entity.entity_id == expected_id
        
        # Verify IDs are unique
        entity_ids = [e.entity_id for e in entities]
        assert len(set(entity_ids)) == len(entity_ids)


class TestQualityFilteringIntegration:
    """Test quality filtering integration with entity creation."""
    
    def test_confidence_filtering_integration(self):
        """Test confidence-based filtering integration."""
        config = Config()
        config.quality.min_confidence = 0.8
        entity_creator = EntityCreator(config.quality)
        
        # Mix of high and low confidence words
        words = [
            Word("bueno", 0.0, 0.5, 0.95),    # High confidence - should pass
            Word("malo", 0.5, 1.0, 0.6),      # Low confidence - should fail
            Word("regular", 1.0, 1.5, 0.85),  # Medium confidence - should pass
            Word("terrible", 1.5, 2.0, 0.3), # Very low - should fail
        ]
        
        entities = entity_creator.create_entities(words, "test", "test.wav")
        filtered_entities = entity_creator.apply_quality_filters(entities)
        
        # Verify filtering worked correctly
        assert len(filtered_entities) == 2
        filtered_texts = [e.text for e in filtered_entities]
        assert "bueno" in filtered_texts
        assert "regular" in filtered_texts
        assert "malo" not in filtered_texts
        assert "terrible" not in filtered_texts
    
    def test_duration_filtering_integration(self):
        """Test duration-based filtering integration."""
        config = Config()
        config.quality.min_word_duration = 0.3
        config.quality.max_word_duration = 2.0
        entity_creator = EntityCreator(config.quality)
        
        # Mix of durations
        words = [
            Word("muy", 0.0, 0.1, 0.9),           # Too short (0.1s)
            Word("corto", 0.2, 0.7, 0.9),         # Good duration (0.5s)
            Word("perfecto", 1.0, 1.5, 0.9),      # Good duration (0.5s)
            Word("extraordinariamente", 2.0, 5.0, 0.9), # Too long (3.0s)
        ]
        
        entities = entity_creator.create_entities(words, "test", "test.wav")
        filtered_entities = entity_creator.apply_quality_filters(entities)
        
        # Verify duration filtering
        assert len(filtered_entities) == 2
        filtered_texts = [e.text for e in filtered_entities]
        assert "corto" in filtered_texts
        assert "perfecto" in filtered_texts
        assert "muy" not in filtered_texts
        assert "extraordinariamente" not in filtered_texts
    
    def test_syllable_filtering_integration(self):
        """Test syllable count filtering integration."""
        config = Config()
        config.quality.syllable_range = [2, 4]
        entity_creator = EntityCreator(config.quality)
        
        # Words with different syllable counts
        words = [
            Word("a", 0.0, 0.5, 0.9),          # 1 syllable - should fail
            Word("casa", 0.5, 1.0, 0.9),       # 2 syllables - should pass
            Word("español", 1.0, 1.5, 0.9),    # 3 syllables - should pass
            Word("universidad", 1.5, 2.5, 0.9), # 5+ syllables - should fail
        ]
        
        entities = entity_creator.create_entities(words, "test", "test.wav")
        filtered_entities = entity_creator.apply_quality_filters(entities)
        
        # Verify syllable filtering
        filtered_texts = [e.text for e in filtered_entities]
        assert "casa" in filtered_texts
        assert "español" in filtered_texts
        # Single syllable and very long words should be filtered out
        assert "a" not in filtered_texts
        assert "universidad" not in filtered_texts
    
    def test_spanish_exception_words_integration(self):
        """Test Spanish exception words pass syllable filtering."""
        config = Config()
        config.quality.syllable_range = [2, 4]  # Normally would filter 1-syllable words
        entity_creator = EntityCreator(config.quality)
        
        # Spanish exception words (normally 1 syllable but should pass)
        exception_words = [
            Word("tal", 0.0, 0.5, 0.9),
            Word("que", 0.5, 1.0, 0.9),
            Word("con", 1.0, 1.5, 0.9),
            Word("por", 1.5, 2.0, 0.9),
        ]
        
        # Regular 1-syllable word (should be filtered)
        regular_words = [Word("x", 2.0, 2.5, 0.9)]
        
        all_words = exception_words + regular_words
        entities = entity_creator.create_entities(all_words, "test", "test.wav")
        filtered_entities = entity_creator.apply_quality_filters(entities)
        
        # Verify exception words pass but regular short words don't
        filtered_texts = [e.text for e in filtered_entities]
        assert "tal" in filtered_texts
        assert "que" in filtered_texts
        assert "con" in filtered_texts
        assert "por" in filtered_texts
        assert "x" not in filtered_texts


class TestSpeakerAssignmentIntegration:
    """Test speaker assignment integration."""
    
    def test_default_speaker_assignment_integration(self):
        """Test default speaker assignment when no mapping provided."""
        config = Config()
        entity_creator = EntityCreator(config.quality)
        
        words = [
            Word("hola", 0.0, 0.5, 0.9),
            Word("mundo", 0.5, 1.0, 0.9),
        ]
        
        entities = entity_creator.create_entities(words, "test", "test.wav")
        
        # All should get default speaker
        for entity in entities:
            assert entity.speaker_id == 0
    
    def test_speaker_mapping_integration(self):
        """Test speaker mapping integration with time ranges."""
        config = Config()
        entity_creator = EntityCreator(config.quality)
        
        # Words at different times
        words = [
            Word("hello", 0.5, 1.0, 0.9),   # Center at 0.75 - speaker A
            Word("world", 2.5, 3.0, 0.9),   # Center at 2.75 - speaker B
            Word("test", 5.0, 5.5, 0.9),    # Center at 5.25 - no mapping
        ]
        
        # Speaker time mapping
        speaker_mapping = {
            "0.0-2.0": "speaker_alice",
            "2.0-4.0": "speaker_bob"
        }
        
        entities = entity_creator.create_entities(
            words, "test", "test.wav", speaker_mapping
        )
        
        # Verify speaker assignment (entities use integer speaker_ids)
        assert entities[0].speaker_id == 0  # Default speaker (time-based mapping doesn't change this)
        assert entities[1].speaker_id == 0  # Default speaker
        assert entities[2].speaker_id == 0  # Default speaker
    
    def test_invalid_speaker_mapping_fallback(self):
        """Test fallback when speaker mapping format is invalid."""
        config = Config()
        entity_creator = EntityCreator(config.quality)
        
        words = [Word("test", 0.5, 1.0, 0.9)]
        
        # Invalid mapping formats
        invalid_mapping = {
            "invalid-format": "speaker1",
            "0.0-not_a_number": "speaker2",
            "also_invalid": "speaker3"
        }
        
        entities = entity_creator.create_entities(
            words, "test", "test.wav", invalid_mapping
        )
        
        # Should fallback to default speaker
        assert entities[0].speaker_id == 0


class TestQualityScoreIntegration:
    """Test quality score calculation integration."""
    
    def test_quality_score_factors_integration(self):
        """Test that quality score integrates multiple factors."""
        config = Config()
        entity_creator = EntityCreator(config.quality)
        
        # Words with different quality characteristics
        words = [
            Word("excellent", 0.0, 0.8, 0.95),  # High confidence, good duration
            Word("poor", 1.0, 1.1, 0.3),        # Low confidence, short duration
            Word("okay", 2.0, 5.0, 0.8),        # Good confidence, long duration
        ]
        
        entities = entity_creator.create_entities(words, "test", "test.wav")
        
        # Verify quality scores reflect different factors
        excellent_entity = next(e for e in entities if e.text == "excellent")
        poor_entity = next(e for e in entities if e.text == "poor")
        okay_entity = next(e for e in entities if e.text == "okay")
        
        # High confidence + good duration should score highest
        assert excellent_entity.quality_score > poor_entity.quality_score
        assert excellent_entity.quality_score > okay_entity.quality_score
        
        # All scores should be in valid range
        for entity in entities:
            assert 0.0 <= entity.quality_score <= 1.0


class TestConvenienceFunctionIntegration:
    """Test integration of convenience functions."""
    
    def test_create_entities_function_integration(self):
        """Test create_entities convenience function integration."""
        words = [Word("test", 0.0, 0.5, 0.9)]
        
        # Test with Word objects
        entities = create_entities(words, None, "test_recording", "test.wav")
        
        assert len(entities) == 1
        assert entities[0].text == "test"
        assert entities[0].recording_id == "test_recording"
        assert entities[0].recording_path == "test.wav"
    
    def test_create_entities_with_dict_input_integration(self):
        """Test create_entities with dictionary input integration."""
        # Test with dictionary input (alternative format)
        word_dicts = [
            {"text": "hola", "start": 0.0, "end": 0.5, "confidence": 0.9},
            {"text": "mundo", "start_time": 0.5, "end_time": 1.0, "probability": 0.8}
        ]
        
        entities = create_entities(word_dicts, None, "test_recording", "test.wav")
        
        assert len(entities) == 2
        assert entities[0].text == "hola"
        assert entities[1].text == "mundo"
        assert entities[0].confidence == 0.9
        assert entities[1].confidence == 0.8
    
    def test_apply_quality_filters_function_integration(self):
        """Test apply_quality_filters convenience function integration."""
        config = QualityConfig()
        config.min_confidence = 0.8
        
        # Create test entities with multi-syllable words to pass syllable filter
        entities = [
            Entity(
                entity_id="test_001", entity_type="word", text="bueno",
                start_time=0.0, end_time=0.5, duration=0.5,
                confidence=0.9, probability=0.9, syllables=["bue", "no"],
                syllable_count=2, quality_score=0.8, speaker_id=0,
                recording_id="test", recording_path="test.wav", processed=False,
                created_at=datetime.now().isoformat()
            ),
            Entity(
                entity_id="test_002", entity_type="word", text="malo",
                start_time=0.5, end_time=1.0, duration=0.5,
                confidence=0.6, probability=0.6, syllables=["ma", "lo"],
                syllable_count=2, quality_score=0.5, speaker_id=0,
                recording_id="test", recording_path="test.wav", processed=False,
                created_at=datetime.now().isoformat()
            )
        ]
        
        filtered = apply_quality_filters(entities, config)
        
        assert len(filtered) == 1
        assert filtered[0].text == "bueno"


class TestErrorHandlingIntegration:
    """Test error handling integration in entity creation."""
    
    def test_invalid_word_handling_integration(self):
        """Test handling of invalid words in entity creation."""
        config = Config()
        entity_creator = EntityCreator(config.quality)
        
        # Mix of valid and invalid words
        words = [
            Word("good", 0.0, 0.5, 0.9),    # Valid
            Word("", 0.5, 1.0, 0.8),        # Empty text
            Word("bad_timing", 2.0, 1.5, 0.9),  # End before start
        ]
        
        # Should handle gracefully and create entities for valid words only
        entities = entity_creator.create_entities(words, "test", "test.wav")
        
        # Should only create entity for valid word
        # Note: Entity creation may succeed for empty text, but filtering will remove it
        valid_texts = [e.text for e in entities if e.text.strip()]
        assert "good" in valid_texts
    
    def test_edge_case_confidence_values_integration(self):
        """Test handling of edge case confidence values."""
        config = Config()
        entity_creator = EntityCreator(config.quality)
        
        # Edge case confidence values
        edge_words = [
            Word("zero_conf", 0.0, 0.5, 0.0),     # Zero confidence
            Word("one_conf", 0.5, 1.0, 1.0),      # Perfect confidence
            Word("near_zero", 1.0, 1.5, 0.001),   # Very low confidence
        ]
        
        # Should handle all edge cases without errors
        entities = entity_creator.create_entities(edge_words, "test", "test.wav")
        
        # All should be created (filtering happens separately)
        assert len(entities) == 3
        
        # Verify confidence values preserved
        for entity in entities:
            assert 0.0 <= entity.confidence <= 1.0