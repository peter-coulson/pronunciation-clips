"""
Configuration loading and validation using Pydantic.

Loads YAML configuration files and validates them with type hints and custom validators.
Supports environment variable overrides for flexible deployment.
"""
import os
import yaml
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator

from .exceptions import ConfigError


class AudioConfig(BaseModel):
    """Audio processing configuration."""
    sample_rate: int = Field(default=16000, ge=8000, le=48000)
    channels: int = Field(default=1, ge=1, le=2)
    buffer_seconds: float = Field(default=0.025, ge=0.0, le=1.0)


class WhisperConfig(BaseModel):
    """Whisper transcription configuration."""
    model: str = Field(default="base")
    language: str = Field(default="es")
    word_timestamps: bool = Field(default=True)
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)
    
    @field_validator('model')
    @classmethod
    def validate_model(cls, v):
        valid_models = ["tiny", "base", "small", "medium", "large"]
        if v not in valid_models:
            raise ValueError(f"model must be one of {valid_models}")
        return v


class SpeakersConfig(BaseModel):
    """Speaker identification configuration."""
    enable_diarization: bool = Field(default=False)
    min_speakers: int = Field(default=1, ge=1)
    max_speakers: int = Field(default=10, ge=1, le=50)
    default_speaker: Optional[Dict[str, str]] = Field(default=None)


class OutputConfig(BaseModel):
    """Output configuration."""
    database_path: str = Field(default="word_database.json")
    encoding: str = Field(default="utf-8")
    pretty_print: bool = Field(default=True)
    backup_on_update: bool = Field(default=True)


class QualityConfig(BaseModel):
    """Quality filtering configuration."""
    min_confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    min_word_duration: float = Field(default=0.3, ge=0.0)
    max_word_duration: float = Field(default=3.0, ge=0.1)
    syllable_range: List[int] = Field(default=[2, 6])
    
    @field_validator('syllable_range')
    @classmethod
    def validate_syllable_range(cls, v):
        if len(v) != 2 or v[0] >= v[1] or v[0] < 1:
            raise ValueError("syllable_range must be [min, max] with min < max and min >= 1")
        return v


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = Field(default="INFO")
    format: str = Field(default="structured")
    file: Optional[str] = Field(default=None)
    console: bool = Field(default=True)
    
    @field_validator('level')
    @classmethod
    def validate_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        if v.upper() not in valid_levels:
            raise ValueError(f"level must be one of {valid_levels}")
        return v.upper()
    
    @field_validator('format')
    @classmethod
    def validate_format(cls, v):
        valid_formats = ["structured", "simple"]
        if v not in valid_formats:
            raise ValueError(f"format must be one of {valid_formats}")
        return v


class Config(BaseModel):
    """Main configuration container."""
    audio: AudioConfig = Field(default_factory=AudioConfig)
    whisper: WhisperConfig = Field(default_factory=WhisperConfig)
    speakers: SpeakersConfig = Field(default_factory=SpeakersConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    quality: QualityConfig = Field(default_factory=QualityConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


def load_config(config_path: str = "config.yaml") -> Config:
    """
    Load configuration from YAML file with environment variable overrides.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        Validated configuration object
        
    Raises:
        ConfigError: If configuration loading or validation fails
    """
    try:
        # Load YAML file
        config_file = Path(config_path)
        if not config_file.exists():
            raise ConfigError(f"Configuration file not found: {config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
        
        if yaml_data is None:
            yaml_data = {}
        
        # Apply environment variable overrides
        yaml_data = _apply_env_overrides(yaml_data)
        
        # Validate with Pydantic
        config = Config(**yaml_data)
        
        return config
        
    except yaml.YAMLError as e:
        raise ConfigError(f"Invalid YAML in {config_path}: {e}")
    except Exception as e:
        raise ConfigError(f"Failed to load configuration: {e}")


def _apply_env_overrides(config_data: Dict[str, Any]) -> Dict[str, Any]:
    """Apply environment variable overrides to configuration data."""
    prefix = "PRONUNCIATION_CLIPS_"
    
    for env_key, env_value in os.environ.items():
        if not env_key.startswith(prefix):
            continue
            
        config_key = env_key[len(prefix):].lower()
        parts = config_key.split('_', 1)
        
        if len(parts) != 2:
            continue
            
        section, key = parts
        
        if section not in config_data:
            config_data[section] = {}
        
        value = _convert_env_value(env_value)
        config_data[section][key] = value
    
    return config_data


def _convert_env_value(value: str) -> Any:
    """Convert environment variable string to appropriate Python type."""
    if value.lower() in ('true', 'false'):
        return value.lower() == 'true'
    
    try:
        return int(value)
    except ValueError:
        pass
    
    try:
        return float(value)
    except ValueError:
        pass
    
    return value