"""
Unit tests for transcription module.

Tests faster-whisper transcription engine, word extraction, timing validation,
and error handling. Focuses on edge cases and configuration validation.
"""
import pytest
from unittest.mock import patch, MagicMock
import numpy as np

from src.audio_to_json.transcription import TranscriptionEngine, Word, transcribe_audio
from src.audio_to_json.audio_processor import ProcessedAudio
from src.shared.config import WhisperConfig
from src.shared.models import AudioMetadata
from src.shared.exceptions import TranscriptionError

pytestmark = [
    pytest.mark.unit,
    pytest.mark.quick
]

class TestWord:
    """Test Word dataclass."""
    
    def test_word_creation(self):
        """Test creating Word objects."""
        word = Word(
            text="hola",
            start_time=1.0,
            end_time=1.5,
            confidence=0.9
        )
        
        assert word.text == "hola"
        assert word.start_time == 1.0
        assert word.end_time == 1.5
        assert word.confidence == 0.9
    
    def test_word_with_different_confidence_values(self):
        """Test Word with various confidence values."""
        confidence_values = [0.0, 0.5, 1.0, -1.0, 2.0]  # Including edge cases
        
        for conf in confidence_values:
            word = Word("test", 0.0, 1.0, conf)
            assert word.confidence == conf
    
    def test_word_with_special_characters(self):
        """Test Word with Spanish special characters."""
        spanish_words = ["niño", "español", "corazón", "María"]
        
        for text in spanish_words:
            word = Word(text, 0.0, 1.0, 0.8)
            assert word.text == text


