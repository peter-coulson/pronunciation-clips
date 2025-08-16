"""
Stage 1 E2E Test: Foundation (Config + Models + Logging + Exceptions)

Test complete foundation stack working together:
- Config loads from YAML without errors
- Entity creation with validation works
- Structured logging initializes with session ID
- JSON serialization/deserialization works
- No exceptions thrown in full workflow
"""
import pytest
from pathlib import Path


def test_foundation_e2e():
    """
    Test: Load config → Create models → Initialize logging → Serialize to JSON
    
    Success Criteria:
    - Config loads from YAML without errors
    - Entity creation with validation works
    - Structured logging initializes with session ID
    - JSON serialization/deserialization works
    - No exceptions thrown in full workflow
    """
    # Will fail initially - that's expected
    from src.shared.config import load_config
    from src.shared.models import Entity, WordDatabase
    from src.shared.logging_config import init_logger
    
    # Load config
    config = load_config("tests/fixtures/test_config.yaml")
    assert config is not None
    
    # Create entities
    entity = Entity(
        entity_id="word_001",
        entity_type="word", 
        text="hola",
        start_time=1.23,
        end_time=1.67,
        duration=0.44,
        confidence=0.95,
        probability=0.89,
        syllables=["ho", "la"],
        syllable_count=2,
        phonetic="ˈoʊlə",
        quality_score=0.87,
        speaker_id="0",
        recording_id="rec_audio1_wav",
        recording_path="audio1.wav",
        processed=False,
        clip_path=None,
        selection_reason=None,
        created_at="2025-08-15T12:00:00Z"
    )
    
    # Initialize logging
    logger = init_logger(config)
    logger.info("Test message", stage="foundation", word_count=1)
    
    # Create database
    database = WordDatabase(
        metadata={"version": "1.0", "created_at": "2025-08-15T12:00:00Z", "whisper_model": "base"},
        speaker_map={"0": {"name": "Test Speaker", "gender": "Unknown", "region": "Unknown"}},
        entities=[entity]
    )
    
    # Serialize and validate
    json_output = database.model_dump_json()
    assert "entities" in json_output
    assert "speaker_map" in json_output
    assert "metadata" in json_output
    
    # Round-trip test
    database_restored = WordDatabase.model_validate_json(json_output)
    assert len(database_restored.entities) == 1
    assert database_restored.entities[0].text == "hola"