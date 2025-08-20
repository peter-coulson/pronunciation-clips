# HANDOFF-1: Foundation to ML Implementation Handoff

## Overview
Session 1 completed the diarization foundation implementation. This handoff document provides Session 2 with the established interfaces, patterns, and integration points needed for ML diarization implementation.

## 1. Foundation Components Implemented

### 1.1 Data Models
**Location**: `src/shared/models.py`

```python
# Core diarization models - IMPLEMENTED AND TESTED
from src.shared.models import SpeakerSegment, DiarizationResult

class SpeakerSegment(BaseModel):
    """Represents a continuous speech segment by one speaker."""
    speaker_id: int = Field(..., ge=0, description="Speaker identifier (0, 1, 2, ...)")
    start_time: float = Field(..., ge=0.0, description="Segment start in seconds")
    end_time: float = Field(..., description="Segment end in seconds")
    confidence: float = Field(..., gt=0.0, le=1.0, description="Diarization confidence")

class DiarizationResult(BaseModel):
    """Complete result from speaker diarization process."""
    speakers: List[int] = Field(..., description="List of detected speaker IDs")
    segments: List[SpeakerSegment] = Field(..., description="All speaker segments")
    audio_duration: float = Field(..., ge=0.0, description="Total audio duration")
    processing_time: float = Field(..., ge=0.0, description="Processing time in seconds")
```

**Key Validation Rules**:
- `end_time > start_time` for all segments
- `confidence > 0.0 and <= 1.0` 
- No overlapping segments (automatic validation)
- Speaker IDs are non-negative integers starting from 0

### 1.2 Configuration System
**Location**: `src/shared/config.py`

```python
# Configuration integration - IMPLEMENTED AND TESTED
from src.shared.config import DiarizationConfig, SpeakersConfig

class DiarizationConfig(BaseModel):
    """Diarization-specific configuration."""
    model: str = Field(default="pyannote/speaker-diarization")
    min_speakers: int = Field(default=1, ge=1)
    max_speakers: int = Field(default=10, ge=1, le=50)
    segmentation_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    clustering_threshold: float = Field(default=0.7, ge=0.0, le=1.0)

class SpeakersConfig(BaseModel):
    """Speaker identification configuration - EXTENDED."""
    enable_diarization: bool = Field(default=False)
    diarization: Optional[DiarizationConfig] = Field(default=None)
    # ... existing fields remain
```

**Configuration Loading Pattern**:
```python
from src.shared.config import load_config

config = load_config("config.yaml")
if config.speakers.enable_diarization:
    diarization_config = config.speakers.diarization or DiarizationConfig()
    # Use diarization_config for ML setup
```

### 1.3 Entity Model Migration
**Location**: `src/shared/models.py`

```python
# Entity model updated - BREAKING CHANGE COMPLETED
class Entity(BaseModel):
    # CHANGED: speaker_id is now int instead of str
    speaker_id: int = Field(..., ge=0, description="Speaker identifier (0, 1, 2, ...)")
    # ... all other fields unchanged
```

**Database Integration**:
```python
# WordDatabase speaker_map now uses integer keys
class WordDatabase(BaseModel):
    speaker_map: Dict[int, SpeakerInfo] = Field(..., description="Speaker ID to info mapping")
    # ... other fields unchanged
```

## 2. ML Module Implementation Requirements

### 2.1 Recommended Module Structure
**Target Location**: `src/audio_to_json/diarization.py`

```python
"""
ML diarization module - TO BE IMPLEMENTED IN SESSION 2

Integrates with PyAnnote for speaker diarization using the foundation
interfaces established in Session 1.
"""
from typing import Optional, Tuple
import numpy as np

from ..shared.models import DiarizationResult, SpeakerSegment
from ..shared.config import DiarizationConfig
from ..shared.exceptions import PipelineError
from ..shared.logging_config import LoggerMixin

class DiarizationProcessor(LoggerMixin):
    """Handles ML-based speaker diarization using PyAnnote."""
    
    def __init__(self, config: DiarizationConfig):
        super().__init__()
        self.config = config
        self.model = None  # To be loaded in _load_model()
        
    def process_audio(self, audio_path: str, audio_duration: float) -> DiarizationResult:
        """
        Process audio file for speaker diarization.
        
        Args:
            audio_path: Path to input audio file
            audio_duration: Duration of audio in seconds
            
        Returns:
            DiarizationResult with speakers and segments
            
        Raises:
            PipelineError: If diarization processing fails
        """
        # Implementation needed in Session 2
        pass
        
    def _load_model(self) -> None:
        """Load PyAnnote diarization model."""
        # Implementation needed in Session 2
        pass
        
    def _extract_segments(self, diarization_output) -> List[SpeakerSegment]:
        """Convert PyAnnote output to SpeakerSegment objects."""
        # Implementation needed in Session 2
        pass

# Convenience function for pipeline integration
def process_diarization(audio_path: str, 
                       audio_duration: float,
                       config: Optional[DiarizationConfig] = None) -> DiarizationResult:
    """
    Convenience function for diarization processing.
    
    Args:
        audio_path: Path to audio file
        audio_duration: Audio duration in seconds
        config: Diarization configuration (uses defaults if None)
        
    Returns:
        DiarizationResult object
    """
    if config is None:
        config = DiarizationConfig()
    
    processor = DiarizationProcessor(config)
    return processor.process_audio(audio_path, audio_duration)
```

