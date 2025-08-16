"""
Exception hierarchy for the pronunciation clips pipeline.

Provides a structured exception hierarchy with clear inheritance and helpful context.
"""


class PipelineError(Exception):
    """Base exception for all pipeline errors."""
    
    def __init__(self, message: str, context: dict = None):
        super().__init__(message)
        self.context = context or {}
        
    def __str__(self):
        base_msg = super().__str__()
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{base_msg} (Context: {context_str})"
        return base_msg


class ConfigError(PipelineError):
    """Raised when configuration loading or validation fails."""
    pass


class AudioError(PipelineError):
    """Raised when audio processing fails."""
    pass


class TranscriptionError(PipelineError):
    """Raised when transcription processing fails."""
    pass


class EntityError(PipelineError):
    """Raised when entity creation or validation fails."""
    pass


class DatabaseError(PipelineError):
    """Raised when database operations fail."""
    pass


class SpeakerError(PipelineError):
    """Raised when speaker identification fails."""
    pass