# Key Interfaces & Contracts

## Core Pipeline Functions

### Audio Processing
```python
def process_audio(audio_path: str, config: AudioConfig) -> AudioMetadata:
    """Load and validate audio file with metadata extraction."""
```

### Transcription Engine  
```python
def transcribe_audio(audio_metadata: AudioMetadata, whisper_config: WhisperConfig) -> List[Word]:
    """Transcribe audio using Whisper with word timestamps."""
```

### Entity Creation
```python
def create_entities(words: List[Word], speaker_mapping: Optional[Dict], 
                   recording_id: str, recording_path: str, 
                   quality_config: QualityConfig) -> List[Entity]:
    """Convert Whisper words to typed entities."""

def apply_quality_filters(entities: List[Entity], config: QualityConfig) -> List[Entity]:
    """Filter entities by confidence, duration, syllable count."""
```

### Database Operations
```python
def write_database(database: WordDatabase, output_path: Path, config: Config) -> Path:
    """Write database to JSON file with atomic operations."""
```

### Pipeline Orchestration
```python
def process_audio_to_json(audio_path: str, config: Config,
                         output_path: Optional[str] = None,
                         speaker_mapping: Optional[Dict] = None,
                         resume_from_stage: Optional[str] = None) -> WordDatabase:
    """Complete audio-to-JSON pipeline."""
```

## CLI Interface Contracts

### Command Structure
```bash
pronunciation-clips process <audio_file> [OPTIONS]
pronunciation-clips version
pronunciation-clips info [--check-dependencies]
```

### Exit Codes
- **0**: Success
- **1**: Error (AudioError, ConfigError, etc.)

## Configuration Interface

### Environment Variable Pattern
```
PRONUNCIATION_CLIPS_<SECTION>_<KEY>=<VALUE>

Examples:
PRONUNCIATION_CLIPS_QUALITY_MIN_CONFIDENCE=0.9
PRONUNCIATION_CLIPS_WHISPER_MODEL=medium
```

### YAML Configuration Sections
- `audio`: Sample rate, channels, buffer settings
- `whisper`: Model, language, temperature settings  
- `quality`: Confidence thresholds, duration limits, syllable ranges
- `speakers`: Diarization settings, default speaker info
- `output`: File paths, encoding, formatting options
- `logging`: Level, format, output destinations