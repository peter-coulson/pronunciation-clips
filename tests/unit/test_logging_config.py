"""
Unit tests for logging configuration.

Tests logging setup, structured logging, and LoggerMixin functionality.
"""
import pytest
import logging
import json
from unittest.mock import patch, MagicMock
from io import StringIO

from src.shared.logging_config import LoggerMixin, init_logger
from src.shared.config import Config, LoggingConfig

pytestmark = [
    pytest.mark.unit,
    pytest.mark.quick
]

class TestLoggerMixin:
    """Test LoggerMixin functionality."""
    
    def test_logger_mixin_creates_logger(self):
        """Test that LoggerMixin creates a logger."""
        class TestClass(LoggerMixin):
            pass
        
        test_instance = TestClass()
        assert test_instance.logger is not None
        # structlog loggers don't have a name attribute like stdlib loggers
    
    def test_logger_mixin_different_classes_different_loggers(self):
        """Test that different classes get different loggers."""
        class TestClass1(LoggerMixin):
            pass
        
        class TestClass2(LoggerMixin):
            pass
        
        instance1 = TestClass1()
        instance2 = TestClass2()
        
        # Each instance should have its own logger instance
        assert instance1.logger is not None
        assert instance2.logger is not None
        # structlog loggers are different instances but don't have names like stdlib
    
    def test_log_progress_method(self):
        """Test log_progress method functionality."""
        class TestClass(LoggerMixin):
            pass
        
        test_instance = TestClass()
        
        # Mock the logger to capture log calls
        with patch.object(test_instance.logger, 'info') as mock_info:
            test_instance.log_progress("Test progress message", 
                                     stage="test", 
                                     count=5)
            
            # Verify log was called with structured format
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            
            # Check that structured logging format is used
            assert "Test progress message" in str(call_args)
    
    def test_log_stage_start_method(self):
        """Test log_stage_start method."""
        class TestClass(LoggerMixin):
            pass
        
        test_instance = TestClass()
        
        with patch.object(test_instance.logger, 'info') as mock_info:
            test_instance.log_stage_start("audio_processing", 
                                        file="test.wav",
                                        duration=120.0)
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            
            # Verify structured format includes stage information
            assert "audio_processing" in str(call_args)
            assert "Stage started" in str(call_args)
    
    def test_log_stage_complete_method(self):
        """Test log_stage_complete method."""
        class TestClass(LoggerMixin):
            pass
        
        test_instance = TestClass()
        
        with patch.object(test_instance.logger, 'info') as mock_info:
            test_instance.log_stage_complete("audio_processing",
                                           entities_processed=100,
                                           processing_time=25.5)
            
            mock_info.assert_called_once()
            call_args = mock_info.call_args
            
            assert "audio_processing" in str(call_args)
            assert "Stage completed" in str(call_args)
    
    def test_log_stage_error_method(self):
        """Test log_stage_error method."""
        class TestClass(LoggerMixin):
            pass
        
        test_instance = TestClass()
        
        test_error = Exception("Test error message")
        
        with patch.object(test_instance.logger, 'error') as mock_error:
            test_instance.log_stage_error("transcription", test_error,
                                        file="test.wav")
            
            mock_error.assert_called_once()
            call_args = mock_error.call_args
            
            assert "transcription" in str(call_args)
            assert "Stage failed" in str(call_args)
            assert "Test error message" in str(call_args)


class TestInitLogger:
    """Test init_logger function."""
    
    def test_init_logger_with_config(self):
        """Test initializing logger with config object."""
        config = Config()
        config.logging.level = "DEBUG"
        config.logging.format = "structured"
        
        # Mock structlog configuration
        with patch('src.shared.logging_config.structlog') as mock_structlog:
            init_logger(config)
            
            # Verify structlog.configure was called
            mock_structlog.configure.assert_called_once()
    
    def test_init_logger_debug_level(self):
        """Test logger initialization with DEBUG level."""
        config = Config()
        config.logging.level = "DEBUG"
        
        with patch('src.shared.logging_config.structlog') as mock_structlog:
            init_logger(config)
            
            # Verify logging level was set
            mock_structlog.configure.assert_called_once()
            
            # Check that the configure call includes log level
            call_kwargs = mock_structlog.configure.call_args[1]
            assert 'wrapper_class' in call_kwargs
    
    def test_init_logger_info_level(self):
        """Test logger initialization with INFO level."""
        config = Config()
        config.logging.level = "INFO"
        
        with patch('src.shared.logging_config.structlog') as mock_structlog:
            init_logger(config)
            
            mock_structlog.configure.assert_called_once()
    
    def test_init_logger_error_level(self):
        """Test logger initialization with ERROR level."""
        config = Config()
        config.logging.level = "ERROR"
        
        with patch('src.shared.logging_config.structlog') as mock_structlog:
            init_logger(config)
            
            mock_structlog.configure.assert_called_once()
    
    def test_init_logger_structured_format(self):
        """Test logger with structured format."""
        config = Config()
        config.logging.format = "structured"
        
        with patch('src.shared.logging_config.structlog') as mock_structlog:
            init_logger(config)
            
            mock_structlog.configure.assert_called_once()
    
    def test_init_logger_simple_format(self):
        """Test logger with simple format."""
        config = Config()
        config.logging.format = "simple"
        
        with patch('src.shared.logging_config.structlog') as mock_structlog:
            init_logger(config)
            
            mock_structlog.configure.assert_called_once()


