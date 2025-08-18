"""
Integration tests for Stage 3: Transcription Engine.

Tests focused integration between audio processing and transcription,
Whisper model management, and Spanish language processing.
"""
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.audio_to_json.audio_processor import AudioProcessor, ProcessedAudio
from src.audio_to_json.transcription import TranscriptionEngine, Word, transcribe_audio
from src.shared.config import Config, WhisperConfig
from src.shared.models import AudioMetadata
from src.shared.exceptions import TranscriptionError


class TestAudioToTranscriptionIntegration:
    """Test integration between audio processing and transcription."""
    
    def test_processed_audio_flows_to_transcription_engine(self):
        """Test that ProcessedAudio objects work correctly with TranscriptionEngine."""
        config = Config()
        processor = AudioProcessor(config)
        transcription_engine = TranscriptionEngine(config.whisper)
        
        # Mock audio file processing
        with patch('pathlib.Path.exists', return_value=True), \
             patch('librosa.load') as mock_load, \
             patch('os.path.getsize', return_value=1000), \
             patch('soundfile.info') as mock_info:
            
            # Setup mocks for audio processing
            mock_load.return_value = (np.array([0.1, 0.2, 0.3], dtype=np.float32), 16000)
            mock_info.return_value = MagicMock(channels=1, format='WAV')
            
            # Process audio
            processed_audio = processor.process_audio("test.wav")
            
            # Mock Whisper model and transcription
            with patch.object(transcription_engine, '_model', None), \
                 patch('whisper.load_model') as mock_load_model:
                
                mock_model = MagicMock()
                mock_model.transcribe.return_value = {
                    "segments": [{
                        "words": [
                            {"word": " hola", "start": 0.0, "end": 0.5, "probability": 0.9},
                            {"word": " mundo", "start": 0.5, "end": 1.0, "probability": 0.8}
                        ]
                    }]
                }
                mock_load_model.return_value = mock_model
                
                # Test transcription integration
                words = transcription_engine.transcribe_audio(processed_audio)
                
                # Verify integration worked correctly
                assert len(words) == 2
                assert words[0].text == "hola"
                assert words[1].text == "mundo"
                assert words[0].confidence == 0.9
                assert words[1].confidence == 0.8
                
                # Verify Whisper was called with correct audio data
                mock_model.transcribe.assert_called_once()
                call_args = mock_model.transcribe.call_args
                assert np.array_equal(call_args[0][0], processed_audio.data)


class TestWhisperModelManagementIntegration:
    """Test Whisper model loading and configuration integration."""
    
    def test_whisper_config_affects_model_loading(self):
        """Test that WhisperConfig properly configures model loading."""
        # Test with different model sizes
        for model_name in ["tiny", "base", "small"]:
            whisper_config = WhisperConfig()
            whisper_config.model = model_name
            
            transcription_engine = TranscriptionEngine(whisper_config)
            
            with patch('whisper.load_model') as mock_load_model:
                mock_model = MagicMock()
                mock_load_model.return_value = mock_model
                
                # Access model property to trigger lazy loading
                _ = transcription_engine.model
                
                # Verify correct model was requested
                mock_load_model.assert_called_once_with(model_name)
    
    def test_transcription_options_from_config(self):
        """Test that transcription options are correctly set from config."""
        whisper_config = WhisperConfig()
        whisper_config.language = "es"
        whisper_config.temperature = 0.5
        whisper_config.word_timestamps = True
        
        transcription_engine = TranscriptionEngine(whisper_config)
        
        # Create test audio
        audio_data = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        processed_audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        with patch.object(transcription_engine, '_model', None), \
             patch('whisper.load_model') as mock_load_model:
            
            mock_model = MagicMock()
            mock_model.transcribe.return_value = {
                "segments": [{
                    "words": [{"word": " test", "start": 0.0, "end": 0.5, "probability": 0.9}]
                }]
            }
            mock_load_model.return_value = mock_model
            
            # Perform transcription
            transcription_engine.transcribe_audio(processed_audio)
            
            # Verify transcription was called with correct options
            mock_model.transcribe.assert_called_once()
            call_kwargs = mock_model.transcribe.call_args[1]
            
            assert call_kwargs["language"] == "es"
            assert call_kwargs["temperature"] == 0.5
            assert call_kwargs["word_timestamps"] is True


class TestSpanishLanguageProcessingIntegration:
    """Test Spanish language specific processing integration."""
    
    def test_spanish_word_extraction_and_cleaning(self):
        """Test that Spanish words are correctly extracted and cleaned."""
        config = Config()
        transcription_engine = TranscriptionEngine(config.whisper)
        
        # Create test audio
        audio_data = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        processed_audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        with patch.object(transcription_engine, '_model', None), \
             patch('whisper.load_model') as mock_load_model:
            
            mock_model = MagicMock()
            # Simulate Whisper output with Spanish words (including leading spaces)
            mock_model.transcribe.return_value = {
                "segments": [{
                    "words": [
                        {"word": " hola", "start": 0.0, "end": 0.5, "probability": 0.9},
                        {"word": " ¿cómo", "start": 0.5, "end": 1.0, "probability": 0.8},
                        {"word": " estás?", "start": 1.0, "end": 1.5, "probability": 0.7},
                        {"word": " niño", "start": 1.5, "end": 2.0, "probability": 0.9}
                    ]
                }]
            }
            mock_load_model.return_value = mock_model
            
            words = transcription_engine.transcribe_audio(processed_audio)
            
            # Verify Spanish characters are preserved and words are cleaned
            assert len(words) == 4
            assert words[0].text == "hola"  # Leading space removed
            assert words[1].text == "¿cómo"  # Spanish question mark preserved
            assert words[2].text == "estás?"  # Accent and punctuation preserved
            assert words[3].text == "niño"  # Ñ character preserved
    
    def test_segment_fallback_for_spanish_content(self):
        """Test fallback to segment-level timing when word timestamps unavailable."""
        config = Config()
        transcription_engine = TranscriptionEngine(config.whisper)
        
        # Create test audio
        audio_data = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        processed_audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        with patch.object(transcription_engine, '_model', None), \
             patch('whisper.load_model') as mock_load_model:
            
            mock_model = MagicMock()
            # Simulate Whisper output without word timestamps
            mock_model.transcribe.return_value = {
                "segments": [{
                    "start": 0.0,
                    "end": 2.0,
                    "text": " hola mundo español"
                }]
            }
            mock_load_model.return_value = mock_model
            
            words = transcription_engine.transcribe_audio(processed_audio)
            
            # Verify fallback creates words from segment text
            assert len(words) == 3
            assert words[0].text == "hola"
            assert words[1].text == "mundo"
            assert words[2].text == "español"
            
            # Verify timing is distributed across segment duration
            assert words[0].start_time == 0.0
            assert words[2].end_time == 2.0
            assert words[0].end_time <= words[1].start_time  # Adjacent or overlapping is fine


