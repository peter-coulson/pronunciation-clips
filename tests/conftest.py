"""
Pytest configuration and shared fixtures for pronunciation clips testing.

Provides command-line flags for test control, diarization configuration,
and shared fixtures for all test modules.
"""
import pytest
import tempfile
import shutil
import yaml
from pathlib import Path


def pytest_addoption(parser):
    """Add custom command-line options for test control."""
    parser.addoption(
        "--disable-diarization",
        action="store_true",
        default=False,
        help="Disable diarization tests (overrides config setting)"
    )
    parser.addoption(
        "--extensive",
        action="store_true", 
        default=False,
        help="Run extensive tests with longer audio files"
    )


def pytest_configure(config):
    """Configure pytest markers and load environment."""
    # Register markers
    config.addinivalue_line("markers", "diarization: Diarization-related tests")
    config.addinivalue_line("markers", "extensive: Extensive tests with longer audio")
    
    # Load .env file at test startup if it exists
    try:
        from dotenv import load_dotenv
        env_file = Path(__file__).parent.parent / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            print(f"✅ Loaded environment variables from {env_file}")
    except ImportError:
        # dotenv not available, skip
        pass


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on command-line flags and configuration."""
    disable_diarization = config.getoption("--disable-diarization")
    extensive = config.getoption("--extensive")
    
    # Check if diarization is enabled in config
    diarization_enabled_in_config = _is_diarization_enabled_in_config()
    
    skip_diarization = pytest.mark.skip(reason="Diarization tests disabled (use --extensive or enable in config.yaml)")
    skip_extensive = pytest.mark.skip(reason="Extensive tests disabled (use --extensive flag)")
    
    for item in items:
        # Skip diarization tests if disabled via flag OR not enabled in config
        if "diarization" in item.keywords:
            if disable_diarization or not diarization_enabled_in_config:
                item.add_marker(skip_diarization)
        
        # Skip extensive tests unless explicitly requested
        if "extensive" in item.keywords and not extensive:
            item.add_marker(skip_extensive)


def _is_diarization_enabled_in_config() -> bool:
    """Check if diarization is enabled in config.yaml."""
    try:
        config_path = Path(__file__).parent.parent / "config.yaml"
        if config_path.exists():
            with open(config_path) as f:
                config = yaml.safe_load(f)
                return config.get("speakers", {}).get("enable_diarization", False)
    except Exception:
        pass
    return False


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


@pytest.fixture
def extensive_tests_enabled(request):
    """Fixture to check if extensive tests are enabled."""
    return request.config.getoption("--extensive")


@pytest.fixture  
def diarization_enabled(request):
    """Fixture to check if diarization tests are enabled."""
    disabled_by_flag = request.config.getoption("--disable-diarization")
    enabled_in_config = _is_diarization_enabled_in_config()
    return not disabled_by_flag and enabled_in_config