class TestTranscriptionEngine:
    """Test TranscriptionEngine class."""
    
    def test_transcription_engine_creation(self):
        """Test creating TranscriptionEngine with config."""
        config = WhisperConfig()
        engine = TranscriptionEngine(config)
        
        assert engine.config == config
        assert engine._model is None  # Lazy loading
        assert engine.logger is not None
    
    @patch('src.audio_to_json.transcription.WhisperModel')
    def test_model_lazy_loading(self, mock_whisper_model):
        """Test lazy loading of faster-whisper model."""
        mock_model = MagicMock()
        mock_whisper_model.return_value = mock_model
        
        config = WhisperConfig()
        config.model = "base"
        engine = TranscriptionEngine(config)
        
        # Model should not be loaded yet
        assert engine._model is None
        mock_whisper_model.assert_not_called()
        
        # Access model property to trigger loading
        model = engine.model
        
        # Now model should be loaded
        mock_whisper_model.assert_called_once_with("base", device="cpu", compute_type="int8")
        assert model == mock_model
        assert engine._model == mock_model
        
        # Second access should not reload
        model2 = engine.model
        assert model2 == mock_model
        assert mock_whisper_model.call_count == 1  # Still only called once
    
    @patch('src.audio_to_json.transcription.WhisperModel')
    def test_transcribe_audio_with_word_timestamps(self, mock_whisper_model):
        """Test transcription with word-level timestamps using faster-whisper."""
        # Setup mock model and segments
        mock_model = MagicMock()
        
        # Mock word objects for faster-whisper
        mock_word1 = MagicMock()
        mock_word1.word = " hola"
        mock_word1.start = 0.0
        mock_word1.end = 0.5
        mock_word1.probability = 0.9
        
        mock_word2 = MagicMock()
        mock_word2.word = " mundo"
        mock_word2.start = 0.5
        mock_word2.end = 1.0
        mock_word2.probability = 0.8
        
        # Mock segment with words
        mock_segment = MagicMock()
        mock_segment.words = [mock_word1, mock_word2]
        
        mock_segments = [mock_segment]
        mock_info = MagicMock()
        
        mock_model.transcribe.return_value = (mock_segments, mock_info)
        mock_whisper_model.return_value = mock_model
        
        # Create test data
        config = WhisperConfig()
        engine = TranscriptionEngine(config)
        
        audio_data = np.array([0.1, 0.2, 0.3])
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        # Transcribe
        words = engine.transcribe_audio(audio)
        
        # Verify results
        assert len(words) == 2
        assert words[0].text == "hola"
        assert words[0].start_time == 0.0
        assert words[0].end_time == 0.5
        assert words[0].confidence == 0.9
        assert words[1].text == "mundo"
        assert words[1].start_time == 0.5
        assert words[1].end_time == 1.0
        assert words[1].confidence == 0.8
    
    @patch('src.audio_to_json.transcription.WhisperModel')
    def test_transcribe_audio_fallback_to_segments(self, mock_whisper_model):
        """Test transcription fallback when no word timestamps available."""
        # Setup mock model without word timestamps
        mock_model = MagicMock()
        
        mock_segment = MagicMock()
        mock_segment.text = " hola mundo"
        mock_segment.start = 0.0
        mock_segment.end = 2.0
        # No words attribute - triggers fallback
        mock_segment.words = None
        
        mock_segments = [mock_segment]
        mock_info = MagicMock()
        
        mock_model.transcribe.return_value = (mock_segments, mock_info)
        mock_whisper_model.return_value = mock_model
        
        config = WhisperConfig()
        engine = TranscriptionEngine(config)
        
        audio_data = np.array([0.1, 0.2, 0.3])
        metadata = AudioMetadata(
            path="test.wav", duration=2.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        audio = ProcessedAudio(audio_data, 16000, 2.0, metadata)
        
        words = engine.transcribe_audio(audio)
        
        # Should create words from segment text with estimated timing
        assert len(words) == 2
        assert words[0].text == "hola"
        assert words[1].text == "mundo"
        # Each word gets equal duration (2.0s / 2 words = 1.0s each)
        assert words[0].start_time == 0.0
        assert words[0].end_time == 1.0
        assert words[1].start_time == 1.0
        assert words[1].end_time == 2.0
        assert words[0].confidence == 0.8  # Default confidence
        assert words[1].confidence == 0.8
    
    @patch('src.audio_to_json.transcription.WhisperModel')
    def test_transcribe_audio_no_words_error(self, mock_whisper_model):
        """Test error when no words are extracted."""
        # Setup mock model with empty result
        mock_model = MagicMock()
        mock_segments = []  # Empty segments
        mock_info = MagicMock()
        
        mock_model.transcribe.return_value = (mock_segments, mock_info)
        mock_whisper_model.return_value = mock_model
        
        config = WhisperConfig()
        engine = TranscriptionEngine(config)
        
        audio_data = np.array([0.1, 0.2, 0.3])
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        with pytest.raises(TranscriptionError, match="No words extracted from transcription"):
            engine.transcribe_audio(audio)
    
    @patch('src.audio_to_json.transcription.WhisperModel')
    def test_transcribe_audio_filters_empty_words(self, mock_whisper_model):
        """Test that empty words are filtered out."""
        # Setup mock model with some empty words
        mock_model = MagicMock()
        
        # Mock words including empty ones
        mock_word1 = MagicMock()
        mock_word1.word = " hola"
        mock_word1.start = 0.0
        mock_word1.end = 0.5
        mock_word1.probability = 0.9
        
        mock_word2 = MagicMock()  # Empty word
        mock_word2.word = ""
        mock_word2.start = 0.5
        mock_word2.end = 0.6
        mock_word2.probability = 0.8
        
        mock_word3 = MagicMock()  # Whitespace only
        mock_word3.word = "   "
        mock_word3.start = 0.6
        mock_word3.end = 0.7
        mock_word3.probability = 0.7
        
        mock_word4 = MagicMock()
        mock_word4.word = " mundo"
        mock_word4.start = 0.7
        mock_word4.end = 1.0
        mock_word4.probability = 0.8
        
        mock_segment = MagicMock()
        mock_segment.words = [mock_word1, mock_word2, mock_word3, mock_word4]
        
        mock_segments = [mock_segment]
        mock_info = MagicMock()
        
        mock_model.transcribe.return_value = (mock_segments, mock_info)
        mock_whisper_model.return_value = mock_model
        
        config = WhisperConfig()
        engine = TranscriptionEngine(config)
        
        audio_data = np.array([0.1, 0.2, 0.3])
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        words = engine.transcribe_audio(audio)
        
        # Should only have non-empty words
        assert len(words) == 2
        assert words[0].text == "hola"
        assert words[1].text == "mundo"
    
    @patch('src.audio_to_json.transcription.WhisperModel')
    def test_transcribe_audio_with_configuration_options(self, mock_whisper_model):
        """Test that configuration options are passed to faster-whisper."""
        mock_model = MagicMock()
        
        mock_word = MagicMock()
        mock_word.word = " test"
        mock_word.start = 0.0
        mock_word.end = 1.0
        mock_word.probability = 0.9
        
        mock_segment = MagicMock()
        mock_segment.words = [mock_word]
        
        mock_segments = [mock_segment]
        mock_info = MagicMock()
        
        mock_model.transcribe.return_value = (mock_segments, mock_info)
        mock_whisper_model.return_value = mock_model
        
        config = WhisperConfig()
        config.language = "es"
        config.temperature = 0.5
        config.word_timestamps = True
        engine = TranscriptionEngine(config)
        
        audio_data = np.array([0.1, 0.2, 0.3])
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        engine.transcribe_audio(audio)
        
        # Verify transcribe was called with correct options
        mock_model.transcribe.assert_called_once()
        call_args = mock_model.transcribe.call_args
        
        # Check audio data (first argument)
        assert np.array_equal(call_args[0][0], audio_data)
        
        # Check options (keyword arguments)
        options = call_args[1]
        assert options["language"] == "es"
        assert options["temperature"] == 0.5
        assert options["word_timestamps"] is True
        assert options["condition_on_previous_text"] is False
    
    @patch('src.audio_to_json.transcription.WhisperModel')
    def test_transcribe_audio_whisper_error(self, mock_whisper_model):
        """Test handling of faster-whisper transcription errors."""
        mock_model = MagicMock()
        mock_model.transcribe.side_effect = Exception("Whisper model error")
        mock_whisper_model.return_value = mock_model
        
        config = WhisperConfig()
        engine = TranscriptionEngine(config)
        
        audio_data = np.array([0.1, 0.2, 0.3])
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        with pytest.raises(TranscriptionError, match="Transcription failed"):
            engine.transcribe_audio(audio)
    
    @patch('src.audio_to_json.transcription.WhisperModel')
    def test_transcribe_audio_logging(self, mock_whisper_model):
        """Test transcription logging functionality."""
        mock_model = MagicMock()
        
        mock_word = MagicMock()
        mock_word.word = " test"
        mock_word.start = 0.0
        mock_word.end = 1.0
        mock_word.probability = 0.9
        
        mock_segment = MagicMock()
        mock_segment.words = [mock_word]
        
        mock_segments = [mock_segment]
        mock_info = MagicMock()
        
        mock_model.transcribe.return_value = (mock_segments, mock_info)
        mock_whisper_model.return_value = mock_model
        
        config = WhisperConfig()
        engine = TranscriptionEngine(config)
        
        audio_data = np.array([0.1, 0.2, 0.3])
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        # Mock logging methods
        with patch.object(engine, 'log_stage_start') as mock_start, \
             patch.object(engine, 'log_progress') as mock_progress, \
             patch.object(engine, 'log_stage_complete') as mock_complete:
            
            engine.transcribe_audio(audio)
            
            # Verify logging calls
            mock_start.assert_called_once()
            assert mock_progress.call_count >= 1
            mock_complete.assert_called_once()
    
    @patch('src.audio_to_json.transcription.WhisperModel')
    def test_transcribe_audio_error_logging(self, mock_whisper_model):
        """Test error logging during transcription."""
        mock_model = MagicMock()
        mock_model.transcribe.side_effect = Exception("Test error")
        mock_whisper_model.return_value = mock_model
        
        config = WhisperConfig()
        engine = TranscriptionEngine(config)
        
        audio_data = np.array([0.1, 0.2, 0.3])
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        with patch.object(engine.logger, 'error') as mock_error:
            with pytest.raises(TranscriptionError):
                engine.transcribe_audio(audio)
            
            # Verify error logging
            mock_error.assert_called_once()


class TestTranscribeAudioFunction:
    """Test standalone transcribe_audio function."""
    
    @patch('src.audio_to_json.transcription.TranscriptionEngine')
    def test_transcribe_audio_function(self, mock_engine_class):
        """Test the convenience transcribe_audio function."""
        # Setup mocks
        mock_engine = MagicMock()
        mock_words = [Word("test", 0.0, 1.0, 0.9)]
        mock_engine.transcribe_audio.return_value = mock_words
        mock_engine_class.return_value = mock_engine
        
        config = WhisperConfig()
        audio_data = np.array([0.1, 0.2, 0.3])
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        result = transcribe_audio(audio, config)
        
        # Verify function calls
        mock_engine_class.assert_called_once_with(config)
        mock_engine.transcribe_audio.assert_called_once_with(audio)
        assert result == mock_words
    
    @patch('src.audio_to_json.transcription.TranscriptionEngine')
    def test_transcribe_audio_function_error_propagation(self, mock_engine_class):
        """Test that the function properly propagates errors."""
        # Setup mocks
        mock_engine = MagicMock()
        mock_engine.transcribe_audio.side_effect = TranscriptionError("Test error")
        mock_engine_class.return_value = mock_engine
        
        config = WhisperConfig()
        audio_data = np.array([0.1, 0.2, 0.3])
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        with pytest.raises(TranscriptionError, match="Test error"):
            transcribe_audio(audio, config)


class TestTranscriptionEngineEdgeCases:
    """Test edge cases and boundary conditions."""
    
    @patch('src.audio_to_json.transcription.WhisperModel')
    def test_transcribe_very_short_audio(self, mock_whisper_model):
        """Test transcribing very short audio."""
        mock_model = MagicMock()
        
        mock_word = MagicMock()
        mock_word.word = " a"
        mock_word.start = 0.0
        mock_word.end = 0.1
        mock_word.probability = 0.7
        
        mock_segment = MagicMock()
        mock_segment.words = [mock_word]
        
        mock_segments = [mock_segment]
        mock_info = MagicMock()
        
        mock_model.transcribe.return_value = (mock_segments, mock_info)
        mock_whisper_model.return_value = mock_model
        
        config = WhisperConfig()
        engine = TranscriptionEngine(config)
        
        # Very short audio (single sample)
        audio_data = np.array([0.1])
        metadata = AudioMetadata(
            path="short.wav", duration=0.1, sample_rate=16000,
            channels=1, format="wav", size_bytes=100
        )
        audio = ProcessedAudio(audio_data, 16000, 0.1, metadata)
        
        words = engine.transcribe_audio(audio)
        assert len(words) == 1
        assert words[0].text == "a"
    
    @patch('src.audio_to_json.transcription.WhisperModel')
    def test_transcribe_empty_segments(self, mock_whisper_model):
        """Test handling of empty segments."""
        mock_model = MagicMock()
        
        mock_segment = MagicMock()
        mock_segment.text = ""
        mock_segment.start = 0.0
        mock_segment.end = 1.0
        mock_segment.words = None
        
        mock_segments = [mock_segment]
        mock_info = MagicMock()
        
        mock_model.transcribe.return_value = (mock_segments, mock_info)
        mock_whisper_model.return_value = mock_model
        
        config = WhisperConfig()
        engine = TranscriptionEngine(config)
        
        audio_data = np.array([0.1, 0.2, 0.3])
        metadata = AudioMetadata(
            path="empty.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        with pytest.raises(TranscriptionError, match="No words extracted from transcription"):
            engine.transcribe_audio(audio)
    
    @patch('src.audio_to_json.transcription.WhisperModel')
    def test_transcribe_multiple_segments(self, mock_whisper_model):
        """Test transcription with multiple segments."""
        mock_model = MagicMock()
        
        # First segment
        mock_word1 = MagicMock()
        mock_word1.word = " hola"
        mock_word1.start = 0.0
        mock_word1.end = 0.5
        mock_word1.probability = 0.9
        
        mock_segment1 = MagicMock()
        mock_segment1.words = [mock_word1]
        
        # Second segment
        mock_word2 = MagicMock()
        mock_word2.word = " mundo"
        mock_word2.start = 1.0
        mock_word2.end = 1.5
        mock_word2.probability = 0.8
        
        mock_segment2 = MagicMock()
        mock_segment2.words = [mock_word2]
        
        mock_segments = [mock_segment1, mock_segment2]
        mock_info = MagicMock()
        
        mock_model.transcribe.return_value = (mock_segments, mock_info)
        mock_whisper_model.return_value = mock_model
        
        config = WhisperConfig()
        engine = TranscriptionEngine(config)
        
        audio_data = np.array([0.1, 0.2, 0.3, 0.4])
        metadata = AudioMetadata(
            path="multi.wav", duration=2.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=2000
        )
        audio = ProcessedAudio(audio_data, 16000, 2.0, metadata)
        
        words = engine.transcribe_audio(audio)
        
        # Should combine words from all segments
        assert len(words) == 2
        assert words[0].text == "hola"
        assert words[1].text == "mundo"
    
    def test_different_whisper_configs(self):
        """Test TranscriptionEngine with various configurations."""
        configs = [
            {"model": "tiny", "language": "en", "temperature": 0.0},
            {"model": "base", "language": "es", "temperature": 0.5},
            {"model": "small", "language": "fr", "temperature": 1.0},
        ]
        
        for config_data in configs:
            config = WhisperConfig()
            config.model = config_data["model"]
            config.language = config_data["language"]
            config.temperature = config_data["temperature"]
            
            engine = TranscriptionEngine(config)
            assert engine.config.model == config_data["model"]
            assert engine.config.language == config_data["language"]
            assert engine.config.temperature == config_data["temperature"]