"""
Structured logging configuration using structlog.

Provides session-correlated logging with rich context for debugging and monitoring.
Supports both console and file output with structured JSON format.
"""
import logging
import sys
import uuid
from pathlib import Path
from typing import Optional

import structlog

from .config import Config


def init_logger(config: Config, session_id: Optional[str] = None) -> structlog.stdlib.BoundLogger:
    """
    Initialize structured logging with session correlation.
    
    Args:
        config: Configuration object with logging settings
        session_id: Optional session ID for correlation (generates UUID if None)
        
    Returns:
        Bound logger with session context
    """
    if session_id is None:
        session_id = str(uuid.uuid4())[:8]
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="ISO"),
            _add_session_id(session_id),
            structlog.dev.ConsoleRenderer() if config.logging.format == "simple" else structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        level=getattr(logging, config.logging.level),
        format="%(message)s",
        handlers=_create_handlers(config.logging)
    )
    
    # Create bound logger with session context
    logger = structlog.get_logger()
    logger = logger.bind(session_id=session_id)
    
    return logger


def _add_session_id(session_id: str):
    """Add session ID to all log entries."""
    def processor(logger, method_name, event_dict):
        event_dict["session_id"] = session_id
        return event_dict
    return processor


def _create_handlers(logging_config) -> list:
    """Create appropriate logging handlers based on configuration."""
    handlers = []
    
    # Console handler
    if logging_config.console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, logging_config.level))
        handlers.append(console_handler)
    
    # File handler
    if logging_config.file:
        file_path = Path(logging_config.file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setLevel(getattr(logging, logging_config.level))
        handlers.append(file_handler)
    
    return handlers


class LoggerMixin:
    """Mixin class to add logging capabilities to any class."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = None
    
    @property
    def logger(self) -> structlog.stdlib.BoundLogger:
        """Get or create a logger for this instance."""
        if self._logger is None:
            self._logger = structlog.get_logger(self.__class__.__name__)
        return self._logger
    
    def log_stage_start(self, stage: str, **context):
        """Log the start of a pipeline stage."""
        self.logger.info("Stage started", stage=stage, **context)
    
    def log_stage_complete(self, stage: str, **context):
        """Log the completion of a pipeline stage."""
        self.logger.info("Stage completed", stage=stage, **context)
    
    def log_stage_error(self, stage: str, error: Exception, **context):
        """Log an error in a pipeline stage."""
        self.logger.error("Stage failed", stage=stage, error=str(error), **context)
    
    def log_progress(self, message: str, **context):
        """Log progress information."""
        self.logger.info(message, **context)
    
    def log_metrics(self, **metrics):
        """Log metrics and performance data."""
        self.logger.info("Metrics", **metrics)