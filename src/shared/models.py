"""
Pydantic data models for type safety and validation.

Defines the core data structures used throughout the pipeline with proper validation,
serialization, and type safety. Designed for easy JSON serialization and pandas integration.
"""
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, field_validator


class Entity(BaseModel):
    """
    Represents a single word occurrence in the audio with all associated metadata.
    """
    # Core identification
    entity_id: str = Field(..., description="Unique identifier (e.g., 'word_001')")
    entity_type: str = Field(..., description="Type of entity: 'word', 'sentence', 'phrase'")
    text: str = Field(..., description="The actual text content")
    
    # Temporal information
    start_time: float = Field(..., ge=0.0, description="Start time in seconds")
    end_time: float = Field(..., ge=0.0, description="End time in seconds")
    duration: float = Field(..., ge=0.0, description="Duration in seconds")
    
    # Whisper outputs
    confidence: float = Field(..., ge=0.0, le=1.0, description="Whisper confidence score")
    probability: float = Field(..., ge=0.0, le=1.0, description="Whisper probability score")
    
    # Analysis fields
    syllables: List[str] = Field(default_factory=list, description="Syllable breakdown")
    syllable_count: int = Field(default=0, ge=0, description="Number of syllables")
    phonetic: Optional[str] = Field(default=None, description="Phonetic transcription")
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall quality score")
    
    # Speaker & context
    speaker_id: str = Field(..., description="Speaker identifier")
    recording_id: str = Field(..., description="Recording identifier")
    recording_path: str = Field(..., description="Path to original recording")
    
    # Processing status
    processed: bool = Field(default=False, description="Whether clip has been extracted")
    clip_path: Optional[str] = Field(default=None, description="Path to extracted clip")
    selection_reason: Optional[str] = Field(default=None, description="Reason for selection")
    created_at: str = Field(..., description="Creation timestamp (ISO format)")
    
    @field_validator('end_time')
    @classmethod
    def end_time_after_start(cls, v, info):
        """Ensure end_time is after start_time."""
        if hasattr(info, 'data') and 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time must be greater than start_time')
        return v
    
    @field_validator('duration')
    @classmethod
    def duration_matches_times(cls, v, info):
        """Ensure duration matches the time difference."""
        if hasattr(info, 'data') and 'start_time' in info.data and 'end_time' in info.data:
            expected_duration = info.data['end_time'] - info.data['start_time']
            if abs(v - expected_duration) > 0.001:  # 1ms tolerance
                raise ValueError(f'duration ({v}) must match end_time - start_time ({expected_duration})')
        return v
    
    @field_validator('entity_type')
    @classmethod
    def validate_entity_type(cls, v):
        """Validate entity type."""
        valid_types = ['word', 'sentence', 'phrase']
        if v not in valid_types:
            raise ValueError(f'entity_type must be one of {valid_types}')
        return v
    
    @field_validator('syllable_count')
    @classmethod
    def syllable_count_matches_syllables(cls, v, info):
        """Ensure syllable_count matches length of syllables list."""
        if hasattr(info, 'data') and 'syllables' in info.data and v != len(info.data['syllables']):
            raise ValueError('syllable_count must match length of syllables list')
        return v


class SpeakerInfo(BaseModel):
    """Information about a speaker."""
    name: str = Field(..., description="Speaker name")
    gender: str = Field(default="Unknown", description="Speaker gender")
    region: str = Field(default="Unknown", description="Speaker region/dialect")
    
    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        """Validate gender field."""
        valid_genders = ['M', 'F', 'Unknown']
        if v not in valid_genders:
            raise ValueError(f'gender must be one of {valid_genders}')
        return v


class AudioMetadata(BaseModel):
    """Metadata about processed audio files."""
    path: str = Field(..., description="Path to audio file")
    duration: float = Field(..., ge=0.0, description="Duration in seconds")
    sample_rate: int = Field(..., ge=1000, description="Sample rate in Hz")
    channels: int = Field(..., ge=1, le=2, description="Number of audio channels")
    format: str = Field(..., description="Audio format (e.g., 'wav', 'mp3')")
    size_bytes: int = Field(..., ge=0, description="File size in bytes")


class WordDatabase(BaseModel):
    """
    Complete database container for all entities and metadata.
    """
    metadata: Dict[str, Any] = Field(..., description="Database metadata")
    speaker_map: Dict[str, SpeakerInfo] = Field(..., description="Speaker ID to info mapping")
    entities: List[Entity] = Field(..., description="All word/sentence/phrase entities")
    
    @field_validator('metadata')
    @classmethod
    def validate_metadata(cls, v):
        """Ensure required metadata fields are present."""
        required_fields = ['version', 'created_at']
        for field in required_fields:
            if field not in v:
                raise ValueError(f'metadata must contain {field}')
        return v
    
    def get_entities_by_type(self, entity_type: str) -> List[Entity]:
        """Get all entities of a specific type."""
        return [e for e in self.entities if e.entity_type == entity_type]
    
    def get_entities_by_speaker(self, speaker_id: str) -> List[Entity]:
        """Get all entities for a specific speaker."""
        return [e for e in self.entities if e.speaker_id == speaker_id]
    
    def get_entities_by_confidence(self, min_confidence: float) -> List[Entity]:
        """Get all entities above a confidence threshold."""
        return [e for e in self.entities if e.confidence >= min_confidence]