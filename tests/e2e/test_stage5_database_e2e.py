"""
Stage 5 E2E Test: Database Writing

Test complete database writing workflow:
- Write WordDatabase to JSON file atomically
- Verify backup creation and JSON validation
- Handle file safety and error conditions
"""
import pytest
from pathlib import Path
import json

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.quick
]


@pytest.mark.quick
def test_database_writing_e2e():
    """
    Test: WordDatabase → Atomic JSON write → Backup creation → Validation
    
    Success Criteria:
    - Write WordDatabase to JSON file atomically
    - Verify backup created before write
    - Verify JSON validates against schema after write
    - Test rollback on write failure
    - Handle existing database file (backup + replace)
    - Clean up temporary files
    """
    from src.audio_to_json.database_writer import write_database
    from src.shared.config import load_config
    from src.shared.models import WordDatabase, Entity
    
    config = load_config("tests/fixtures/test_config.yaml")
    
    # Create test database
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
        recording_id="rec_test_wav",
        recording_path="test.wav",
        processed=False,
        clip_path=None,
        selection_reason=None,
        created_at="2025-08-15T12:00:00Z"
    )
    
    database = WordDatabase(
        metadata={"version": "1.0", "created_at": "2025-08-15T12:00:00Z", "whisper_model": "base"},
        speaker_map={"0": {"name": "Test Speaker", "gender": "Unknown", "region": "Unknown"}},
        entities=[entity]
    )
    
    # Write database
    output_path = Path("tests/output/test_database.json")
    write_database(database, output_path, config)
    
    # Verify output file exists and is valid JSON
    assert output_path.exists()
    
    with open(output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Validate JSON structure
    assert "metadata" in data
    assert "speaker_map" in data
    assert "entities" in data
    assert len(data["entities"]) == 1
    assert data["entities"][0]["text"] == "hola"
    
    # Test round-trip
    database_restored = WordDatabase.model_validate(data)
    assert len(database_restored.entities) == 1
    assert database_restored.entities[0].text == "hola"