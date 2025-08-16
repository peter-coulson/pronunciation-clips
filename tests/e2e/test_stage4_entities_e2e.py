"""
Stage 4 E2E Test: Entity Creation & Quality Filtering

Test complete entity creation workflow:
- Convert Whisper words to valid Entity objects
- Generate unique entity IDs
- Apply quality filtering correctly
- Speaker assignment works
"""
import pytest


def test_entity_creation_e2e():
    """
    Test: Whisper words → Entity objects → Quality filtering → Speaker assignment
    
    Success Criteria:
    - Convert Whisper words to valid Entity objects
    - Generate unique entity_ids in format "word_001", "word_002"
    - Assign entity_type="word" to all entities
    - Calculate duration field correctly (end_time - start_time)
    - Quality filtering removes low-confidence words
    - Speaker assignment works correctly
    """
    from src.audio_to_json.entity_creation import create_entities, apply_quality_filters
    from src.shared.config import load_config
    from src.shared.models import Entity
    
    config = load_config("tests/fixtures/test_config.yaml")
    
    # Create mock transcription data
    mock_words = [
        {"text": "hola", "start": 1.0, "end": 1.5, "confidence": 0.95},
        {"text": "que", "start": 1.6, "end": 1.8, "confidence": 0.4},  # Low confidence - should be filtered
        {"text": "como", "start": 1.9, "end": 2.3, "confidence": 0.9},  # 2 syllables, good duration
        {"text": "a", "start": 2.4, "end": 2.42, "confidence": 0.8},  # Too short - should be filtered
        {"text": "extraordinariamente", "start": 3.0, "end": 7.0, "confidence": 0.8},  # Too long - should be filtered
    ]
    
    # Create entities
    entities = create_entities(mock_words, speaker_mapping=None, recording_id="test_001")
    
    # Apply quality filters
    filtered_entities = apply_quality_filters(entities, config.quality)
    
    # Validate results
    assert len(filtered_entities) == 2  # Only "hola" and "como" should remain
    
    for entity in filtered_entities:
        assert entity.entity_type == "word"
        assert entity.entity_id.startswith("word_")
        assert entity.start_time < entity.end_time
        assert entity.duration == entity.end_time - entity.start_time
        assert entity.confidence >= config.quality.min_confidence
        assert entity.duration >= config.quality.min_word_duration
        assert entity.duration <= config.quality.max_word_duration
        assert entity.speaker_id == "speaker_0"  # Default speaker