# Configuration Reference

## Validated Colombian Spanish Settings
From real testing with Juan Gabriel Vásquez audio:

```yaml
# Quality thresholds (validated with real data)
quality:
  min_confidence: 0.8        # 35% pass rate, avg confidence 0.978
  min_word_duration: 0.3     # Filters articles, keeps content words  
  max_word_duration: 3.0     # Handles complex Spanish words
  syllable_range: [2, 6]     # 2-syl: 45%, 3-syl: 20%, 4+syl: 35%

# Whisper settings (validated)
whisper:
  model: "medium"            # Optimal speed/accuracy for Spanish
  language: "es"             # Required for proper Spanish tokenization
  word_timestamps: true      # Essential for clip extraction
  temperature: 0.0           # Deterministic output
```

## Complete Configuration Schema

### Audio Processing
```yaml
audio:
  sample_rate: 16000         # Required for Whisper
  channels: 1                # Mono conversion
  buffer_seconds: 0.025      # 25ms default buffer (Colombian Spanish: use smart buffering)
```

### Speaker Configuration
```yaml  
speakers:
  enable_diarization: true   # PyAnnote-based speaker diarization with MPS acceleration
  min_speakers: 1
  max_speakers: 10
  default_speaker:
    name: "Default Speaker"
    gender: "Unknown"
    region: "Unknown"

# Diarization configuration
diarization:
  model: "pyannote/speaker-diarization"  # HuggingFace model path
  segmentation_threshold: 0.5            # Speaker segment detection threshold
  clustering_threshold: 0.7              # Speaker clustering threshold
```

### Output Configuration
```yaml
output:
  database_path: "word_database.json"
  encoding: "utf-8"
  pretty_print: true         # Human-readable JSON formatting
  backup_on_update: true     # Automatic backups before updates
```

### Logging Configuration  
```yaml
logging:
  level: "INFO"              # DEBUG, INFO, WARNING, ERROR
  format: "structured"       # structured | simple
  file: null                 # Optional log file path
  console: true              # Console output enabled
```

## Environment Variable Overrides
All configuration values can be overridden:

```bash
# Quality settings
PRONUNCIATION_CLIPS_QUALITY_MIN_CONFIDENCE=0.9
PRONUNCIATION_CLIPS_QUALITY_MIN_WORD_DURATION=0.2

# Whisper settings  
PRONUNCIATION_CLIPS_WHISPER_MODEL=large
PRONUNCIATION_CLIPS_WHISPER_LANGUAGE=es

# Diarization settings
ENABLE_DIARIZATION_TESTS=true              # Enable diarization testing (requires HF_TOKEN)
HF_TOKEN=your_huggingface_token            # HuggingFace authentication token

# Logging
PRONUNCIATION_CLIPS_LOGGING_LEVEL=DEBUG
```

## Performance Implications
- **model: "medium"**: Best balance for Colombian Spanish (vs "base" or "large")
- **min_confidence: 0.8**: Filters ~65% of words, keeps high-quality pronunciations
- **syllable_range: [2, 6]**: Captures meaningful Spanish words, filters articles
- **Smart buffering**: Critical for Colombian Spanish continuous speech