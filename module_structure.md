# Module Structure Design

## Project Root Structure
```
pronunciation-clips/
├── config.yaml                    # Main configuration file
├── requirements.txt               # Dependencies
├── implementation.md              # Architecture documentation
├── CLAUDE.md                      # Project guidelines
│
├── src/                           # Source code
│   ├── __init__.py
│   ├── shared/                    # Shared utilities (cross-module)
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration loading & validation
│   │   ├── models.py              # Pydantic data models
│   │   ├── logging_config.py      # Structured logging setup
│   │   ├── exceptions.py          # Exception hierarchy
│   │   └── file_utils.py          # Atomic I/O operations
│   │
│   ├── audio_to_json/             # Module 1: Audio → JSON Pipeline
│   │   ├── __init__.py
│   │   ├── pipeline.py            # Main pipeline orchestration
│   │   ├── audio_processor.py     # Audio loading & validation
│   │   ├── transcription.py       # Whisper integration
│   │   ├── speaker_identification.py  # Speaker diarization
│   │   ├── entity_creation.py     # Entity creation & quality filtering
│   │   └── database_writer.py     # JSON database output
│   │
│   └── cli/                       # Command-line interface
│       ├── __init__.py
│       ├── main.py                # Click CLI entry point
│       └── commands.py            # CLI command implementations
│
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── fixtures/                  # Test audio files & configs
│   │   ├── sample_audio.wav       # Small test audio file
│   │   ├── test_config.yaml       # Test configuration
│   │   └── expected_output.json   # Expected pipeline output
│   │
│   ├── unit/                      # Unit tests
│   │   ├── test_config.py
│   │   ├── test_models.py
│   │   ├── test_audio_processor.py
│   │   ├── test_transcription.py
│   │   ├── test_entity_creation.py
│   │   └── test_file_utils.py
│   │
│   ├── integration/               # Integration tests
│   │   ├── test_full_pipeline.py
│   │   ├── test_resumability.py
│   │   └── test_cli.py
│   │
│   └── property/                  # Property-based tests
│       └── test_quality_filtering.py
│
├── temp/                          # Temporary files (gitignored)
│   └── .gitkeep
│
└── output/                        # Default output directory
    └── .gitkeep
```

## Module Responsibilities

### **shared/** - Cross-Module Utilities
- **config.py**: Load YAML, validate with Pydantic, environment overrides
- **models.py**: Entity, WordDatabase, SpeakerInfo, AudioMetadata classes
- **logging_config.py**: Configure structlog, session correlation
- **exceptions.py**: PipelineError, AudioError, TranscriptionError hierarchy
- **file_utils.py**: Atomic writes, backup creation, directory management

### **audio_to_json/** - Core Pipeline Logic
- **pipeline.py**: Main orchestration, stage coordination, resumability
- **audio_processor.py**: Load audio files, validate format, extract metadata
- **transcription.py**: Whisper integration, word timestamp extraction
- **speaker_identification.py**: Manual/automatic speaker mapping
- **entity_creation.py**: Merge transcription + speakers, apply quality filters
- **database_writer.py**: Save final JSON database with atomic writes

### **cli/** - User Interface
- **main.py**: Click CLI setup, main entry point
- **commands.py**: Individual CLI commands (process, batch, etc.)

## Key Design Principles

### **Single Responsibility**
Each module handles one specific pipeline stage or utility function

### **Clear Dependencies**
```
cli/ → audio_to_json/ → shared/
     ↘ shared/         ↗
```

### **Testability**
- Each module can be tested in isolation
- Fixtures provide consistent test data
- Integration tests verify end-to-end behavior

### **Resumability Support**
- `pipeline.py` manages intermediate file state
- Each stage can be skipped if output already exists
- Clear checkpoint naming in `temp/` directory

### **Configuration-Driven**
- No hardcoded values in any module
- All behavior controlled via `config.yaml`
- Environment variable overrides supported