# Speaker Diarization Implementation Specification

## Overview

This document outlines the implementation of automated speaker diarization to replace the current manual speaker assignment system. The goal is to automatically detect speaker changes in audio and assign speaker IDs, with post-processing capabilities for speaker naming.

## Current System Analysis

### Current Architecture (Stage 7 - Manual Assignment)

**Current Flow:**
```
Audio → Transcription → Entity Creation (all speaker_id: 0) → Manual Assignment → Database
```

**Current Code:**
- `src/audio_to_json/speaker_identification.py` - Manual time-range mapping (154 lines)
- `src/audio_to_json/entity_creation.py:_get_speaker_id()` - Simple default assignment
- All entities assigned `speaker_id: "speaker_0"` by default

**Current Problems:**
1. No automatic speaker detection
2. Manual time-range input is impractical
3. String-based speaker IDs inefficient (`"speaker_0"` vs `0`)
4. Over-engineered manual mapping system

**Current E2E Test Results:**
- ✅ Juan Gabriel Vásquez (Spanish): 409 entities, 1 speaker detected
- ✅ Hotz/Fridman (English): 526 entities, 1 speaker detected (74.1% zero-gap = conversational)

## Target Architecture (ML-Based Diarization)

### Target Flow:
```
Audio → Transcription → ML Diarization → Entity Assignment → Speaker Labeling → Database
```

### New Components:

#### 1. **ML Diarization Stage** (New)
- **Purpose**: Automatically detect speaker changes using ML models
- **Input**: Processed audio + word timestamps  
- **Output**: Speaker segments `[(start_time, end_time, speaker_id), ...]`
- **Technology**: pyannote-audio or resemblyzer

#### 2. **Enhanced Entity Assignment** (Modified)
- **Purpose**: Assign detected speaker IDs to word entities
- **Input**: Word entities + speaker segments
- **Output**: Entities with correct numeric speaker IDs

#### 3. **Speaker Labeling** (New CLI Command)
- **Purpose**: Post-processing to assign names to detected speakers
- **Input**: Database + name mappings
- **Output**: Updated speaker_map with human-readable names

## Detailed Implementation Specifications

### 1. Model Changes

#### Entity Model Updates
```python
# Current
speaker_id: str = Field(..., description="Speaker identifier")  # "speaker_0"

# Target  
speaker_id: int = Field(default=0, description="Speaker identifier")  # 0, 1, 2
```

#### New Speaker Segment Model
```python
@dataclass
class SpeakerSegment:
    """Represents a time segment with detected speaker."""
    start_time: float
    end_time: float  
    speaker_id: int
    confidence: float = 0.0  # Diarization confidence
```

### 2. Configuration Updates

#### Diarization Configuration
```yaml
# config.yaml additions
diarization:
  enabled: true
  model: "pyannote/speaker-diarization"  # HuggingFace model
  min_speakers: 1
  max_speakers: 10
  clustering_threshold: 0.7
  min_segment_duration: 1.0  # seconds
  use_auth_token: null  # for private models
```

### 3. New Diarization Module

#### `src/audio_to_json/diarization.py` (New File)
```python
class SpeakerDiarizer(LoggerMixin):
    """ML-based speaker diarization using pyannote."""
    
    def __init__(self, diarization_config: DiarizationConfig):
        self.config = diarization_config
        self._pipeline = None
    
    def diarize_audio(self, audio_path: str) -> List[SpeakerSegment]:
        """
        Perform speaker diarization on audio file.
        
        Returns:
            List of speaker segments with timing and speaker IDs
        """
        
    def _load_pipeline(self):
        """Lazy-load pyannote diarization pipeline."""
        
    def _convert_to_segments(self, diarization_result) -> List[SpeakerSegment]:
        """Convert pyannote output to our SpeakerSegment format."""
```

### 4. Enhanced Entity Creation

#### Modified `src/audio_to_json/entity_creation.py`
```python
class EntityCreator(LoggerMixin):
    def create_entities(self, 
                       words: List[Word], 
                       recording_id: str, 
                       recording_path: str,
                       speaker_segments: Optional[List[SpeakerSegment]] = None) -> List[Entity]:
        """
        Create entities with speaker assignment from diarization.
        
        Args:
            speaker_segments: ML-detected speaker segments (replaces manual mapping)
        """
        
    def _assign_speaker_id(self, start_time: float, end_time: float,
                          speaker_segments: List[SpeakerSegment]) -> int:
        """Assign speaker ID based on ML diarization segments."""
        if not speaker_segments:
            return 0  # Default single speaker
            
        word_center = (start_time + end_time) / 2
        for segment in speaker_segments:
            if segment.start_time <= word_center <= segment.end_time:
                return segment.speaker_id
        return 0  # Fallback
```