class TestTranscriptionErrorHandlingIntegration:
    """Test error handling integration in transcription pipeline."""
    
    def test_transcription_error_propagation(self):
        """Test that transcription errors are properly caught and wrapped."""
        config = Config()
        transcription_engine = TranscriptionEngine(config.whisper)
        
        # Create test audio
        audio_data = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        processed_audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        with patch.object(transcription_engine, '_model', None), \
             patch('whisper.load_model') as mock_load_model:
            
            mock_model = MagicMock()
            mock_model.transcribe.side_effect = RuntimeError("Whisper model error")
            mock_load_model.return_value = mock_model
            
            # Test error handling
            with pytest.raises(TranscriptionError) as exc_info:
                transcription_engine.transcribe_audio(processed_audio)
            
            # Verify error was properly wrapped
            assert "Transcription failed" in str(exc_info.value)
            assert isinstance(exc_info.value, TranscriptionError)
    
    def test_empty_transcription_handling(self):
        """Test handling of empty transcription results."""
        config = Config()
        transcription_engine = TranscriptionEngine(config.whisper)
        
        # Create test audio
        audio_data = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        processed_audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        with patch.object(transcription_engine, '_model', None), \
             patch('whisper.load_model') as mock_load_model:
            
            mock_model = MagicMock()
            # Simulate empty transcription result
            mock_model.transcribe.return_value = {"segments": []}
            mock_load_model.return_value = mock_model
            
            # Should raise TranscriptionError for empty results
            with pytest.raises(TranscriptionError, match="No words extracted"):
                transcription_engine.transcribe_audio(processed_audio)


class TestConvenienceFunctionIntegration:
    """Test integration of convenience transcribe_audio function."""
    
    def test_transcribe_audio_function_integration(self):
        """Test that transcribe_audio function works with ProcessedAudio."""
        config = Config()
        
        # Create test audio
        audio_data = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        processed_audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        with patch('src.audio_to_json.transcription.TranscriptionEngine') as mock_engine_class:
            mock_engine = MagicMock()
            mock_words = [Word("test", 0.0, 0.5, 0.9)]
            mock_engine.transcribe_audio.return_value = mock_words
            mock_engine_class.return_value = mock_engine
            
            # Test convenience function
            result = transcribe_audio(processed_audio, config.whisper)
            
            # Verify function works correctly
            assert result == mock_words
            mock_engine_class.assert_called_once_with(config.whisper)
            mock_engine.transcribe_audio.assert_called_once_with(processed_audio)


class TestPerformanceIntegration:
    """Test performance-related integration aspects."""
    
    def test_model_lazy_loading_efficiency(self):
        """Test that model is only loaded once and reused."""
        config = Config()
        transcription_engine = TranscriptionEngine(config.whisper)
        
        with patch('whisper.load_model') as mock_load_model:
            mock_model = MagicMock()
            mock_load_model.return_value = mock_model
            
            # Access model multiple times
            _ = transcription_engine.model
            _ = transcription_engine.model
            _ = transcription_engine.model
            
            # Verify model was only loaded once
            mock_load_model.assert_called_once()
    
    def test_large_audio_processing_integration(self):
        """Test integration with large audio files."""
        config = Config()
        transcription_engine = TranscriptionEngine(config.whisper)
        
        # Create large audio array (simulate 5 minutes of audio)
        large_audio_data = np.array([0.1] * (16000 * 300), dtype=np.float32)
        metadata = AudioMetadata(
            path="large.wav", duration=300.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=10000000
        )
        processed_audio = ProcessedAudio(large_audio_data, 16000, 300.0, metadata)
        
        with patch.object(transcription_engine, '_model', None), \
             patch('whisper.load_model') as mock_load_model:
            
            mock_model = MagicMock()
            # Simulate many words in long audio
            mock_segments = []
            for i in range(50):  # 50 segments
                mock_segments.append({
                    "words": [
                        {"word": f" word{i*2}", "start": i*2, "end": i*2+0.5, "probability": 0.8},
                        {"word": f" word{i*2+1}", "start": i*2+0.5, "end": i*2+1, "probability": 0.8}
                    ]
                })
            
            mock_model.transcribe.return_value = {"segments": mock_segments}
            mock_load_model.return_value = mock_model
            
            words = transcription_engine.transcribe_audio(processed_audio)
            
            # Verify large transcription is handled correctly
            assert len(words) == 100  # 50 segments * 2 words each
            assert words[0].text == "word0"
            assert words[-1].text == "word99"
            
            # Verify all timing is correct
            for word in words:
                assert word.start_time < word.end_time
                assert word.confidence > 0