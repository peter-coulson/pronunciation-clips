# Stage 2: Audio Processing

## Deliverables
- `audio_to_json/audio_processor.py` - Audio loading, validation, and format handling

## Implementation Status
✅ **IMPLEMENTED** - Audio processing module complete

## Success Criteria

### End-to-End Tests (ALL MUST PASS)
1. **Valid Audio Processing**
   - Load 16kHz WAV file and extract correct metadata
   - Load 44.1kHz WAV file and resample to 16kHz
   - Extract duration, sample rate, channel count accurately

2. **Audio Format Validation**
   - Reject non-existent file with AudioError
   - Reject unsupported format (e.g., PDF) with AudioError
   - Reject corrupted audio file with clear error

3. **Audio Metadata Accuracy**
   - Process 30-second Spanish audio file
   - Verify duration within 0.1 seconds of actual
   - Verify sample rate conversion works correctly

## Required Test Audio Files
- `fixtures/spanish_30sec_16khz.wav` - Clear 16kHz baseline
- `fixtures/spanish_30sec_44khz.wav` - High sample rate for resampling test
- `fixtures/corrupted.wav` - Invalid audio file for error handling

## Architecture Implementation
- **Format support**: WAV, MP3, M4A, FLAC input formats
- **Automatic resampling**: Convert all audio to 16kHz for Whisper
- **Metadata extraction**: Duration, sample rate, channels, file size
- **Validation**: File existence, format support, corruption detection
- **Error handling**: Specific AudioError exceptions with context

## Testing Commands
```bash
./pytest_venv.sh tests/integration/test_stage2_audio.py -v
```

## Git Commit Pattern
```
Stage 2: Audio processing complete

- Audio loading and validation working
- Format conversion (44.1kHz → 16kHz) working
- Metadata extraction accurate
- Error handling for invalid files
- All unit, integration, and E2E tests passing
```