### 2.2 Pipeline Integration Points
**Location**: `src/audio_to_json/pipeline.py`

The pipeline already has placeholder methods that need ML implementation:

```python
class AudioToJsonPipeline:
    def process_diarization(self, audio_path: str) -> DiarizationResult:
        """
        NEEDS IMPLEMENTATION: Process audio file for speaker diarization only.
        
        Expected implementation pattern:
        1. Check if diarization is enabled in config
        2. Load/validate audio file
        3. Call diarization.process_diarization()
        4. Return DiarizationResult
        """
        pass
    
    def process(self, audio_path: str) -> List[Entity]:
        """
        NEEDS ENHANCEMENT: Add diarization to main pipeline.
        
        Expected integration points:
        1. After transcribe_audio() - get DiarizationResult
        2. During create_entities() - assign speaker_ids from diarization
        3. Update speaker mapping in create_database()
        """
        pass
```

## 3. Error Handling Patterns

### 3.1 Graceful Degradation Strategy
**Pattern Established**: Always provide fallback to single-speaker mode

```python
# Pattern to follow in ML implementation
try:
    # Attempt ML diarization
    result = process_diarization(audio_path, duration, config)
    if len(result.speakers) == 0:
        # Fallback: create single speaker result
        result = create_single_speaker_fallback(duration)
except Exception as e:
    self.logger.warning("Diarization failed, using single speaker", error=str(e))
    result = create_single_speaker_fallback(duration)

def create_single_speaker_fallback(duration: float) -> DiarizationResult:
    """Create fallback result for single speaker."""
    return DiarizationResult(
        speakers=[0],
        segments=[SpeakerSegment(
            speaker_id=0,
            start_time=0.0,
            end_time=duration,
            confidence=1.0
        )],
        audio_duration=duration,
        processing_time=0.0
    )
```

### 3.2 Dependency Management
**Required Dependencies** (to be added to requirements):
```
pyannote.audio>=3.0.0
torch>=2.0.0
# May require HuggingFace authentication
```

**Import Protection Pattern**:
```python
# Use this pattern for optional ML dependencies
try:
    from pyannote.audio import Pipeline
    PYANNOTE_AVAILABLE = True
except ImportError:
    PYANNOTE_AVAILABLE = False
    Pipeline = None

def _load_model(self):
    if not PYANNOTE_AVAILABLE:
        raise PipelineError(
            "PyAnnote not available. Install with: pip install pyannote.audio"
        )
    # Proceed with model loading
```

## 4. Configuration Integration Examples

### 4.1 Environment Variable Support
**Already Implemented**: Environment variables work through existing config system

```bash
# Enable diarization via environment variable
export PRONUNCIATION_CLIPS_SPEAKERS_ENABLE_DIARIZATION=true
```

### 4.2 YAML Configuration Example
```yaml
# config.yaml - diarization configuration
speakers:
  enable_diarization: true
  diarization:
    model: "pyannote/speaker-diarization-3.1"
    min_speakers: 1
    max_speakers: 5
    segmentation_threshold: 0.6
    clustering_threshold: 0.8
```

### 4.3 Configuration Loading in ML Module
```python
def __init__(self, config: DiarizationConfig):
    super().__init__()
    self.config = config
    
    # Log configuration for debugging
    self.logger.info("Initializing diarization", 
                    model=config.model,
                    min_speakers=config.min_speakers,
                    max_speakers=config.max_speakers)
```

## 5. Performance & Quality Requirements

### 5.1 Performance Benchmarks
From E2E test specifications (Session 2 targets):
- **Processing Speed**: 2-4x realtime for 10min audio
- **Memory Usage**: <2GB for 10min audio
- **No Regression**: When diarization disabled, no performance impact

### 5.2 Quality Thresholds
Expected ML output quality:
- **Confidence Scores**: >0.0, typically 0.79-0.95 range
- **Speaker Balance**: Max speaker <80% for multi-speaker audio
- **Temporal Accuracy**: Segments should align with actual speaker changes
- **Coverage**: Segments should cover full audio duration with minimal gaps

### 5.3 Validation Requirements
```python
def validate_diarization_result(result: DiarizationResult, 
                               expected_duration: float) -> bool:
    """Validate ML diarization output meets quality standards."""
    
    # Check basic structure
    if not result.speakers or not result.segments:
        return False
    
    # Check duration coverage
    total_coverage = sum(seg.end_time - seg.start_time for seg in result.segments)
    coverage_ratio = total_coverage / expected_duration
    if coverage_ratio < 0.8:  # At least 80% coverage
        return False
    
    # Check confidence scores
    if any(seg.confidence <= 0.0 for seg in result.segments):
        return False
    
    return True
```