### 5. New CLI Commands

#### Speaker Labeling Command
```python
@cli.command()
@click.argument('database_file', type=click.Path(exists=True))
@click.option('--names', help='Speaker names: "0:Lex Fridman,1:George Hotz"')
@click.option('--mapping-file', type=click.Path(exists=True))
def label_speakers(database_file, names, mapping_file):
    """Assign human-readable names to detected speakers."""
```

#### Diarization Analysis Command
```python
@cli.command()
@click.argument('database_file', type=click.Path(exists=True))
def analyze_speakers(database_file):
    """Show speaker distribution and statistics."""
    # Output: Speaker 0: 245 words (46.6%), Speaker 1: 281 words (53.4%)
```

### 6. Pipeline Integration

#### Modified `src/audio_to_json/pipeline.py`
```python
class AudioToJsonPipeline(LoggerMixin):
    def process_audio_to_json(self, audio_path: str, ...) -> WordDatabase:
        # ... existing stages ...
        
        # New Stage 2.5: Speaker Diarization (optional)
        speaker_segments = None
        if self.config.diarization.enabled:
            self.log_progress("Starting Speaker Diarization")
            diarizer = SpeakerDiarizer(self.config.diarization)
            speaker_segments = diarizer.diarize_audio(audio_path)
            self.log_progress("Diarization complete", 
                            speakers_detected=len(set(s.speaker_id for s in speaker_segments)))
        
        # Modified Stage 3: Entity Creation (with speaker segments)
        entities = create_entities(words, recording_id, str(audio_file), 
                                 self.config.quality, speaker_segments)
```

## Dependencies and Installation

### New Requirements
```
# requirements.txt additions
pyannote.audio>=3.1.0
torch>=2.0.0
torchaudio>=2.0.0
huggingface_hub>=0.16.0
```

### Installation Setup
```python
# src/shared/dependencies.py (new file)
def check_diarization_dependencies():
    """Check if diarization dependencies are available."""
    try:
        import torch
        from pyannote.audio import Pipeline
        return True
    except ImportError as e:
        return False, str(e)
```

## E2E Test Specifications

### Test Suite: `tests/e2e/test_diarization_e2e.py`

#### Test 1: Basic Diarization Detection
```python
def test_diarization_basic_detection_e2e():
    """
    Test: Multi-speaker audio → Speaker segments detected
    
    Success Criteria:
    - Detect 2+ speakers in Hotz/Fridman conversation
    - Speaker segments have valid timestamps
    - Speaker IDs are integers (0, 1, 2...)
    - Segments cover full audio duration
    - No overlapping segments
    """
    config = load_config_with_diarization()
    segments = diarize_audio("tests/fixtures/hotz_fridman_conversation.wav", config)
    
    assert len(segments) > 1  # Multiple segments
    assert len(set(s.speaker_id for s in segments)) >= 2  # Multiple speakers
    
    for segment in segments:
        assert segment.start_time < segment.end_time
        assert isinstance(segment.speaker_id, int)
        assert segment.confidence > 0.0
```

#### Test 2: Entity Assignment Integration
```python
def test_diarization_entity_assignment_e2e():
    """
    Test: Audio → Diarization → Entity assignment → Correct speaker IDs
    
    Success Criteria:
    - Entities assigned to detected speakers (not all speaker_id: 0)
    - Speaker distribution roughly matches conversation pattern
    - All entities have valid integer speaker IDs
    - Speaker changes align with segment boundaries
    """
    database = process_audio_to_json("tests/fixtures/hotz_fridman_conversation.wav", 
                                   config_with_diarization)
    
    # Validate multiple speakers assigned
    speaker_ids = set(e.speaker_id for e in database.entities)
    assert len(speaker_ids) >= 2
    
    # Validate speaker distribution (not 100% single speaker)
    speaker_counts = {sid: len([e for e in database.entities if e.speaker_id == sid]) 
                     for sid in speaker_ids}
    max_speaker_percentage = max(speaker_counts.values()) / len(database.entities)
    assert max_speaker_percentage < 0.8  # No single speaker dominates too much
```

