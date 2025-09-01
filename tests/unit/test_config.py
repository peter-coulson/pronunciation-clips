"""
Unit tests for configuration module.

Tests config loading, validation, defaults, and error handling.
Focuses on edge cases and boundary conditions.
"""
import pytest
import tempfile
import os
from pathlib import Path

from src.shared.config import (
    Config, AudioConfig, WhisperConfig, SpeakersConfig, DiarizationConfig,
    QualityConfig, OutputConfig, LoggingConfig, load_config
)
from src.shared.exceptions import ConfigError

pytestmark = [
    pytest.mark.unit,
    pytest.mark.quick
]

class TestAudioConfig:
    """Test AudioConfig validation and defaults."""
    
    def test_default_values(self):
        """Test default audio configuration values."""
        config = AudioConfig()
        assert config.sample_rate == 16000
        assert config.channels == 1
        assert config.buffer_seconds == 0.025
    
    def test_sample_rate_validation(self):
        """Test sample rate boundary validation."""
        # Valid sample rates
        AudioConfig(sample_rate=8000)
        AudioConfig(sample_rate=44100)
        
        # Invalid sample rates
        with pytest.raises(ValueError):
            AudioConfig(sample_rate=7999)  # Too low
        
        with pytest.raises(ValueError):
            AudioConfig(sample_rate=48001)  # Too high
    
    def test_channels_validation(self):
        """Test channel count validation."""
        # Valid channels
        AudioConfig(channels=1)
        AudioConfig(channels=2)
        
        # Invalid channels
        with pytest.raises(ValueError):
            AudioConfig(channels=0)
        
        with pytest.raises(ValueError):
            AudioConfig(channels=3)
    
    def test_buffer_validation(self):
        """Test buffer seconds validation."""
        # Valid buffer
        AudioConfig(buffer_seconds=0.0)
        AudioConfig(buffer_seconds=1.0)
        
        # Invalid buffer
        with pytest.raises(ValueError):
            AudioConfig(buffer_seconds=-0.1)


class TestWhisperConfig:
    """Test WhisperConfig validation."""
    
    def test_default_values(self):
        """Test default Whisper configuration."""
        config = WhisperConfig()
        assert config.model == "base"
        assert config.language == "es"
        assert config.word_timestamps is True
        assert config.temperature == 0.0
    
    def test_model_validation(self):
        """Test model name validation."""
        # Valid models
        for model in ["tiny", "base", "small", "medium", "large"]:
            WhisperConfig(model=model)
        
        # Invalid model
        with pytest.raises(ValueError):
            WhisperConfig(model="invalid_model")
    
    def test_language_validation(self):
        """Test language code validation."""
        # Valid languages (no validation exists, so any string works)
        WhisperConfig(language="en")
        WhisperConfig(language="es")
        WhisperConfig(language="fr")
        WhisperConfig(language="english")  # This actually works since no validation exists
    
    def test_temperature_validation(self):
        """Test temperature range validation."""
        # Valid temperatures
        WhisperConfig(temperature=0.0)
        WhisperConfig(temperature=0.5)
        WhisperConfig(temperature=1.0)
        
        # Invalid temperatures
        with pytest.raises(ValueError):
            WhisperConfig(temperature=-0.1)
        
        with pytest.raises(ValueError):
            WhisperConfig(temperature=1.1)


class TestQualityConfig:
    """Test QualityConfig validation and edge cases."""
    
    def test_default_values(self):
        """Test default quality configuration."""
        config = QualityConfig()
        assert config.min_confidence == 0.8
        assert config.min_word_duration == 0.3
        assert config.max_word_duration == 3.0
        assert config.syllable_range == [2, 6]
    
    def test_confidence_validation(self):
        """Test confidence range validation."""
        # Valid confidence
        QualityConfig(min_confidence=0.0)
        QualityConfig(min_confidence=1.0)
        
        # Invalid confidence
        with pytest.raises(ValueError):
            QualityConfig(min_confidence=-0.1)
        
        with pytest.raises(ValueError):
            QualityConfig(min_confidence=1.1)
    
    def test_duration_validation(self):
        """Test duration range validation."""
        # Valid durations
        QualityConfig(min_word_duration=0.0, max_word_duration=1.0)
        
        # Invalid - negative min (using Pydantic's ge=0.0 constraint)
        with pytest.raises(ValueError):
            QualityConfig(min_word_duration=-0.1)
        
        # Invalid - max too small (using Pydantic's ge=0.1 constraint)
        with pytest.raises(ValueError):
            QualityConfig(max_word_duration=0.05)
    
    def test_syllable_range_validation(self):
        """Test syllable range validation."""
        # Valid ranges
        QualityConfig(syllable_range=[1, 5])
        QualityConfig(syllable_range=[2, 6])
        
        # Invalid - min > max
        with pytest.raises(ValueError):
            QualityConfig(syllable_range=[5, 2])
        
        # Invalid - negative values
        with pytest.raises(ValueError):
            QualityConfig(syllable_range=[0, 5])


class TestSpeakersConfig:
    """Test SpeakersConfig validation."""
    
    def test_default_values(self):
        """Test default speaker configuration."""
        config = SpeakersConfig()
        assert config.enable_diarization is False
        assert config.min_speakers == 1
        assert config.max_speakers == 10
    
    def test_speaker_count_validation(self):
        """Test speaker count validation."""
        # Valid counts
        SpeakersConfig(min_speakers=1, max_speakers=10)
        
        # Invalid - zero min (using Pydantic's ge=1 constraint)
        with pytest.raises(ValueError):
            SpeakersConfig(min_speakers=0)
        
        # Invalid - max too high (using Pydantic's le=50 constraint)
        with pytest.raises(ValueError):
            SpeakersConfig(max_speakers=51)


