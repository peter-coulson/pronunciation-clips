# Level 2 Architecture Specification

## Session Information
- **Session Name**: clip-extraction-system
- **Feature Name**: Pronunciation Clip Extraction System
- **Specification Level**: Level 2 (Architecture Level)
- **Architecture Date**: 2025-09-03
- **Previous Level**: Requirements Level (validated requirements analysis)
- **Next Level**: Interface Level (component boundaries definition)

## Architecture Overview

### System Purpose
Design a two-module system for extracting pronunciation clips from Spanish audio:
1. **Module 1**: Audio → JSON Pipeline (existing, enhanced)
2. **Module 2**: JSON → Clips Pipeline (new implementation)

### Architectural Principles
- **Function-Based Pipeline Architecture**: Simple, testable stage functions with clear input/output contracts
- **Immutable Entity Pattern**: Entity objects don't change once created, state tracking via 'processed' flag
- **Configuration-Driven Behavior**: YAML configuration with environment variable overrides
- **Resumable Processing**: Intermediate JSON checkpoints enable resuming from any pipeline stage

## System Decomposition

### Core System Components

#### 1. Foundation Layer (`src/shared/`)
**Responsibility**: Shared functionality across all modules
**Components**:
- **Configuration Management**: YAML loading with Pydantic validation and environment overrides
- **Data Models**: Pydantic schemas for Entity, WordDatabase, SpeakerInfo, AudioMetadata
- **Logging Infrastructure**: Structured logging with session correlation and rich context
- **Exception Handling**: PipelineError hierarchy with contextual information
- **Utility Functions**: Path normalization, file operations, validation helpers

**Architecture Rationale**: Centralized foundation prevents code duplication and ensures consistency across modules.

#### 2. Audio-to-JSON Pipeline (`src/audio_to_json/`)
**Responsibility**: Convert audio files to structured JSON database with entities
**Components**:
- **Audio Processor**: Audio loading, validation, format conversion, metadata extraction
- **Transcription Engine**: faster-whisper integration for word-level transcription
- **Diarization Processor**: PyAnnote integration for speaker identification (optional)
- **Entity Creator**: Transform transcription/diarization results into Entity objects
- **Database Writer**: Atomic JSON operations with backup/rollback capability
- **Pipeline Orchestrator**: Stage coordination with resumability via checkpoints

**Architecture Rationale**: Sequential pipeline stages with clear boundaries enable testing, debugging, and partial processing resumption.

#### 3. JSON-to-Clips Pipeline (`src/json_to_clips/`)
**Responsibility**: Extract audio clips from JSON database based on search criteria
**Components**:
- **Database Reader**: Query operations on JSON database with filtering capabilities
- **Search Engine**: Entity filtering by text patterns, speaker, confidence, duration
- **Clip Extractor**: Audio segmentation and file creation based on entity timestamps
- **Metadata Manager**: Clip metadata association and provenance tracking
- **Output Organizer**: Directory structure creation and file naming conventions

**Architecture Rationale**: Separation from audio processing enables independent development and different optimization strategies.

#### 4. CLI Interface (`src/cli/`)
**Responsibility**: User interaction layer for all system operations
**Components**:
- **Command Router**: Click-based command structure with argument validation
- **Progress Reporter**: User feedback for long-running operations
- **Configuration Manager**: CLI-based configuration overrides and validation
- **Error Handler**: User-friendly error messages with recovery suggestions
- **Help System**: Documentation and usage guidance integration

**Architecture Rationale**: Clean separation of user interface from processing logic enables alternative interfaces (API, GUI) without core changes.

### Component Relationships

#### Data Flow Architecture
```
Audio Files → Audio Processor → Transcription Engine → Entity Creator → Database Writer → JSON Database
                                      ↓
                              Diarization Processor (optional)
                                      ↓
JSON Database → Database Reader → Search Engine → Clip Extractor → Audio Clips
                                                        ↓
                                              Metadata Manager → Output Organization
```

#### Control Flow Architecture
```
CLI Interface → Configuration Manager → Pipeline Orchestrator
                                              ↓
Foundation Layer ← Audio-to-JSON Pipeline ← Configuration
                                              ↓
Foundation Layer ← JSON-to-Clips Pipeline ← JSON Database
```

#### Dependency Architecture
- **Foundation Layer**: No dependencies on other system components
- **Audio-to-JSON Pipeline**: Depends on Foundation Layer only
- **JSON-to-Clips Pipeline**: Depends on Foundation Layer only
- **CLI Interface**: Depends on Foundation Layer and orchestrates both pipelines

## Context Integration Notes

### Constraint Knowledge Application
- **Audio Format Compatibility**: Architecture supports librosa and faster-whisper compatible formats (.wav, .mp3, .m4a, .flac)
- **Memory Management**: Streaming I/O patterns with bounded memory usage for long audio files
- **Platform Integration**: macOS/Linux support with optional GPU acceleration (MPS/CUDA) for diarization
- **Database Schema**: JSON-based storage with migration path to SQLite using pandas integration