#### Test 3: Speaker Labeling Post-Processing
```python
def test_speaker_labeling_e2e():
    """
    Test: Detected speakers → Name assignment → Updated database
    
    Success Criteria:
    - Speaker names correctly assigned to IDs
    - Speaker map updated with human-readable names
    - Entity speaker_ids remain unchanged
    - Database format maintained
    """
    # Process with diarization
    database = process_audio_to_json(audio_file, config_with_diarization)
    
    # Apply speaker labels
    name_mapping = {0: "Lex Fridman", 1: "George Hotz"}
    updated_db = apply_speaker_labels(database, name_mapping)
    
    assert "Lex Fridman" in [info.name for info in updated_db.speaker_map.values()]
    assert "George Hotz" in [info.name for info in updated_db.speaker_map.values()]
```

#### Test 4: Single Speaker Fallback
```python
def test_single_speaker_fallback_e2e():
    """
    Test: Single-speaker audio → Graceful fallback → All entities speaker_id: 0
    
    Success Criteria:
    - Single speaker audio processed without errors
    - All entities assigned speaker_id: 0
    - No spurious speaker detection
    - Performance not degraded
    """
    database = process_audio_to_json("tests/fixtures/juan_gabriel_single_speaker.wav", 
                                   config_with_diarization)
    
    speaker_ids = set(e.speaker_id for e in database.entities)
    assert speaker_ids == {0}  # Only single speaker
```

#### Test 5: Diarization Disabled Mode
```python
def test_diarization_disabled_compatibility_e2e():
    """
    Test: Diarization disabled → Backward compatibility maintained
    
    Success Criteria:
    - Works exactly like current system when disabled
    - All entities get speaker_id: 0
    - No performance impact
    - No additional dependencies loaded
    """
    config_disabled = load_config()
    config_disabled.diarization.enabled = False
    
    database = process_audio_to_json(test_audio, config_disabled)
    assert all(e.speaker_id == 0 for e in database.entities)
```

### Test Fixtures Required

#### Multi-Speaker Test Audio
- **`tests/fixtures/hotz_fridman_conversation.wav`** (existing - 4min conversation)
- **`tests/fixtures/two_speaker_clear.wav`** (synthetic - clear speaker changes)
- **`tests/fixtures/three_speaker_meeting.wav`** (meeting with 3 participants)

#### Expected Outputs
- **`tests/fixtures/expected_diarization_segments.json`** (known-good diarization results)
- **`tests/fixtures/expected_speaker_distribution.json`** (expected entity counts per speaker)

## Performance Requirements

### Processing Speed Targets
- **Diarization**: 2-4x realtime (acceptable trade-off for accuracy)
- **Overall pipeline**: 8-12x realtime (down from current 14.9x due to diarization)
- **Memory usage**: <2GB for 10-minute audio files

### Accuracy Targets
- **Speaker detection**: >85% accuracy on clear conversational audio
- **Segment boundaries**: Within ±1 second of human annotation
- **False positive rate**: <10% spurious speaker detection

## Migration Strategy

### Phase 1: Implementation (Week 1)
1. Implement diarization module with pyannote integration
2. Modify entity creation to use speaker segments
3. Update models to use integer speaker IDs
4. Add configuration options

### Phase 2: CLI & Testing (Week 2)
1. Implement speaker labeling CLI command
2. Create comprehensive E2E test suite
3. Add dependency checking and error handling
4. Performance optimization

### Phase 3: Integration & Documentation (Week 3)
1. Update pipeline integration
2. Backward compatibility testing
3. Documentation and examples
4. Performance benchmarking

## Rollback Plan

If diarization proves problematic:
1. **Configuration flag**: `diarization.enabled: false` reverts to current behavior
2. **Graceful degradation**: Missing dependencies fall back to single speaker
3. **Model compatibility**: Integer speaker IDs work with existing system
4. **Minimal disruption**: Core transcription pipeline unchanged

## Success Metrics

### Technical Metrics
- [ ] E2E tests pass with >95% reliability
- [ ] Processing speed within 2-4x realtime
- [ ] Memory usage <2GB for 10min audio
- [ ] Speaker detection accuracy >85%

### User Experience Metrics
- [ ] Multi-speaker conversations properly segmented
- [ ] Speaker labeling workflow intuitive
- [ ] Backward compatibility maintained
- [ ] Clear error messages for setup issues

## Conclusion

This implementation transforms the pronunciation clip generator from a single-speaker system to a robust multi-speaker platform using industry-standard ML diarization, while maintaining simplicity through post-processing speaker labeling and full backward compatibility.