class TestDiarizationConfig:
    """Test DiarizationConfig validation."""
    
    def test_default_values(self):
        """Test default diarization configuration."""
        config = DiarizationConfig()
        assert config.model == "pyannote/speaker-diarization"
        assert config.min_speakers == 1
        assert config.max_speakers == 10
        assert config.segmentation_threshold == 0.5
        assert config.clustering_threshold == 0.7
    
    def test_speaker_count_validation(self):
        """Test speaker count validation."""
        # Valid counts
        DiarizationConfig(min_speakers=1, max_speakers=10)
        DiarizationConfig(min_speakers=2, max_speakers=50)
        
        # Invalid - zero min (using Pydantic's ge=1 constraint)
        with pytest.raises(ValueError):
            DiarizationConfig(min_speakers=0)
        
        # Invalid - max too high (using Pydantic's le=50 constraint)
        with pytest.raises(ValueError):
            DiarizationConfig(max_speakers=51)
    
    def test_threshold_validation(self):
        """Test threshold value validation."""
        # Valid threshold values (0.0 to 1.0)
        DiarizationConfig(segmentation_threshold=0.0, clustering_threshold=0.0)
        DiarizationConfig(segmentation_threshold=0.5, clustering_threshold=0.7)
        DiarizationConfig(segmentation_threshold=1.0, clustering_threshold=1.0)
        
        # Invalid segmentation threshold
        with pytest.raises(ValueError):
            DiarizationConfig(segmentation_threshold=-0.1)
        
        with pytest.raises(ValueError):
            DiarizationConfig(segmentation_threshold=1.1)
        
        # Invalid clustering threshold
        with pytest.raises(ValueError):
            DiarizationConfig(clustering_threshold=-0.1)
        
        with pytest.raises(ValueError):
            DiarizationConfig(clustering_threshold=1.1)
    
    def test_model_field(self):
        """Test model field configuration."""
        config = DiarizationConfig(model="custom/diarization-model")
        assert config.model == "custom/diarization-model"


class TestOutputConfig:
    """Test OutputConfig validation."""
    
    def test_default_values(self):
        """Test default output configuration."""
        config = OutputConfig()
        assert config.database_path == "word_database.json"
        assert config.encoding == "utf-8"
        assert config.pretty_print is True
        assert config.backup_on_update is True


class TestLoggingConfig:
    """Test LoggingConfig validation."""
    
    def test_default_values(self):
        """Test default logging configuration."""
        config = LoggingConfig()
        assert config.level == "INFO"
        assert config.format == "structured"
    
    def test_level_validation(self):
        """Test logging level validation."""
        # Valid levels
        for level in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            LoggingConfig(level=level)
        
        # Invalid level
        with pytest.raises(ValueError):
            LoggingConfig(level="INVALID")
    
    def test_format_validation(self):
        """Test logging format validation."""
        # Valid formats
        LoggingConfig(format="simple")
        LoggingConfig(format="structured")
        
        # Invalid format
        with pytest.raises(ValueError):
            LoggingConfig(format="invalid")


class TestConfig:
    """Test main Config class and composition."""
    
    def test_default_config(self):
        """Test default configuration creation."""
        config = Config()
        assert isinstance(config.audio, AudioConfig)
        assert isinstance(config.whisper, WhisperConfig)
        assert isinstance(config.speakers, SpeakersConfig)
        assert isinstance(config.quality, QualityConfig)
        assert isinstance(config.output, OutputConfig)
        assert isinstance(config.logging, LoggingConfig)


class TestConfigLoading:
    """Test configuration file loading and error handling."""
    
    def test_load_valid_config(self):
        """Test loading valid YAML configuration."""
        config_yaml = """
audio:
  sample_rate: 16000
  channels: 1
  buffer_seconds: 0.1

whisper:
  model: "base"
  language: "es"
  word_timestamps: true
  temperature: 0.0

quality:
  min_confidence: 0.8
  min_word_duration: 0.3
  max_word_duration: 3.0
  syllable_range: [2, 6]
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(config_yaml)
            f.flush()
            
            try:
                config = load_config(f.name)
                assert config.audio.sample_rate == 16000
                assert config.whisper.model == "base"
                assert config.quality.min_confidence == 0.8
            finally:
                os.unlink(f.name)
    
    def test_load_nonexistent_file(self):
        """Test loading non-existent configuration file."""
        with pytest.raises(ConfigError):
            load_config("nonexistent_config.yaml")
    
    def test_load_invalid_yaml(self):
        """Test loading invalid YAML syntax."""
        invalid_yaml = """
audio:
  sample_rate: 16000
whisper:
  model: "base"
  - invalid syntax
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(invalid_yaml)
            f.flush()
            
            try:
                with pytest.raises(ConfigError):
                    load_config(f.name)
            finally:
                os.unlink(f.name)
    
    def test_load_config_validation_error(self):
        """Test loading config with validation errors."""
        invalid_config = """
audio:
  sample_rate: 99999  # Invalid sample rate
whisper:
  model: "invalid_model"  # Invalid model
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(invalid_config)
            f.flush()
            
            try:
                with pytest.raises(ConfigError):
                    load_config(f.name)
            finally:
                os.unlink(f.name)
    
    def test_partial_config_with_defaults(self):
        """Test loading partial config uses defaults for missing values."""
        partial_config = """
audio:
  sample_rate: 44100
# whisper config missing - should use defaults
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(partial_config)
            f.flush()
            
            try:
                config = load_config(f.name)
                assert config.audio.sample_rate == 44100
                assert config.whisper.model == "base"  # Default value
            finally:
                os.unlink(f.name)