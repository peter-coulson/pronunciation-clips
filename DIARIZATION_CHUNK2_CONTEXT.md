# DIARIZATION CHUNK 2 CONTEXT - Core ML Module

## Chunk Scope: ML Diarization Implementation Only
**Files**: `src/audio_to_json/diarization.py` (new file, ~120 lines)
**Token Budget**: ~2000 tokens
**Dependencies**: Chunk 1 (SpeakerSegment, DiarizationConfig) 

## Required Interfaces (from Chunk 1)
```python
@dataclass
class SpeakerSegment:
    start_time: float
    end_time: float  
    speaker_id: int
    confidence: float = 0.0

class DiarizationConfig:
    enabled: bool
    model: str = "pyannote/speaker-diarization"
    min_speakers: int = 1
    max_speakers: int = 10
    clustering_threshold: float = 0.7
    min_segment_duration: float = 1.0
    use_auth_token: Optional[str] = None
```

## Output Contracts (for Chunk 3+)
```python
class SpeakerDiarizer(LoggerMixin):
    def diarize_audio(self, audio_path: str) -> List[SpeakerSegment]:
        """Returns speaker segments with timing and IDs"""
        
def check_diarization_dependencies() -> Tuple[bool, Optional[str]]:
    """Returns (available, error_message)"""
```

## Implementation Requirements

### Core Class Structure
```python
from src.shared.logging_mixin import LoggerMixin
from typing import List, Optional, Tuple
import torch
from pyannote.audio import Pipeline

class SpeakerDiarizer(LoggerMixin):
    def __init__(self, config: DiarizationConfig):
        self.config = config
        self._pipeline = None
    
    def diarize_audio(self, audio_path: str) -> List[SpeakerSegment]:
        # Implementation here
        
    def _load_pipeline(self):
        # Lazy loading implementation
        
    def _convert_to_segments(self, diarization_result) -> List[SpeakerSegment]:
        # Convert pyannote format to SpeakerSegment
```

### Dependency Management
- Import pyannote.audio with try/catch
- Graceful fallback if ML dependencies missing
- Clear error messages for setup issues
- Lazy loading to avoid startup penalties

### Error Handling Patterns
- Missing dependency → clear installation message
- Audio file issues → specific file error
- Model loading failures → model setup guidance
- Processing errors → fallback to single speaker

### Performance Considerations
- Pipeline caching (don't reload per audio file)
- Memory management for large audio files
- Processing progress logging
- Reasonable timeout handling

## Testing Requirements
- Unit test: basic diarization with mock audio
- Unit test: dependency checking functionality  
- Unit test: error handling for missing files
- Unit test: segment format conversion accuracy

## Focus Areas
- **ML Integration**: Proper pyannote-audio usage
- **Error Handling**: Graceful failures with clear messages
- **Performance**: Efficient pipeline management
- **Format Conversion**: Accurate segment timing