# HANDOFF-0: E2E Test Analysis & Session 1 Foundation Requirements

## Overview
Session 0 completed comprehensive E2E test implementation for the diarization system. This handoff document extracts the critical interface contracts, data structures, and integration requirements needed for Session 1 foundation implementation.

## 1. Interface Contracts Discovered

### 1.1 AudioToJsonPipeline Interface Extensions
**Current State**: `AudioToJsonPipeline` exists but lacks diarization methods  
**Required Methods**:

```python
class AudioToJsonPipeline:
    def process_diarization(self, audio_path: str) -> DiarizationResult:
        """
        Process audio file for speaker diarization only.
        
        Args:
            audio_path: Path to input audio file
            
        Returns:
            DiarizationResult with speakers and segments
            
        Success Criteria:
        - Detect 2+ speakers in multi-speaker audio
        - Return valid speaker segments with timestamps
        - Handle single-speaker gracefully (return 1 speaker)
        - Confidence scores > 0.0 and <= 1.0
        - No overlapping segments
        """
    
    def process(self, audio_path: str) -> List[Entity]:
        """
        Process audio through complete pipeline including diarization.
        
        Args:
            audio_path: Path to input audio file
            
        Returns:
            List of Entity objects with speaker_id assigned
            
        Success Criteria:
        - All entities have valid integer speaker_ids
        - Multi-speaker distribution (max speaker < 80%)
        - Single speaker gets all entities with speaker_id=0
        - Backward compatibility when diarization disabled
        """
    
    def assign_speaker_names(self, entities: List[Entity], 
                           speaker_names: Dict[int, str]) -> Dict[str, Any]:
        """
        Apply human-readable names to speaker IDs.
        
        Args:
            entities: List of processed entities
            speaker_names: Mapping of speaker_id to human name
            
        Returns:
            Dict with 'entities' and 'speaker_map' keys
            
        Success Criteria:
        - Speaker map updated with human-readable names
        - Entity speaker_ids remain unchanged
        - Database format maintained
        """
```

### 1.2 Configuration Interface Requirements
**Current State**: `SpeakersConfig` exists but needs diarization support  
**Required Extensions**:

```python
class DiarizationConfig(BaseModel):
    """Diarization-specific configuration."""
    model: str = Field(default="pyannote/speaker-diarization")
    min_speakers: int = Field(default=1, ge=1)
    max_speakers: int = Field(default=10, ge=1, le=50)
    segmentation_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    clustering_threshold: float = Field(default=0.7, ge=0.0, le=1.0)

class SpeakersConfig(BaseModel):
    """Speaker identification configuration - EXTEND EXISTING."""
    enable_diarization: bool = Field(default=False)
    diarization: Optional[DiarizationConfig] = Field(default=None)
    # ... existing fields remain
```

## 2. Data Structures Required

### 2.1 Core Diarization Models
**Priority**: CRITICAL - Required for E2E test success

```python
class SpeakerSegment(BaseModel):
    """Represents a continuous speech segment by one speaker."""
    speaker_id: int = Field(..., ge=0, description="Speaker identifier (0, 1, 2, ...)")
    start_time: float = Field(..., ge=0.0, description="Segment start in seconds")
    end_time: float = Field(..., description="Segment end in seconds")
    confidence: float = Field(..., gt=0.0, le=1.0, description="Diarization confidence")
    
    @field_validator('end_time')
    @classmethod
    def end_after_start(cls, v, info):
        if hasattr(info, 'data') and 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time must be greater than start_time')
        return v

class DiarizationResult(BaseModel):
    """Complete result from speaker diarization process."""
    speakers: List[int] = Field(..., description="List of detected speaker IDs")
    segments: List[SpeakerSegment] = Field(..., description="All speaker segments")
    audio_duration: float = Field(..., ge=0.0, description="Total audio duration")
    processing_time: float = Field(..., ge=0.0, description="Processing time in seconds")
    
    @field_validator('segments')
    @classmethod
    def no_overlapping_segments(cls, segments):
        """Validate no overlapping segments."""
        sorted_segments = sorted(segments, key=lambda x: x.start_time)
        for i in range(len(sorted_segments) - 1):
            if sorted_segments[i].end_time > sorted_segments[i + 1].start_time:
                raise ValueError('Segments must not overlap')
        return segments
```

### 2.2 Entity Model Extension
**Current State**: `Entity.speaker_id` is `str`, needs to support `int`  
**Required Change**:

