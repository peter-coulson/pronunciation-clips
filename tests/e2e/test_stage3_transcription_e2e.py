"""
Stage 3 E2E Test: Transcription Engine

Test complete transcription workflow:
- Whisper transcribes Spanish audio successfully
- Word timestamps are valid
- Confidence scores in valid range
- Word count reasonable for audio duration
"""
import pytest

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.quick
]


@pytest.mark.quick
def test_transcription_e2e():
    """
    Test: Audio data → Whisper transcription → Word timestamps
    
    Success Criteria:
    - Whisper transcribes Spanish audio successfully
    - Word timestamps are valid (start < end)
    - Confidence scores between 0.0 and 1.0
    - Word count reasonable for 30-second audio
    - Spanish language detection works
    """
    from src.audio_to_json.transcription import transcribe_audio
    from src.audio_to_json.audio_processor import process_audio
    from src.shared.config import load_config
    
    config = load_config("tests/fixtures/test_config.yaml")
    
    # Load and transcribe
    audio_data = process_audio("tests/fixtures/spanish_clear_30sec.wav", config) 
    words = transcribe_audio(audio_data, config.whisper)
    
    # Validate results
    assert len(words) > 0
    assert len(words) < 1000  # Reasonable for 30 seconds
    
    for word in words:
        assert word.start_time < word.end_time
        assert 0.0 <= word.confidence <= 1.0
        assert len(word.text.strip()) > 0
    
    # Check Spanish language processing
    spanish_words = [w.text for w in words]
    assert any(word in ["hola", "buenos", "días", "cómo", "que", "de", "la", "el"] for word in spanish_words)