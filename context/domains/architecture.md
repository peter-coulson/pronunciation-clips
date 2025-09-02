# Architecture & Design

## MVP Scope
- Local-only inputs: accept audio files from disk; no URLs or cloud sources
- Focus on a scalable pipeline; UI and long-term APIs are out of scope
- JSON-based storage with migration path to SQLite

## System Architecture

### Two-Module Design
- **Module 1**: Audio → JSON Pipeline (Current focus)
  - Scope: Audio files → Complete JSON database with all entities
  - Output: Populated JSON, no audio clips extracted yet
- **Module 2**: JSON → Clips Pipeline (Future implementation)
  - Scope: JSON database → Audio clips + updated JSON processing status

### Pipeline Stages
1. **Audio Processing**: Format validation, metadata extraction, resampling
2. **Transcription**: faster-whisper with CPU optimization
2.5. **Speaker Diarization**: Optional PyAnnote-based speaker separation with MPS acceleration
3. **Entity Creation**: Convert words to typed entities with quality filtering and speaker assignment
4. **Database Creation**: Assemble complete WordDatabase with metadata
5. **Smart Buffering**: Colombian Spanish zero-gap detection and buffering
6. **Database Writing**: Atomic JSON file operations with backup

### Core Components

#### Shared Foundation (`src/shared/`)
- **Configuration**: YAML config with Pydantic validation (`config.py`)
- **Data Models**: Type-safe Pydantic models (`models.py`)
- **Logging**: Structured logging with session correlation (`logging_config.py`)
- **Exceptions**: Hierarchical error handling (`exceptions.py`)

#### Audio-to-JSON Pipeline (`src/audio_to_json/`)
- **Audio Processor**: Format handling, validation, metadata extraction
- **Transcription Engine**: faster-whisper with CPU optimization
- **Diarization Processor**: PyAnnote-based speaker diarization with MPS acceleration and pipeline caching
- **Entity Creation**: Word-to-entity conversion with quality filters and speaker assignment
- **Speaker Identification**: Speaker mapping and diarization support with batch processing
- **Database Writer**: Atomic file operations with backup/rollback
- **Pipeline Orchestrator**: Stage coordination and resumability

#### CLI Interface (`src/cli/`)
- **Main Interface**: Click-based command-line interface
- **User Experience**: Progress bars, error handling, configuration management

## Design Patterns

### Data Flow Architecture
- **Function-based pipeline**: Simple, testable stage functions
- **Intermediate storage**: JSON checkpoints in `temp/` for resumability
- **Immutable entities**: Entity objects don't change once created
- **State tracking**: `processed` flag enables resumable operations

### Error Handling Strategy
- **Exception hierarchy**: All errors inherit from PipelineError
- **Fail fast**: Exceptions bubble up with contextual information
- **Structured logging**: Rich context at each stage
- **User-friendly CLI**: Clean error messages for end users

### Configuration Management
- **YAML-driven**: All behavior controlled via config files
- **Environment overrides**: `PRONUNCIATION_CLIPS_*` environment variables
- **Validation**: Pydantic ensures type safety and constraints
- **Default fallbacks**: Built-in defaults for missing configurations