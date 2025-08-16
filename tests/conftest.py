"""
Shared pytest fixtures for all test modules
"""
import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def test_config_path():
    """Return path to test configuration file"""
    return Path("tests/fixtures/test_config.yaml")


@pytest.fixture
def test_audio_fixtures():
    """Return paths to test audio files"""
    fixtures_dir = Path("tests/fixtures")
    return {
        "spanish_30sec_16khz": fixtures_dir / "spanish_30sec_16khz.wav",
        "spanish_30sec_44khz": fixtures_dir / "spanish_30sec_44khz.wav", 
        "spanish_clear_30sec": fixtures_dir / "spanish_clear_30sec.wav",
        "spanish_noisy_30sec": fixtures_dir / "spanish_noisy_30sec.wav",
        "spanish_quiet_30sec": fixtures_dir / "spanish_quiet_30sec.wav",
        "spanish_complete_test": fixtures_dir / "spanish_complete_test.wav"
    }


@pytest.fixture
def mock_transcription_data():
    """Mock Whisper transcription output for testing"""
    return [
        {"text": "hola", "start": 1.0, "end": 1.5, "confidence": 0.95},
        {"text": "como", "start": 1.6, "end": 2.0, "confidence": 0.9},
        {"text": "estas", "start": 2.1, "end": 2.6, "confidence": 0.85},
        {"text": "muy", "start": 2.7, "end": 2.9, "confidence": 0.8},
        {"text": "bien", "start": 3.0, "end": 3.4, "confidence": 0.92}
    ]


@pytest.fixture
def expected_entity_fields():
    """Expected fields for Entity objects"""
    return [
        "entity_id", "entity_type", "text", "start_time", "end_time", "duration",
        "confidence", "probability", "syllables", "syllable_count", "phonetic",
        "quality_score", "speaker_id", "recording_id", "recording_path",
        "processed", "clip_path", "selection_reason", "created_at"
    ]