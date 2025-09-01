"""
Stage 2 E2E Test: Audio Processing

Test complete audio processing workflow:
- Load audio file and extract correct metadata
- Resample audio to target sample rate
- Validate audio format and reject invalid files
- Audio metadata matches expected values
"""
import pytest

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.quick
]


@pytest.mark.quick
def test_audio_processing_e2e():
    """
    Test: Load audio file → Extract metadata → Validate format → Resample if needed
    
    Success Criteria:
    - Load 16kHz WAV file successfully
    - Extract correct duration, sample rate, channels
    - Resample 44.1kHz to 16kHz correctly
    - Reject invalid audio files with clear errors
    - Audio metadata matches expected values
    """
    from src.audio_to_json.audio_processor import process_audio
    from src.shared.config import load_config
    from src.shared.exceptions import AudioError
    
    config = load_config("tests/fixtures/test_config.yaml")
    
    # Test 1: Valid 16kHz audio
    audio_data = process_audio("tests/fixtures/spanish_30sec_16khz.wav", config)
    assert audio_data.sample_rate == 16000
    assert abs(audio_data.duration - 30.0) < 0.1
    assert audio_data.channels == 1
    
    # Test 2: Resample 44.1kHz audio  
    audio_data = process_audio("tests/fixtures/spanish_30sec_44khz.wav", config)
    assert audio_data.sample_rate == 16000
    
    # Test 3: Invalid file should raise AudioError
    with pytest.raises(AudioError):
        process_audio("nonexistent.wav", config)