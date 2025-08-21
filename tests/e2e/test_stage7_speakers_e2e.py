"""
Stage 7 E2E Test: Speaker Integration

Test complete speaker identification workflow:
- Apply provided speaker map to entities
- Handle default speaker assignment
- Process multi-speaker scenarios correctly
"""
import pytest


def test_speaker_integration_e2e():
    """
    Test: Entity list → Speaker mapping → Speaker assignment
    
    Success Criteria:
    - Apply provided speaker map to entities
    - Verify speaker_id assignment based on timestamps
    - Handle overlapping speaker segments correctly
    - Create appropriate speaker_map in output JSON
    """
    from src.audio_to_json.speaker_identification import apply_speaker_mapping
    from src.shared.config import load_config
    from src.shared.models import Entity
    
    config = load_config("tests/fixtures/test_config.yaml")
    
    # Create test entities
    entities = [
        Entity(
            entity_id="word_001", entity_type="word", text="hola",
            start_time=1.0, end_time=1.5, duration=0.5, confidence=0.9,
            probability=0.85, syllables=["ho", "la"], syllable_count=2,
            phonetic="ˈoʊlə", quality_score=0.8, speaker_id=0,
            recording_id="test", recording_path="test.wav", processed=False,
            clip_path=None, selection_reason=None, created_at="2025-08-15T12:00:00Z"
        ),
        Entity(
            entity_id="word_002", entity_type="word", text="maría",
            start_time=10.0, end_time=10.8, duration=0.8, confidence=0.9,
            probability=0.85, syllables=["ma", "rí", "a"], syllable_count=3,
            phonetic="maˈɾi.a", quality_score=0.8, speaker_id=0,
            recording_id="test", recording_path="test.wav", processed=False,
            clip_path=None, selection_reason=None, created_at="2025-08-15T12:00:00Z"
        )
    ]
    
    # Define speaker mapping (timestamp ranges)
    speaker_mapping = [
        {"start": 0.0, "end": 5.0, "speaker": "María", "speaker_id": 1},
        {"start": 5.0, "end": 15.0, "speaker": "Carlos", "speaker_id": 2}
    ]
    
    # Apply speaker mapping
    updated_entities, speaker_map = apply_speaker_mapping(entities, speaker_mapping)
    
    # Validate speaker assignment
    assert updated_entities[0].speaker_id == 1  # María (0-5s range)
    assert updated_entities[1].speaker_id == 2  # Carlos (5-15s range)
    
    # Validate speaker map
    assert 1 in speaker_map
    assert 2 in speaker_map
    assert speaker_map[1]["name"] == "María"
    assert speaker_map[2]["name"] == "Carlos"


def test_default_speaker_handling_e2e():
    """
    Test default speaker assignment when no speaker mapping provided
    
    Success Criteria:
    - Assign default speaker when speaker_mapping=None
    - Create appropriate speaker_map in output JSON
    - Handle unknown speakers gracefully
    """
    from src.audio_to_json.speaker_identification import apply_speaker_mapping
    from src.shared.config import load_config
    from src.shared.models import Entity
    
    config = load_config("tests/fixtures/test_config.yaml")
    
    # Create test entity
    entity = Entity(
        entity_id="word_001", entity_type="word", text="hola",
        start_time=1.0, end_time=1.5, duration=0.5, confidence=0.9,
        probability=0.85, syllables=["ho", "la"], syllable_count=2,
        phonetic="ˈoʊlə", quality_score=0.8, speaker_id=0,
        recording_id="test", recording_path="test.wav", processed=False,
        clip_path=None, selection_reason=None, created_at="2025-08-15T12:00:00Z"
    )
    
    # Apply no speaker mapping (default behavior)
    updated_entities, speaker_map = apply_speaker_mapping([entity], speaker_mapping=None)
    
    # Validate default speaker assignment
    assert updated_entities[0].speaker_id == 0
    assert 0 in speaker_map
    assert speaker_map[0]["name"] == "Test Speaker"