```python
class Entity(BaseModel):
    # Change from:
    # speaker_id: str = Field(..., description="Speaker identifier")
    # To:
    speaker_id: int = Field(..., ge=0, description="Speaker identifier (0, 1, 2, ...)")
    # ... all other fields remain unchanged
```

## 3. Integration Points & Dependencies

### 3.1 ML Dependencies
**PyAnnote Integration**:
- Model: `"pyannote/speaker-diarization"`
- Required packages: `pyannote.audio`, `torch`
- HuggingFace authentication may be required
- Graceful fallback when dependencies missing

### 3.2 Configuration Integration
**File**: `src/shared/config.py`
- Extend `SpeakersConfig` with `DiarizationConfig`
- Add validation for diarization parameters
- Environment variable support: `PRONUNCIATION_CLIPS_SPEAKERS_ENABLE_DIARIZATION`

### 3.3 Pipeline Integration Points
**File**: `src/audio_to_json/pipeline.py`
- Integration with existing `transcribe_audio()` workflow
- Speaker assignment during `create_entities()` phase
- Database writing with speaker information

### 3.4 Error Handling Requirements
**Graceful Degradation**:
- Missing ML dependencies → Fall back to single speaker mode
- Model loading failures → Log warning, use speaker_id=0
- Audio processing errors → Clear error messages
- Invalid configuration → Validation errors with helpful messages

## 4. Performance & Quality Requirements

### 4.1 Performance Benchmarks
From E2E test specifications:
- Processing speed: 2-4x realtime
- Memory usage: <2GB for 10min audio
- No performance regression when disabled

### 4.2 Quality Thresholds
From fixture expectations:
- Confidence scores: >0.0 (typically 0.79-0.95)
- Speaker balance: Max speaker <80% for multi-speaker
- Temporal accuracy: Segments align with audio boundaries
- Coverage: Segments cover full audio duration

## 5. Session 1 Success Criteria

### 5.1 Core Implementation Goals
1. **SpeakerSegment & DiarizationResult models** - Pass model validation tests
2. **DiarizationConfig integration** - Configuration loading with diarization enabled
3. **Entity.speaker_id conversion** - Change from str to int, update all references
4. **AudioToJsonPipeline.process_diarization()** - Return valid DiarizationResult
5. **Basic single-speaker fallback** - Handle diarization disabled case

### 5.2 E2E Test Milestones
**Must Pass After Session 1**:
- `test_diarization_disabled_compatibility_e2e` - Backward compatibility
- Basic structure tests for `process_diarization()` method existence

**Defer to Later Sessions**:
- Full multi-speaker detection (requires ML integration)
- Speaker naming functionality
- Performance optimization

### 5.3 Integration Validation
- Configuration loads successfully with diarization enabled
- Pipeline instantiates without errors
- Entity model accepts integer speaker_ids
- Database format maintains compatibility

## 6. Context for Session 1

### 6.1 Critical Files to Modify
1. `src/shared/models.py` - Add SpeakerSegment, DiarizationResult
2. `src/shared/config.py` - Add DiarizationConfig, extend SpeakersConfig  
3. `src/audio_to_json/pipeline.py` - Add diarization methods
4. Update all Entity creation to use integer speaker_ids

### 6.2 Test Strategy
- Start with disabled diarization test (easiest to pass)
- Implement basic method signatures to satisfy interface contracts
- Add model validation tests for new data structures
- Ensure backward compatibility throughout

### 6.3 Architecture Decisions
- Speaker IDs are integers starting from 0
- Single speaker always gets speaker_id=0
- Diarization is optional/disabled by default
- Configuration uses nested structure for diarization settings

## 7. Risk Mitigation

### 7.1 Breaking Changes
**Entity.speaker_id type change**: Review all code that creates or processes entities
**Pipeline method additions**: Ensure new methods don't conflict with existing workflow

### 7.2 Dependency Management
**ML libraries**: Implement optional imports with graceful fallback
**Configuration validation**: Clear error messages for invalid diarization settings

### 7.3 Testing Strategy
**Incremental validation**: Start with structure tests before ML integration
**Backward compatibility**: Ensure existing functionality unaffected

---

## Session 1 Next Actions
1. Implement core data models (SpeakerSegment, DiarizationResult)
2. Extend configuration system for diarization
3. Add basic pipeline method signatures
4. Convert Entity.speaker_id to integer type
5. Validate E2E test compatibility with new structures