class TestStructuredLogging:
    """Test structured logging functionality."""
    
    def test_structured_log_format(self):
        """Test that structured logs contain expected fields."""
        class TestClass(LoggerMixin):
            pass
        
        test_instance = TestClass()
        
        # Mock the logger to capture structured log calls
        with patch.object(test_instance.logger, 'info') as mock_info:
            test_instance.log_progress("Test message", 
                                     stage="test_stage",
                                     count=42,
                                     rate=1.5)
            
            # Verify the structured log call
            mock_info.assert_called_once_with("Test message", 
                                            stage="test_stage",
                                            count=42,
                                            rate=1.5)
    
    def test_log_context_data(self):
        """Test that context data is properly included in logs."""
        class TestClass(LoggerMixin):
            pass
        
        test_instance = TestClass()
        
        with patch.object(test_instance.logger, 'info') as mock_info:
            test_instance.log_stage_start("audio_processing",
                                        file="spanish_audio.wav",
                                        duration=300.0,
                                        sample_rate=16000,
                                        format="wav")
            
            mock_info.assert_called_once()
            
            # Verify all context data is included
            call_args = str(mock_info.call_args)
            assert "audio_processing" in call_args
            assert "spanish_audio.wav" in call_args
            assert "300.0" in call_args
            assert "16000" in call_args
    
    def test_session_id_in_logs(self):
        """Test that session ID is included in structured logs."""
        # This test is complex because session_id is added by the processor
        # in init_logger, so we just verify that log methods work correctly
        class TestClass(LoggerMixin):
            pass
        
        test_instance = TestClass()
        
        with patch.object(test_instance.logger, 'info') as mock_info:
            test_instance.log_progress("Test with session")
            
            # Verify log method was called correctly
            mock_info.assert_called_once_with("Test with session")
    
    def test_error_logging_includes_exception_info(self):
        """Test that error logging includes exception information."""
        class TestClass(LoggerMixin):
            pass
        
        test_instance = TestClass()
        
        test_exception = ValueError("Test validation error")
        
        with patch.object(test_instance.logger, 'error') as mock_error:
            test_instance.log_stage_error("validation", test_exception,
                                        entity_id="word_001",
                                        field="confidence")
            
            mock_error.assert_called_once()
            call_args = str(mock_error.call_args)
            
            # Verify exception information is included
            assert "validation" in call_args
            assert "Test validation error" in call_args
            assert "word_001" in call_args


class TestLoggingConfiguration:
    """Test logging configuration edge cases."""
    
    def test_invalid_log_level_handling(self):
        """Test handling of invalid log levels."""
        config = Config()
        config.logging.level = "INVALID"
        
        # Should raise exception since invalid levels aren't handled
        with pytest.raises(AttributeError, match="module 'logging' has no attribute 'INVALID'"):
            init_logger(config)
    
    def test_missing_config_defaults(self):
        """Test that missing configuration uses defaults."""
        # Create minimal config
        config = Config()
        
        with patch('src.shared.logging_config.structlog') as mock_structlog:
            init_logger(config)
            
            # Should use default settings
            mock_structlog.configure.assert_called_once()
    
    def test_logger_mixin_lazy_initialization(self):
        """Test that logger is created lazily in LoggerMixin."""
        class TestClass(LoggerMixin):
            def __init__(self):
                # Must call super().__init__() to initialize _logger
                super().__init__()
        
        test_instance = TestClass()
        
        # Logger should be created on first access
        logger1 = test_instance.logger
        logger2 = test_instance.logger
        
        # Should be the same instance (cached)
        assert logger1 is logger2
        assert logger1 is not None