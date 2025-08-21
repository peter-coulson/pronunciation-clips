"""
Unit tests for entity creation module.

Tests Entity creation from Word objects, quality filtering, syllable analysis,
and speaker assignment. Focuses on configuration validation and edge cases.
"""
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from src.audio_to_json.entity_creation import EntityCreator, create_entities, apply_quality_filters
from src.audio_to_json.transcription import Word
from src.shared.models import Entity
from src.shared.config import QualityConfig
from src.shared.exceptions import EntityError


class TestEntityCreator:
    """Test EntityCreator class."""
    
    def test_entity_creator_creation(self):
        """Test creating EntityCreator with config."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        assert creator.quality_config == config
        assert creator.logger is not None
    
    def test_create_entities_basic(self):
        """Test basic entity creation from words."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        words = [
            Word("hola", 0.0, 0.5, 0.9),
            Word("mundo", 0.5, 1.0, 0.8)
        ]
        
        entities = creator.create_entities(words, "test_recording", "test.wav")
        
        assert len(entities) == 2
        
        # Check first entity
        entity1 = entities[0]
        assert entity1.entity_id == "word_001"
        assert entity1.entity_type == "word"
        assert entity1.text == "hola"
        assert entity1.start_time == 0.0
        assert entity1.end_time == 0.5
        assert entity1.duration == 0.5
        assert entity1.confidence == 0.9
        assert entity1.probability == 0.9
        assert entity1.recording_id == "test_recording"
        assert entity1.recording_path == "test.wav"
        assert entity1.speaker_id == 0  # Default
        assert entity1.processed is False
        assert entity1.clip_path is None
        assert entity1.selection_reason is None
        
        # Check second entity
        entity2 = entities[1]
        assert entity2.entity_id == "word_002"
        assert entity2.text == "mundo"
        assert entity2.start_time == 0.5
        assert entity2.end_time == 1.0
        assert entity2.duration == 0.5
        assert entity2.confidence == 0.8
    
    def test_create_entities_with_speaker_mapping(self):
        """Test entity creation with speaker mapping."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        words = [
            Word("hola", 0.0, 0.5, 0.9),
            Word("mundo", 1.5, 2.0, 0.8)
        ]
        
        speaker_mapping = {
            "0.0-1.0": "0",  # Maps to speaker ID 0
            "1.0-2.5": "1"   # Maps to speaker ID 1
        }
        
        entities = creator.create_entities(words, "test", "test.wav", speaker_mapping)
        
        assert len(entities) == 2
        assert entities[0].speaker_id == 0  # Word center 0.25 falls in 0.0-1.0
        assert entities[1].speaker_id == 1  # Word center 1.75 falls in 1.0-2.5
    
    def test_create_entities_syllable_analysis(self):
        """Test syllable analysis in entity creation."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        words = [
            Word("hola", 0.0, 0.5, 0.9),
            Word("español", 0.5, 1.0, 0.8),
            Word("tal", 1.0, 1.2, 0.7)
        ]
        
        entities = creator.create_entities(words, "test", "test.wav")
        
        # Check syllable analysis
        hola_entity = entities[0]
        assert len(hola_entity.syllables) >= 1
        assert hola_entity.syllable_count == len(hola_entity.syllables)
        
        espanol_entity = entities[1]
        assert len(espanol_entity.syllables) >= 2  # español has multiple syllables
        
        tal_entity = entities[2]
        assert len(tal_entity.syllables) == 1
        assert tal_entity.syllables == ["tal"]
    
    def test_create_entities_quality_score_calculation(self):
        """Test quality score calculation."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        # Test various combinations
        words = [
            Word("test", 0.0, 0.5, 0.9),  # Good confidence, good duration
            Word("x", 0.5, 0.6, 0.3),     # Poor confidence, short duration
            Word("verylongword", 1.0, 4.0, 0.7)  # Long duration
        ]
        
        entities = creator.create_entities(words, "test", "test.wav")
        
        # Quality scores should be between 0 and 1
        for entity in entities:
            assert 0.0 <= entity.quality_score <= 1.0
        
        # Higher confidence should generally lead to higher quality
        assert entities[0].quality_score > entities[1].quality_score
    
    def test_create_entities_error_handling(self):
        """Test error handling during entity creation."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        # Create a word that will cause issues
        bad_word = MagicMock()
        bad_word.text = "test"
        bad_word.start_time = "invalid"  # String instead of float
        bad_word.end_time = 1.0
        bad_word.confidence = 0.8
        
        good_word = Word("hola", 0.0, 0.5, 0.9)
        
        words = [bad_word, good_word]
        
        # Should continue processing and create entity for good word
        entities = creator.create_entities(words, "test", "test.wav")
        assert len(entities) == 1
        assert entities[0].text == "hola"
    
    def test_create_entities_logging(self):
        """Test logging during entity creation."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        words = [Word("test", 0.0, 0.5, 0.9)]
        
        with patch.object(creator, 'log_stage_start') as mock_start, \
             patch.object(creator, 'log_stage_complete') as mock_complete:
            
            creator.create_entities(words, "test", "test.wav")
            
            mock_start.assert_called_once()
            mock_complete.assert_called_once()
    
    def test_apply_quality_filters_confidence(self):
        """Test confidence-based quality filtering."""
        config = QualityConfig()
        config.min_confidence = 0.8
        creator = EntityCreator(config)
        
        # Create test entities with different confidence levels
        # Use 2-syllable words and good duration to meet other criteria
        high_conf_entity = self._create_test_entity("hello", 0.9, 0.5, ["hel", "lo"])
        low_conf_entity = self._create_test_entity("world", 0.7, 0.5, ["wor", "ld"])
        
        entities = [high_conf_entity, low_conf_entity]
        filtered = creator.apply_quality_filters(entities)
        
        # Only high confidence entity should pass
        assert len(filtered) == 1
        assert filtered[0].text == "hello"
    
    def test_apply_quality_filters_duration(self):
        """Test duration-based quality filtering."""
        config = QualityConfig()
        config.min_word_duration = 0.3
        config.max_word_duration = 2.0
        creator = EntityCreator(config)
        
        # Create test entities with different durations
        # Use 2-syllable words and good confidence to meet other criteria
        too_short = self._create_test_entity("hello", 0.9, 0.1, ["hel", "lo"])
        good_duration = self._create_test_entity("world", 0.9, 0.5, ["wor", "ld"])
        too_long = self._create_test_entity("testing", 0.9, 3.0, ["tes", "ting"])
        
        entities = [too_short, good_duration, too_long]
        filtered = creator.apply_quality_filters(entities)
        
        # Only good duration entity should pass
        assert len(filtered) == 1
        assert filtered[0].text == "world"
    
    def test_apply_quality_filters_syllable_count(self):
        """Test syllable count-based quality filtering."""
        config = QualityConfig()
        config.syllable_range = [2, 4]
        creator = EntityCreator(config)
        
        # Create test entities with different syllable counts
        one_syllable = self._create_test_entity("a", 0.9, 0.5, ["a"])
        two_syllables = self._create_test_entity("hello", 0.9, 0.5, ["hel", "lo"])
        five_syllables = self._create_test_entity("biblioteca", 0.9, 0.5, ["bi", "bli", "o", "te", "ca"])
        
        entities = [one_syllable, two_syllables, five_syllables]
        filtered = creator.apply_quality_filters(entities)
        
        # Only two syllable entity should pass
        assert len(filtered) == 1
        assert filtered[0].text == "hello"
    
    def test_apply_quality_filters_spanish_exceptions(self):
        """Test Spanish word exceptions in syllable filtering."""
        config = QualityConfig()
        config.syllable_range = [2, 4]
        creator = EntityCreator(config)
        
        # Create entities for Spanish exception words
        tal_entity = self._create_test_entity("tal", 0.9, 0.5, ["tal"])
        que_entity = self._create_test_entity("que", 0.9, 0.5, ["que"])
        con_entity = self._create_test_entity("con", 0.9, 0.5, ["con"])
        random_short = self._create_test_entity("x", 0.9, 0.5, ["x"])
        
        entities = [tal_entity, que_entity, con_entity, random_short]
        filtered = creator.apply_quality_filters(entities)
        
        # Spanish exception words should pass, random short word should not
        assert len(filtered) == 3
        filtered_texts = [e.text for e in filtered]
        assert "tal" in filtered_texts
        assert "que" in filtered_texts
        assert "con" in filtered_texts
        assert "x" not in filtered_texts
    
    def test_apply_quality_filters_empty_text(self):
        """Test filtering of empty text entities."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        empty_text = self._create_test_entity("", 0.9, 0.5, [])
        whitespace_text = self._create_test_entity("   ", 0.9, 0.5, ["   "])
        good_text = self._create_test_entity("hello", 0.9, 0.5, ["hel", "lo"])  # 2 syllables to meet criteria
        
        entities = [empty_text, whitespace_text, good_text]
        filtered = creator.apply_quality_filters(entities)
        
        # Only good text entity should pass
        assert len(filtered) == 1
        assert filtered[0].text == "hello"
    
    def test_apply_quality_filters_logging(self):
        """Test logging during quality filtering."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        entity = self._create_test_entity("test", 0.9, 0.5, ["test"])
        
        with patch.object(creator, 'log_stage_start') as mock_start, \
             patch.object(creator, 'log_stage_complete') as mock_complete:
            
            creator.apply_quality_filters([entity])
            
            mock_start.assert_called_once()
            mock_complete.assert_called_once()
    
    def test_assign_speaker_id_no_mapping(self):
        """Test speaker ID assignment with no mapping."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        speaker_id = creator._assign_speaker_id(0.0, 1.0, None, None)
        assert speaker_id == 0
    
    def test_assign_speaker_id_with_mapping(self):
        """Test speaker ID assignment with mapping."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        mapping = {
            "0.0-2.0": "0",  # alice -> speaker 0
            "2.0-4.0": "1"   # bob -> speaker 1
        }
        
        # Test word in first range
        speaker_id1 = creator._assign_speaker_id(0.5, 1.0, None, mapping)
        assert speaker_id1 == 0
        
        # Test word in second range
        speaker_id2 = creator._assign_speaker_id(2.5, 3.0, None, mapping)
        assert speaker_id2 == 1
        
        # Test word outside ranges
        speaker_id3 = creator._assign_speaker_id(5.0, 6.0, None, mapping)
        assert speaker_id3 == 0
    
    def test_assign_speaker_id_invalid_mapping(self):
        """Test speaker ID assignment with invalid mapping format."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        invalid_mapping = {
            "invalid-format": "speaker1",
            "0.0-not_a_number": "speaker2"
        }
        
        speaker_id = creator._assign_speaker_id(0.5, 1.0, None, invalid_mapping)
        assert speaker_id == 0  # Should fallback to default
    
    def test_assign_speaker_id_with_diarization_segments(self):
        """Test speaker ID assignment with diarization segments."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        from src.shared.models import DiarizationResult, SpeakerSegment
        
        # Create diarization result with two speakers
        segments = [
            SpeakerSegment(speaker_id=0, start_time=0.0, end_time=2.0, confidence=0.9),
            SpeakerSegment(speaker_id=1, start_time=2.0, end_time=4.0, confidence=0.8),
            SpeakerSegment(speaker_id=0, start_time=4.0, end_time=6.0, confidence=0.85)
        ]
        diarization_result = DiarizationResult(
            speakers=[0, 1],
            segments=segments,
            audio_duration=6.0,
            processing_time=1.0
        )
        
        # Test word in first segment (speaker 0)
        speaker_id1 = creator._assign_speaker_id(0.5, 1.0, diarization_result, None)
        assert speaker_id1 == 0
        
        # Test word in second segment (speaker 1)
        speaker_id2 = creator._assign_speaker_id(2.5, 3.0, diarization_result, None)
        assert speaker_id2 == 1
        
        # Test word in third segment (speaker 0 again)
        speaker_id3 = creator._assign_speaker_id(4.5, 5.0, diarization_result, None)
        assert speaker_id3 == 0
        
        # Test word in gap (should find closest segment)
        speaker_id4 = creator._assign_speaker_id(6.5, 7.0, diarization_result, None)
        assert speaker_id4 == 0  # Should match the closest segment (third one)
    
    def test_assign_speaker_id_diarization_priority(self):
        """Test that diarization result takes priority over speaker mapping."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        from src.shared.models import DiarizationResult, SpeakerSegment
        
        # Create conflicting mappings
        speaker_mapping = {"0.0-2.0": "5"}  # Old mapping says speaker 5
        
        segments = [
            SpeakerSegment(speaker_id=2, start_time=0.0, end_time=2.0, confidence=0.9)
        ]
        diarization_result = DiarizationResult(
            speakers=[2],
            segments=segments,
            audio_duration=2.0,
            processing_time=1.0
        )
        
        # Should use diarization result (speaker 2), not mapping (speaker 5)
        speaker_id = creator._assign_speaker_id(1.0, 1.5, diarization_result, speaker_mapping)
        assert speaker_id == 2
    
    def test_estimate_syllables_spanish_words(self):
        """Test Spanish syllable estimation."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        test_cases = [
            ("hola", ["ho", "la"]),
            ("español", ["es", "pa", "ñol"]),
            ("tal", ["tal"]),
            ("casa", ["ca", "sa"]),
            ("", []),
            ("a", ["a"])
        ]
        
        for word, expected_pattern in test_cases:
            syllables = creator._estimate_syllables(word)
            if expected_pattern:
                # Check that we got some syllables and reasonable count
                assert len(syllables) >= 1
                # For most words, syllable count should be reasonable
                if word in ["hola", "casa"]:
                    assert len(syllables) == 2
                elif word == "tal":
                    assert syllables == ["tal"]
            else:
                assert syllables == []
    
    def test_estimate_syllables_edge_cases(self):
        """Test syllable estimation edge cases."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        # Test special characters
        syllables = creator._estimate_syllables("niño")
        assert len(syllables) >= 1
        
        # Test accented vowels
        syllables = creator._estimate_syllables("corazón")
        assert len(syllables) >= 2
        
        # Test uppercase
        syllables = creator._estimate_syllables("HOLA")
        assert len(syllables) >= 1
    
    def test_calculate_quality_score_variations(self):
        """Test quality score calculation with various inputs."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        # High confidence, good duration, good syllables
        word1 = Word("test", 0.0, 0.5, 0.9)
        score1 = creator._calculate_quality_score(word1, 0.5, ["test"])
        
        # Low confidence
        word2 = Word("test", 0.0, 0.5, 0.3)
        score2 = creator._calculate_quality_score(word2, 0.5, ["test"])
        
        # Very short duration
        word3 = Word("test", 0.0, 0.1, 0.9)
        score3 = creator._calculate_quality_score(word3, 0.1, ["test"])
        
        # Very long duration
        word4 = Word("test", 0.0, 3.0, 0.9)
        score4 = creator._calculate_quality_score(word4, 3.0, ["test"])
        
        # All scores should be in valid range
        for score in [score1, score2, score3, score4]:
            assert 0.0 <= score <= 1.0
        
        # Higher confidence should give higher score
        assert score1 > score2
        
        # Good duration should be better than extremes
        assert score1 > score3
        assert score1 > score4
    
    def _create_test_entity(self, text: str, confidence: float, 
                           duration: float, syllables: list) -> Entity:
        """Helper to create test Entity objects."""
        return Entity(
            entity_id="test_001",
            entity_type="word",
            text=text,
            start_time=0.0,
            end_time=duration,
            duration=duration,
            confidence=confidence,
            probability=confidence,
            syllables=syllables,
            syllable_count=len(syllables),
            quality_score=0.8,
            speaker_id=0,
            recording_id="test",
            recording_path="test.wav",
            processed=False,
            created_at=datetime.now().isoformat()
        )


class TestCreateEntitiesFunction:
    """Test standalone create_entities function."""
    
    def test_create_entities_function_with_words(self):
        """Test convenience function with Word objects."""
        words = [Word("hola", 0.0, 0.5, 0.9)]
        
        entities = create_entities(words, None, "test_recording", "test.wav")
        
        assert len(entities) == 1
        assert entities[0].text == "hola"
        assert entities[0].recording_id == "test_recording"
    
    def test_create_entities_function_with_dicts(self):
        """Test convenience function with dictionary input."""
        words = [
            {"text": "hola", "start": 0.0, "end": 0.5, "confidence": 0.9},
            {"text": "mundo", "start_time": 0.5, "end_time": 1.0, "probability": 0.8}
        ]
        
        entities = create_entities(words, None, "test_recording", "test.wav")
        
        assert len(entities) == 2
        assert entities[0].text == "hola"
        assert entities[0].confidence == 0.9
        assert entities[1].text == "mundo"
        assert entities[1].confidence == 0.8
    
    def test_create_entities_function_with_custom_config(self):
        """Test convenience function with custom quality config."""
        config = QualityConfig()
        config.min_confidence = 0.9
        
        words = [Word("test", 0.0, 0.5, 0.9)]
        
        entities = create_entities(words, None, "test", quality_config=config)
        
        assert len(entities) == 1
        assert entities[0].text == "test"
    
    def test_create_entities_function_default_config(self):
        """Test convenience function with default config."""
        words = [Word("test", 0.0, 0.5, 0.9)]
        
        entities = create_entities(words, None, "test")
        
        assert len(entities) == 1
        assert entities[0].text == "test"


class TestApplyQualityFiltersFunction:
    """Test standalone apply_quality_filters function."""
    
    def test_apply_quality_filters_function(self):
        """Test convenience quality filtering function."""
        config = QualityConfig()
        config.min_confidence = 0.8
        
        high_conf_entity = Entity(
            entity_id="test_001", entity_type="word", text="hello",
            start_time=0.0, end_time=0.5, duration=0.5,
            confidence=0.9, probability=0.9, syllables=["hel", "lo"],
            syllable_count=2, quality_score=0.8, speaker_id=0,
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        low_conf_entity = Entity(
            entity_id="test_002", entity_type="word", text="world",
            start_time=0.5, end_time=1.0, duration=0.5,
            confidence=0.7, probability=0.7, syllables=["wor", "ld"],
            syllable_count=2, quality_score=0.6, speaker_id=0,
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        entities = [high_conf_entity, low_conf_entity]
        filtered = apply_quality_filters(entities, config)
        
        assert len(filtered) == 1
        assert filtered[0].text == "hello"


class TestEntityCreatorEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_create_entities_empty_word_list(self):
        """Test entity creation with empty word list."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        entities = creator.create_entities([], "test", "test.wav")
        assert len(entities) == 0
    
    def test_create_entities_invalid_times(self):
        """Test handling of invalid time values."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        # Word with end_time before start_time
        bad_word = Word("test", 1.0, 0.5, 0.9)
        
        with patch.object(creator.logger, 'warning') as mock_warning:
            entities = creator.create_entities([bad_word], "test", "test.wav")
            
            # Should log warning and skip the bad word
            mock_warning.assert_called()
            assert len(entities) == 0
    
    def test_apply_quality_filters_empty_entity_list(self):
        """Test quality filtering with empty entity list."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        filtered = creator.apply_quality_filters([])
        assert len(filtered) == 0
    
    def test_create_entities_very_high_confidence(self):
        """Test handling of confidence values > 1.0."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        # Confidence > 1.0 (sometimes happens in Whisper)
        # This should be rejected by Pydantic validation
        word = Word("test", 0.0, 0.5, 1.5)
        
        with patch.object(creator.logger, 'warning') as mock_warning:
            entities = creator.create_entities([word], "test", "test.wav")
            
            # Should log warning and skip the invalid word
            mock_warning.assert_called()
            assert len(entities) == 0  # Entity creation should fail due to validation
    
    def test_create_entities_negative_confidence(self):
        """Test handling of negative confidence values."""
        config = QualityConfig()
        creator = EntityCreator(config)
        
        # Negative confidence should be rejected by Pydantic validation
        word = Word("test", 0.0, 0.5, -0.5)
        
        with patch.object(creator.logger, 'warning') as mock_warning:
            entities = creator.create_entities([word], "test", "test.wav")
            
            # Should log warning and skip the invalid word
            mock_warning.assert_called()
            assert len(entities) == 0  # Entity creation should fail due to validation
    
    def test_quality_filters_all_filters_combined(self):
        """Test quality filters with multiple criteria."""
        config = QualityConfig()
        config.min_confidence = 0.8
        config.min_word_duration = 0.3
        config.max_word_duration = 2.0
        config.syllable_range = [2, 4]
        
        creator = EntityCreator(config)
        
        # Entity that passes all filters
        good_entity = Entity(
            entity_id="good", entity_type="word", text="hello",
            start_time=0.0, end_time=0.5, duration=0.5,
            confidence=0.9, probability=0.9, syllables=["hel", "lo"],
            syllable_count=2, quality_score=0.9, speaker_id=0,
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        # Entity that fails confidence
        bad_conf_entity = Entity(
            entity_id="bad_conf", entity_type="word", text="hello",
            start_time=0.0, end_time=0.5, duration=0.5,
            confidence=0.7, probability=0.7, syllables=["hel", "lo"],
            syllable_count=2, quality_score=0.7, speaker_id=0,
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        entities = [good_entity, bad_conf_entity]
        filtered = creator.apply_quality_filters(entities)
        
        assert len(filtered) == 1
        assert filtered[0].entity_id == "good"