### Pattern Knowledge Application
- **Function-Based Pipeline**: Each component consists of simple, testable functions with clear contracts
- **Immutable Entity Pattern**: Entity objects maintain state through 'processed' flags without modification
- **Configuration-Driven**: YAML configuration structure with environment override capability
- **Colombian Spanish Processing**: Zero-gap buffering pattern to prevent word overlap in continuous speech

### Integration Knowledge Application
- **Two-Module Architecture**: Clear separation between audio processing and clip extraction enables independent optimization
- **Database Interface**: JSON-based intermediate storage with structured query capabilities
- **External Dependencies**: Proper integration contracts for faster-whisper, PyAnnote, and librosa
- **CLI Framework**: Click-based interface with progress reporting and error handling

### Convention Knowledge Application
- **Project Structure**: Modular organization (shared, audio_to_json, json_to_clips, cli) following established patterns
- **Error Handling**: PipelineError hierarchy with contextual information and structured logging
- **Testing Integration**: 3-layer testing architecture (Unit → Integration → E2E) with 27 test files
- **Version Control**: Stage-based development with complete functionality per commit

## Architecture Validation

### Component Cohesion Analysis
- **Foundation Layer**: High cohesion - all components support shared functionality
- **Audio-to-JSON Pipeline**: High cohesion - all components contribute to audio → entities transformation
- **JSON-to-Clips Pipeline**: High cohesion - all components contribute to entities → clips transformation  
- **CLI Interface**: Medium cohesion - unified user interface across different operations

### Component Coupling Analysis
- **Foundation ↔ Pipelines**: Low coupling through configuration and model interfaces
- **Audio-to-JSON ↔ JSON-to-Clips**: Very low coupling through JSON database intermediate storage
- **CLI ↔ Pipelines**: Low coupling through orchestration interfaces without direct dependency
- **Pipeline Internal**: Medium coupling appropriate for sequential processing stages

### Scalability Considerations
- **Horizontal Scaling**: JSON database enables multi-file processing with shared results
- **Vertical Scaling**: Pipeline checkpoints enable resumable processing for large audio files
- **Component Scaling**: Independent module development enables parallel team scaling
- **Performance Scaling**: Model caching and batch processing optimize resource utilization

### Maintainability Assessment
- **Clear Boundaries**: Component responsibilities are well-defined and non-overlapping
- **Testable Architecture**: Function-based design enables comprehensive unit testing
- **Configuration Management**: Centralized configuration reduces maintenance complexity
- **Error Handling**: Structured exception hierarchy enables systematic debugging

## Architecture Decisions Record

### Decision: Two-Module Architecture
**Context**: Original requirement for pronunciation clip extraction from audio files
**Decision**: Implement as separate Audio→JSON and JSON→Clips modules
**Rationale**: 
- Enables independent optimization strategies
- Provides reusable intermediate JSON database
- Allows different usage patterns (batch vs interactive)
- Facilitates testing and debugging

### Decision: Function-Based Pipeline Design  
**Context**: Need for testable, maintainable processing architecture
**Decision**: Use simple functions with clear input/output contracts
**Rationale**:
- Enables comprehensive unit testing
- Simplifies debugging and error isolation  
- Facilitates resume capability through checkpoints
- Reduces complexity compared to object-oriented alternatives

### Decision: JSON Database Intermediate Storage
**Context**: Bridge between audio processing and clip extraction
**Decision**: Use structured JSON with migration path to SQLite
**Rationale**:
- Human-readable for debugging and validation
- Pandas integration for SQLite migration
- Atomic operations with backup/rollback
- Query capabilities without database dependencies

### Decision: Pydantic-Based Configuration
**Context**: Configuration management across multiple modules
**Decision**: YAML configuration with Pydantic validation
**Rationale**:
- Type safety and validation at load time
- Environment variable override support
- Hierarchical structure for complex configurations
- IDE support and documentation generation

## Implementation Readiness Assessment

### Ready for Interface Level Transition
- ✅ Component responsibilities clearly defined
- ✅ Data flow architecture established  
- ✅ Dependency relationships mapped
- ✅ Context knowledge properly integrated
- ✅ Architecture decisions documented with rationale

### Interface Design Requirements
The Interface Level specification will need to define:
1. Component boundary contracts and method signatures
2. Data schema specifications for Entity and configuration models
3. Error handling interfaces and exception contracts
4. CLI command interfaces and parameter validation
5. External dependency integration contracts

### Architecture Success Criteria Met
- ✅ Architecture makes logical sense with clear component purposes
- ✅ Components are well-defined with appropriate coupling/cohesion
- ✅ Context knowledge integrated throughout architecture decisions
- ✅ Scalability and maintainability considerations addressed
- ✅ Foundation established for implementable interface definitions