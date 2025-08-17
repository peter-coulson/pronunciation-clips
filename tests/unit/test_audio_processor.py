"""
Unit tests for audio processing module.

Tests audio loading, validation, resampling, and ProcessedAudio functionality.
Focuses on edge cases, error handling, and configuration validation.
"""
import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import numpy as np

from src.audio_to_json.audio_processor import AudioProcessor, ProcessedAudio, process_audio
from src.shared.config import Config, AudioConfig
from src.shared.models import AudioMetadata
from src.shared.exceptions import AudioError


class TestProcessedAudio:
    """Test ProcessedAudio container class."""
    
    def test_processed_audio_creation(self):
        """Test creating ProcessedAudio object."""
        data = np.array([0.1, 0.2, 0.3, 0.4])
        sample_rate = 16000
        duration = 0.25
        metadata = AudioMetadata(
            path="test.wav",
            duration=duration,
            sample_rate=sample_rate,
            channels=1,
            format="wav",
            size_bytes=1000
        )
        
        processed = ProcessedAudio(data, sample_rate, duration, metadata)
        
        assert np.array_equal(processed.data, data)
        assert processed.sample_rate == sample_rate
        assert processed.duration == duration
        assert processed.metadata == metadata
        assert processed.channels == 1
    
    def test_processed_audio_mono_channel_detection(self):
        """Test channel detection for mono audio."""
        mono_data = np.array([0.1, 0.2, 0.3])
        metadata = AudioMetadata(
            path="test.wav", duration=0.1, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        
        processed = ProcessedAudio(mono_data, 16000, 0.1, metadata)
        assert processed.channels == 1
    
    def test_processed_audio_stereo_channel_detection(self):
        """Test channel detection for stereo audio."""
        stereo_data = np.array([[0.1, 0.2], [0.3, 0.4]])  # 2 channels, 2 samples
        metadata = AudioMetadata(
            path="test.wav", duration=0.1, sample_rate=16000,
            channels=2, format="wav", size_bytes=1000
        )
        
        processed = ProcessedAudio(stereo_data, 16000, 0.1, metadata)
        assert processed.channels == 2
    
    def test_processed_audio_repr(self):
        """Test string representation of ProcessedAudio."""
        data = np.array([0.1, 0.2])
        metadata = AudioMetadata(
            path="test.wav", duration=1.5, sample_rate=44100,
            channels=1, format="wav", size_bytes=1000
        )
        
        processed = ProcessedAudio(data, 44100, 1.5, metadata)
        repr_str = repr(processed)
        
        assert "ProcessedAudio" in repr_str
        assert "duration=1.50s" in repr_str
        assert "sr=44100Hz" in repr_str
        assert "channels=1" in repr_str


class TestAudioProcessor:
    """Test AudioProcessor class."""
    
    def test_audio_processor_creation(self):
        """Test creating AudioProcessor with config."""
        config = Config()
        processor = AudioProcessor(config)
        
        assert processor.config == config
        assert processor.logger is not None
    
    @patch('src.audio_to_json.audio_processor.Path.exists')
    def test_process_audio_file_not_found(self, mock_exists):
        """Test processing non-existent audio file."""
        mock_exists.return_value = False
        
        config = Config()
        processor = AudioProcessor(config)
        
        with pytest.raises(AudioError, match="Audio file not found"):
            processor.process_audio("nonexistent.wav")
    
    @patch('src.audio_to_json.audio_processor.sf.info')
    @patch('src.audio_to_json.audio_processor.os.path.getsize')
    @patch('src.audio_to_json.audio_processor.librosa.load')
    @patch('src.audio_to_json.audio_processor.Path.exists')
    def test_process_audio_successful_mono(self, mock_exists, mock_load, mock_getsize, mock_info):
        """Test successful audio processing for mono file."""
        # Setup mocks
        mock_exists.return_value = True
        mock_load.return_value = (np.array([0.1, 0.2, 0.3]), 16000)
        mock_getsize.return_value = 1000
        mock_info.return_value = MagicMock(channels=1, format='WAV')
        
        config = Config()
        processor = AudioProcessor(config)
        
        result = processor.process_audio("test.wav")
        
        assert isinstance(result, ProcessedAudio)
        assert result.sample_rate == 16000
        assert result.channels == 1
        assert result.metadata.path == "test.wav"
    
    @patch('src.audio_to_json.audio_processor.sf.info')
    @patch('src.audio_to_json.audio_processor.os.path.getsize')
    @patch('src.audio_to_json.audio_processor.librosa.resample')
    @patch('src.audio_to_json.audio_processor.librosa.load')
    @patch('src.audio_to_json.audio_processor.Path.exists')
    def test_process_audio_with_resampling(self, mock_exists, mock_load, mock_resample, mock_getsize, mock_info):
        """Test audio processing with resampling."""
        # Setup mocks
        mock_exists.return_value = True
        original_data = np.array([0.1, 0.2, 0.3, 0.4])
        resampled_data = np.array([0.1, 0.3])  # Downsampled
        mock_load.return_value = (original_data, 44100)  # Original SR different from target
        mock_resample.return_value = resampled_data
        mock_getsize.return_value = 2000
        mock_info.return_value = MagicMock(channels=1, format='WAV')
        
        config = Config()
        config.audio.sample_rate = 16000  # Different from original 44100
        processor = AudioProcessor(config)
        
        result = processor.process_audio("test.wav")
        
        # Verify resampling was called
        mock_resample.assert_called_once_with(original_data, orig_sr=44100, target_sr=16000)
        assert result.sample_rate == 16000
        assert np.array_equal(result.data, resampled_data)
    
    @patch('src.audio_to_json.audio_processor.sf.info')
    @patch('src.audio_to_json.audio_processor.os.path.getsize')
    @patch('src.audio_to_json.audio_processor.librosa.load')
    @patch('src.audio_to_json.audio_processor.Path.exists')
    def test_process_audio_stereo_to_mono_conversion(self, mock_exists, mock_load, mock_getsize, mock_info):
        """Test stereo to mono conversion."""
        # Setup mocks
        mock_exists.return_value = True
        stereo_data = np.array([[0.1, 0.3], [0.2, 0.4]])  # 2 channels
        mock_load.return_value = (stereo_data, 16000)
        mock_getsize.return_value = 1500
        mock_info.return_value = MagicMock(channels=2, format='WAV')
        
        config = Config()
        config.audio.channels = 1  # Force mono
        processor = AudioProcessor(config)
        
        result = processor.process_audio("stereo.wav")
        
        # Should be converted to mono by averaging channels
        assert result.channels == 1
        assert len(result.data.shape) == 1  # 1D array for mono
    
    @patch('src.audio_to_json.audio_processor.sf.info')
    @patch('src.audio_to_json.audio_processor.os.path.getsize')
    @patch('src.audio_to_json.audio_processor.librosa.load')
    @patch('src.audio_to_json.audio_processor.Path.exists')
    def test_process_audio_preserve_stereo(self, mock_exists, mock_load, mock_getsize, mock_info):
        """Test preserving stereo when configured."""
        # Setup mocks
        mock_exists.return_value = True
        stereo_data = np.array([[0.1, 0.3], [0.2, 0.4]])
        mock_load.return_value = (stereo_data, 16000)
        mock_getsize.return_value = 1500
        mock_info.return_value = MagicMock(channels=2, format='WAV')
        
        config = Config()
        config.audio.channels = 2  # Keep stereo
        processor = AudioProcessor(config)
        
        result = processor.process_audio("stereo.wav")
        
        assert result.channels == 2
        assert np.array_equal(result.data, stereo_data)
    
    @patch('src.audio_to_json.audio_processor.sf.info')
    @patch('src.audio_to_json.audio_processor.os.path.getsize')
    @patch('src.audio_to_json.audio_processor.librosa.load')
    @patch('src.audio_to_json.audio_processor.Path.exists')
    def test_process_audio_metadata_extraction(self, mock_exists, mock_load, mock_getsize, mock_info):
        """Test metadata extraction during audio processing."""
        # Setup mocks
        mock_exists.return_value = True
        audio_data = np.array([0.1, 0.2, 0.3, 0.4, 0.5])  # 5 samples
        original_sr = 44100
        mock_load.return_value = (audio_data, original_sr)
        mock_getsize.return_value = 2048
        mock_info.return_value = MagicMock(channels=1, format='FLAC')
        
        config = Config()
        processor = AudioProcessor(config)
        
        result = processor.process_audio("/path/to/test.flac")
        
        # Check metadata
        metadata = result.metadata
        assert metadata.path == "/path/to/test.flac"
        assert metadata.duration == len(audio_data) / original_sr
        assert metadata.sample_rate == original_sr
        assert metadata.channels == 1
        assert metadata.format == "flac"
        assert metadata.size_bytes == 2048
    
    @patch('src.audio_to_json.audio_processor.sf.info')
    @patch('src.audio_to_json.audio_processor.os.path.getsize')
    @patch('src.audio_to_json.audio_processor.librosa.load')
    @patch('src.audio_to_json.audio_processor.Path.exists')
    def test_process_audio_librosa_error(self, mock_exists, mock_load, mock_getsize, mock_info):
        """Test handling of librosa loading errors."""
        # Setup mocks
        mock_exists.return_value = True
        mock_load.side_effect = Exception("Corrupted audio file")
        
        config = Config()
        processor = AudioProcessor(config)
        
        with pytest.raises(AudioError, match="Failed to process audio file"):
            processor.process_audio("corrupted.wav")
    
    @patch('src.audio_to_json.audio_processor.sf.info')
    @patch('src.audio_to_json.audio_processor.os.path.getsize')
    @patch('src.audio_to_json.audio_processor.librosa.load')
    @patch('src.audio_to_json.audio_processor.Path.exists')
    def test_process_audio_logging(self, mock_exists, mock_load, mock_getsize, mock_info):
        """Test that audio processing logs are generated."""
        # Setup mocks
        mock_exists.return_value = True
        mock_load.return_value = (np.array([0.1, 0.2]), 16000)
        mock_getsize.return_value = 1000
        mock_info.return_value = MagicMock(channels=1, format='WAV')
        
        config = Config()
        processor = AudioProcessor(config)
        
        # Mock logging methods
        with patch.object(processor, 'log_stage_start') as mock_start, \
             patch.object(processor, 'log_progress') as mock_progress, \
             patch.object(processor, 'log_stage_complete') as mock_complete:
            
            processor.process_audio("test.wav")
            
            # Verify logging calls
            mock_start.assert_called_once()
            assert mock_progress.call_count >= 1  # At least one progress log
            mock_complete.assert_called_once()
    
    @patch('src.audio_to_json.audio_processor.sf.info')
    @patch('src.audio_to_json.audio_processor.os.path.getsize')
    @patch('src.audio_to_json.audio_processor.librosa.load')
    @patch('src.audio_to_json.audio_processor.Path.exists')
    def test_process_audio_error_logging(self, mock_exists, mock_load, mock_getsize, mock_info):
        """Test error logging during audio processing."""
        # Setup mocks
        mock_exists.return_value = True
        mock_load.side_effect = Exception("Test error")
        
        config = Config()
        processor = AudioProcessor(config)
        
        # Mock logging methods
        with patch.object(processor, 'log_stage_error') as mock_error:
            with pytest.raises(AudioError):
                processor.process_audio("test.wav")
            
            # Verify error logging
            mock_error.assert_called_once()


class TestProcessAudioFunction:
    """Test standalone process_audio function."""
    
    @patch('src.audio_to_json.audio_processor.AudioProcessor')
    def test_process_audio_function(self, mock_processor_class):
        """Test the convenience process_audio function."""
        # Setup mocks
        mock_processor = MagicMock()
        mock_result = MagicMock()
        mock_processor.process_audio.return_value = mock_result
        mock_processor_class.return_value = mock_processor
        
        config = Config()
        result = process_audio("test.wav", config)
        
        # Verify function calls
        mock_processor_class.assert_called_once_with(config)
        mock_processor.process_audio.assert_called_once_with("test.wav")
        assert result == mock_result
    
    @patch('src.audio_to_json.audio_processor.AudioProcessor')
    def test_process_audio_function_error_propagation(self, mock_processor_class):
        """Test that the function properly propagates errors."""
        # Setup mocks
        mock_processor = MagicMock()
        mock_processor.process_audio.side_effect = AudioError("Test error")
        mock_processor_class.return_value = mock_processor
        
        config = Config()
        
        with pytest.raises(AudioError, match="Test error"):
            process_audio("test.wav", config)


class TestAudioProcessorEdgeCases:
    """Test edge cases and boundary conditions."""
    
    @patch('src.audio_to_json.audio_processor.sf.info')
    @patch('src.audio_to_json.audio_processor.os.path.getsize')
    @patch('src.audio_to_json.audio_processor.librosa.load')
    @patch('src.audio_to_json.audio_processor.Path.exists')
    def test_process_empty_audio_file(self, mock_exists, mock_load, mock_getsize, mock_info):
        """Test processing an empty audio file."""
        # Setup mocks
        mock_exists.return_value = True
        mock_load.return_value = (np.array([]), 16000)  # Empty audio
        mock_getsize.return_value = 44  # Just header bytes
        mock_info.return_value = MagicMock(channels=1, format='WAV')
        
        config = Config()
        processor = AudioProcessor(config)
        
        result = processor.process_audio("empty.wav")
        
        assert len(result.data) == 0
        assert result.duration == 0.0
    
    @patch('src.audio_to_json.audio_processor.sf.info')
    @patch('src.audio_to_json.audio_processor.os.path.getsize')
    @patch('src.audio_to_json.audio_processor.librosa.load')
    @patch('src.audio_to_json.audio_processor.Path.exists')
    def test_process_very_short_audio(self, mock_exists, mock_load, mock_getsize, mock_info):
        """Test processing very short audio files."""
        # Setup mocks
        mock_exists.return_value = True
        mock_load.return_value = (np.array([0.1]), 16000)  # Single sample
        mock_getsize.return_value = 100
        mock_info.return_value = MagicMock(channels=1, format='WAV')
        
        config = Config()
        processor = AudioProcessor(config)
        
        result = processor.process_audio("short.wav")
        
        assert len(result.data) == 1
        assert result.duration == 1/16000  # Duration of single sample
    
    @patch('src.audio_to_json.audio_processor.sf.info')
    @patch('src.audio_to_json.audio_processor.os.path.getsize')
    @patch('src.audio_to_json.audio_processor.librosa.load')
    @patch('src.audio_to_json.audio_processor.Path.exists')
    def test_process_audio_different_config_sample_rates(self, mock_exists, mock_load, mock_getsize, mock_info):
        """Test processing with various target sample rates."""
        # Setup mocks
        mock_exists.return_value = True
        original_data = np.array([0.1, 0.2, 0.3, 0.4])
        mock_load.return_value = (original_data, 44100)
        mock_getsize.return_value = 1000
        mock_info.return_value = MagicMock(channels=1, format='WAV')
        
        # Test different target sample rates
        for target_sr in [8000, 16000, 22050, 48000]:
            config = Config()
            config.audio.sample_rate = target_sr
            processor = AudioProcessor(config)
            
            with patch('src.audio_to_json.audio_processor.librosa.resample') as mock_resample:
                mock_resample.return_value = np.array([0.1, 0.2])  # Mock resampled data
                
                result = processor.process_audio("test.wav")
                
                if target_sr != 44100:  # Should resample if different
                    mock_resample.assert_called_once_with(original_data, orig_sr=44100, target_sr=target_sr)
                    assert result.sample_rate == target_sr
    
    @patch('src.audio_to_json.audio_processor.sf.info')
    @patch('src.audio_to_json.audio_processor.os.path.getsize')
    @patch('src.audio_to_json.audio_processor.librosa.load')
    @patch('src.audio_to_json.audio_processor.Path.exists')
    def test_process_audio_special_characters_path(self, mock_exists, mock_load, mock_getsize, mock_info):
        """Test processing audio with special characters in path."""
        # Setup mocks
        mock_exists.return_value = True
        mock_load.return_value = (np.array([0.1, 0.2]), 16000)
        mock_getsize.return_value = 1000
        mock_info.return_value = MagicMock(channels=1, format='WAV')
        
        config = Config()
        processor = AudioProcessor(config)
        
        # Test with special characters
        special_path = "/path/to/spanish_ñoño_ü_audio.wav"
        result = processor.process_audio(special_path)
        
        assert result.metadata.path == special_path
    
    def test_audio_processor_with_different_configs(self):
        """Test AudioProcessor with various configurations."""
        # Test different audio configs
        configs = [
            {"sample_rate": 8000, "channels": 1},
            {"sample_rate": 44100, "channels": 2},
            {"sample_rate": 48000, "channels": 1},
        ]
        
        for config_data in configs:
            config = Config()
            config.audio.sample_rate = config_data["sample_rate"]
            config.audio.channels = config_data["channels"]
            
            processor = AudioProcessor(config)
            assert processor.config.audio.sample_rate == config_data["sample_rate"]
            assert processor.config.audio.channels == config_data["channels"]