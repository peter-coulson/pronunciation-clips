"""
Unit tests for custom exceptions.

Tests exception hierarchy, error context, and message formatting.
"""
import pytest

from src.shared.exceptions import (
    PipelineError, ConfigError, AudioError, TranscriptionError,
    EntityError, DatabaseError, SpeakerError
)

pytestmark = [
    pytest.mark.unit,
    pytest.mark.quick
]


class TestPipelineError:
    """Test base exception class."""
    
    def test_basic_exception(self):
        """Test basic exception creation and message."""
        error = PipelineError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)
    
    def test_exception_with_context(self):
        """Test exception with context data."""
        context = {"file": "test.wav", "stage": "transcription"}
        error = PipelineError("Test error", context)
        
        assert "Test error" in str(error)
        assert error.context == context
    
    def test_exception_inheritance(self):
        """Test exception inheritance from base Exception."""
        error = PipelineError("Test")
        assert isinstance(error, Exception)
        assert isinstance(error, PipelineError)


class TestConfigError:
    """Test configuration-related exceptions."""
    
    def test_config_error_creation(self):
        """Test ConfigError creation."""
        error = ConfigError("Invalid configuration")
        assert str(error) == "Invalid configuration"
        assert isinstance(error, PipelineError)
    
    def test_config_error_with_file_context(self):
        """Test ConfigError with file context."""
        context = {"config_file": "config.yaml", "field": "audio.sample_rate"}
        error = ConfigError("Invalid sample rate", context)
        
        assert "Invalid sample rate" in str(error)
        assert error.context["config_file"] == "config.yaml"
    
    def test_config_error_inheritance(self):
        """Test ConfigError inheritance chain."""
        error = ConfigError("Test")
        assert isinstance(error, ConfigError)
        assert isinstance(error, PipelineError)
        assert isinstance(error, Exception)


class TestAudioError:
    """Test audio processing exceptions."""
    
    def test_audio_error_creation(self):
        """Test AudioError creation."""
        error = AudioError("Audio processing failed")
        assert str(error) == "Audio processing failed"
        assert isinstance(error, PipelineError)
    
    def test_audio_error_with_context(self):
        """Test AudioError with audio file context."""
        context = {
            "audio_file": "test.wav",
            "sample_rate": 44100,
            "duration": 120.5,
            "error_type": "format_conversion"
        }
        error = AudioError("Failed to convert audio format", context)
        
        assert "Failed to convert audio format" in str(error)
        assert error.context["audio_file"] == "test.wav"
        assert error.context["sample_rate"] == 44100


class TestTranscriptionError:
    """Test transcription-related exceptions."""
    
    def test_transcription_error_creation(self):
        """Test TranscriptionError creation."""
        error = TranscriptionError("Whisper transcription failed")
        assert str(error) == "Whisper transcription failed"
        assert isinstance(error, PipelineError)
    
    def test_transcription_error_with_model_context(self):
        """Test TranscriptionError with model context."""
        context = {
            "model": "base",
            "language": "es",
            "audio_duration": 300.0,
            "words_extracted": 0
        }
        error = TranscriptionError("No words extracted from transcription", context)
        
        assert "No words extracted" in str(error)
        assert error.context["model"] == "base"
        assert error.context["words_extracted"] == 0


class TestEntityError:
    """Test entity creation and processing exceptions."""
    
    def test_entity_error_creation(self):
        """Test EntityError creation."""
        error = EntityError("Entity validation failed")
        assert str(error) == "Entity validation failed"
        assert isinstance(error, PipelineError)
    
    def test_entity_error_with_entity_context(self):
        """Test EntityError with entity context."""
        context = {
            "entity_id": "word_001",
            "entity_type": "word",
            "start_time": 1.0,
            "end_time": 0.5,  # Invalid - end < start
            "validation_error": "end_time must be greater than start_time"
        }
        error = EntityError("Entity validation failed", context)
        
        assert "Entity validation failed" in str(error)
        assert error.context["entity_id"] == "word_001"
        assert error.context["validation_error"] == "end_time must be greater than start_time"


class TestDatabaseError:
    """Test database operation exceptions."""
    
    def test_database_error_creation(self):
        """Test DatabaseError creation."""
        error = DatabaseError("Database write failed")
        assert str(error) == "Database write failed"
        assert isinstance(error, PipelineError)
    
    def test_database_error_with_operation_context(self):
        """Test DatabaseError with operation context."""
        context = {
            "operation": "write",
            "database_path": "/path/to/database.json",
            "entity_count": 500,
            "file_size": 1024000,
            "disk_space": "insufficient"
        }
        error = DatabaseError("Insufficient disk space for database write", context)
        
        assert "Insufficient disk space" in str(error)
        assert error.context["operation"] == "write"
        assert error.context["entity_count"] == 500




class TestExceptionInheritanceChain:
    """Test exception inheritance and polymorphism."""
    
    def test_all_exceptions_inherit_from_base(self):
        """Test all custom exceptions inherit from PipelineError."""
        exceptions = [
            ConfigError("test"),
            AudioError("test"),
            TranscriptionError("test"),
            EntityError("test"),
            DatabaseError("test"),
            SpeakerError("test")
        ]
        
        for exc in exceptions:
            assert isinstance(exc, PipelineError)
            assert isinstance(exc, Exception)
    
    def test_exception_catching_polymorphism(self):
        """Test that base exception can catch all derived exceptions."""
        exceptions = [
            ConfigError("config"),
            AudioError("audio"),
            TranscriptionError("transcription"),
            EntityError("entity"),
            DatabaseError("database"),
            SpeakerError("speaker")
        ]
        
        # Test that we can catch all with base exception
        for exc in exceptions:
            try:
                raise exc
            except PipelineError as caught:
                assert caught is exc
            except Exception:
                pytest.fail(f"Should have caught {type(exc).__name__} as PipelineError")
    
    def test_specific_exception_catching(self):
        """Test catching specific exception types."""
        # Test specific catching
        try:
            raise ConfigError("test config error")
        except ConfigError as e:
            assert str(e) == "test config error"
        except Exception:
            pytest.fail("Should have caught ConfigError specifically")
        
        # Test that specific catching doesn't catch other types
        with pytest.raises(AudioError):
            try:
                raise AudioError("test audio error")
            except ConfigError:
                pytest.fail("Should not catch AudioError as ConfigError")
            except AudioError:
                raise  # Re-raise for pytest.raises to catch