## 6. Testing Integration Points

### 6.1 Unit Test Patterns
**Location**: `tests/unit/test_diarization.py` (to be created)

```python
# Expected test structure for Session 2
class TestDiarizationProcessor:
    def test_process_audio_basic(self):
        """Test basic diarization processing."""
        pass
    
    def test_process_audio_single_speaker(self):
        """Test single speaker detection."""
        pass
    
    def test_process_audio_multi_speaker(self):
        """Test multi-speaker detection."""
        pass
    
    def test_model_loading_failure(self):
        """Test graceful handling of model loading failures."""
        pass
```

### 6.2 E2E Test Compatibility
**Location**: `tests/e2e/test_diarization_e2e.py` (already exists)

The E2E tests expect these methods to be implemented:
- `AudioToJsonPipeline.process_diarization()`
- `AudioToJsonPipeline.assign_speaker_names()`
- Integration with main `process()` method

## 7. Logging & Observability Patterns

### 7.1 Structured Logging Requirements
```python
# Follow established logging patterns
class DiarizationProcessor(LoggerMixin):
    def process_audio(self, audio_path: str, audio_duration: float):
        self.log_stage_start("diarization", 
                           audio_path=audio_path,
                           duration=audio_duration)
        
        start_time = time.time()
        try:
            # ML processing
            result = self._perform_diarization(audio_path)
            
            self.log_stage_complete("diarization",
                                  speakers_detected=len(result.speakers),
                                  segments_created=len(result.segments),
                                  processing_time=time.time() - start_time)
            return result
            
        except Exception as e:
            self.log_stage_error("diarization", e)
            raise
```

### 7.2 Performance Metrics
```python
# Expected metrics to track in ML implementation
self.logger.info("Diarization performance",
                duration=audio_duration,
                processing_time=processing_time,
                realtime_factor=audio_duration / processing_time,
                speakers_detected=len(speakers),
                segments_per_minute=len(segments) / (audio_duration / 60),
                avg_confidence=sum(s.confidence for s in segments) / len(segments))
```

## 8. Integration Workflow for Session 2

### 8.1 Implementation Order
1. **Create diarization module** (`src/audio_to_json/diarization.py`)
2. **Implement PyAnnote integration** with dependency protection
3. **Add pipeline integration** in `AudioToJsonPipeline`
4. **Implement fallback mechanisms** for error handling
5. **Add comprehensive unit tests**
6. **Validate E2E test compatibility**

### 8.2 Validation Checklist
- [ ] DiarizationProcessor returns valid DiarizationResult objects
- [ ] Configuration integration works end-to-end
- [ ] Graceful fallback to single speaker mode
- [ ] Error handling follows established patterns
- [ ] Logging provides appropriate observability
- [ ] Performance meets benchmark requirements
- [ ] E2E tests pass with ML implementation

## 9. Critical Foundation Interfaces

### 9.1 Import Statements for Session 2
```python
# Core models (ready to use)
from src.shared.models import SpeakerSegment, DiarizationResult, Entity

# Configuration (ready to use)
from src.shared.config import DiarizationConfig, SpeakersConfig, load_config

# Logging and exceptions (follow these patterns)
from src.shared.logging_config import LoggerMixin
from src.shared.exceptions import PipelineError

# Entity creation integration (already supports integer speaker_ids)
from src.audio_to_json.entity_creation import EntityCreator
```

### 9.2 Speaker ID Assignment Pattern
```python
# Established pattern for entity creation with diarization
def assign_speakers_to_entities(entities: List[Entity], 
                               diarization_result: DiarizationResult) -> List[Entity]:
    """Assign speaker IDs from diarization to entities."""
    for entity in entities:
        word_center = (entity.start_time + entity.end_time) / 2
        
        # Find matching segment
        for segment in diarization_result.segments:
            if segment.start_time <= word_center <= segment.end_time:
                entity.speaker_id = segment.speaker_id
                break
        else:
            # Fallback to speaker 0 if no segment found
            entity.speaker_id = 0
    
    return entities
```

---

## Session 2 Success Criteria

### Must Implement
1. **Working DiarizationProcessor** with PyAnnote integration
2. **Pipeline integration** for `process_diarization()` method
3. **Error handling** with graceful fallback
4. **Configuration integration** end-to-end

### Must Pass
1. **E2E diarization tests** (basic structure already exists)
2. **Unit tests** for ML diarization components
3. **Integration tests** with pipeline
4. **Performance benchmarks** within specifications

The foundation provides complete type safety, validation, and integration points. Session 2 can focus entirely on ML implementation without concerns about data structure compatibility or configuration management.