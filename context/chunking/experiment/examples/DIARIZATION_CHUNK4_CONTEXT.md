# DIARIZATION CHUNK 4 CONTEXT - Pipeline Integration

## Chunk Scope: Pipeline Integration Only  
**Files**: `src/audio_to_json/pipeline.py` (modify existing)
**Token Budget**: ~2000 tokens
**Dependencies**: Chunks 1, 2, 3 (models, diarization module, entity integration)

## Required Interfaces (from previous chunks)
```python
# From Chunk 2
class SpeakerDiarizer:
    def diarize_audio(self, audio_path: str) -> List[SpeakerSegment]

# From Chunk 3  
def create_entities(words: List[Word], recording_id: str, recording_path: str,
                   quality_config, speaker_segments: Optional[List[SpeakerSegment]] = None) -> List[Entity]
```

## Current Pipeline Structure
**Existing Stages**:
1. Audio Processing → processed audio file
2. Transcription → List[Word] with timestamps
3. Entity Creation → List[Entity] with speaker_id: 0
4. Database Writing → WordDatabase

**Target Integration**: Add Stage 2.5 between Transcription and Entity Creation

## Integration Points

### Pipeline Method Modification
```python
class AudioToJsonPipeline(LoggerMixin):
    def process_audio_to_json(self, audio_path: str, ...) -> WordDatabase:
        # ... existing stages 1-2 ...
        
        # NEW Stage 2.5: Speaker Diarization (conditional)
        speaker_segments = None
        if self.config.diarization.enabled:
            self.log_progress("Starting Speaker Diarization")
            diarizer = SpeakerDiarizer(self.config.diarization)
            speaker_segments = diarizer.diarize_audio(audio_path)
            self.log_progress("Diarization complete", 
                            speakers_detected=len(set(s.speaker_id for s in speaker_segments)))
        
        # Modified Stage 3: Entity Creation (pass speaker_segments)
        entities = create_entities(words, recording_id, str(audio_file), 
                                 self.config.quality, speaker_segments)
        
        # ... existing stages 4+ ...
```

### Configuration Integration
- Access `self.config.diarization.enabled` flag
- Handle missing diarization config gracefully
- Pass diarization config to SpeakerDiarizer

### Error Handling Strategy
- Missing dependencies → log warning, continue without diarization
- Diarization failures → log error, fall back to speaker_segments=None
- Configuration errors → clear error messages
- No impact on existing pipeline stages

### Progress Logging Integration
- Follow existing logging patterns from pipeline
- Log diarization start/completion
- Include speaker count in progress messages
- Maintain consistent logging format

## Implementation Focus
- **Minimal Changes**: Only add Stage 2.5, don't modify other stages
- **Backward Compatibility**: Works with and without diarization enabled
- **Error Isolation**: Diarization failures don't break pipeline
- **Consistent Patterns**: Follow existing stage implementation patterns

## Testing Requirements
- Integration test: pipeline with diarization enabled
- Integration test: pipeline with diarization disabled  
- Integration test: diarization failure fallback
- Integration test: configuration edge cases

## Performance Considerations
- Stage timing logging (existing pattern)
- Memory management (don't hold large diarization data unnecessarily)
- Processing order optimization
- Progress reporting accuracy