# Implementation Details

## Data Storage Architecture

### Storage Format
- **Initial**: JSON-based word occurrences database
- **Migration path**: Designed for easy conversion to SQLite in future
- **Structure**: Flat array of word occurrences for optimal querying
- **Future extensibility**: Designed to support sentences/phrases without breaking changes

### JSON Schema

```json
{
  "metadata": {
    "version": "1.0",
    "created_at": "2025-08-15T...",
    "whisper_model": "base"
  },
  "speaker_map": {
    "0": {"name": "María", "gender": "F", "region": "Bogotá"},
    "1": {"name": "Carlos", "gender": "M", "region": "Medellín"}, 
    "2": {"name": "Speaker_3", "gender": "Unknown", "region": "Unknown"}
  },
  "entities": [
    {
      "entity_id": "word_001",
      "entity_type": "word",
      "text": "hola",
      "start_time": 1.23,
      "end_time": 1.67,
      "duration": 0.44,
      
      // Whisper outputs
      "confidence": 0.95,
      "probability": 0.89,
      
      // Analysis fields
      "syllables": ["ho", "la"],
      "syllable_count": 2,
      "phonetic": "ˈoʊlə",
      "quality_score": 0.87,
      
      // Speaker & context
      "speaker_id": "0",
      "recording_id": "rec_audio1_wav",
      "recording_path": "audio1.wav",
      
      // Processing status
      "processed": false,
      "clip_path": null,
      "selection_reason": null,
      "created_at": "2025-08-15T..."
    }
  ]
}
```

## Dependencies

From `requirements.txt`:
- `openai-whisper>=20231117` - Speech recognition and word timestamps
- `librosa>=0.10.0` - Audio processing
- `pydub>=0.25.0` - Audio manipulation
- `soundfile>=0.12.0` - Audio I/O
- `pandas>=2.0.0` - Data analysis and JSON/SQL migration
- `numpy>=1.21.0` - Numerical operations
- `torch>=2.0.0` - Deep learning framework
- `torchaudio>=2.0.0` - Audio processing for PyTorch

## Modular Architecture

### Module Separation
- **Module 1**: Audio → JSON Pipeline (Initial focus)
  - Scope: Audio files → Complete JSON database with all entities
  - Output: Populated JSON, no audio clips extracted yet
- **Module 2**: JSON → Clips Pipeline (Future implementation)
  - Scope: JSON database → Audio clips + updated JSON processing status

### Shared Components (Root Level)
- **Configuration management**: Centralized YAML config with Pydantic validation
- **Logging framework**: Structured logging across both modules  
- **Core data models**: Pydantic models for type safety and validation
- **Common validation**: Entity structure, timestamps, file paths, JSON schema

### Data Models Design
- **Framework**: Pydantic for validation, serialization, and type safety
- **Entity Model**: Single class with `entity_type` field (word/sentence/phrase)
- **Database Container**: `WordDatabase` model with metadata, speaker_map, entities
- **Validation Strategy**: Field-level validation with custom validators
- **Benefits**: JSON serialization, pandas integration, IDE autocomplete

### Pipeline Data Flow & Intermediate Storage
- **Function-based pipeline**: Simple, testable stage functions
- **Intermediate files**: JSON files in `temp/` for resumability between stages
- **Modular speaker integration**: Optional speaker mapping merged with transcription
- **Data aggregation**: `create_entities()` merges word timestamps + speaker data
- **Resumability**: Each stage saves output, can resume from any checkpoint

### Error Handling Strategy
- **MVP approach**: Simple exception hierarchy with clear inheritance
- **Fail fast**: Let exceptions bubble up, log with context
- **Expandable**: Easy to add retry logic and specific error types later
- **No complex recovery**: Keep initial implementation simple

### Logging & Observability
- **Structured logging**: Using structlog with rich context at each stage
- **Key metrics**: Word counts, confidence distributions, processing times
- **Session correlation**: UUID-based session tracking across pipeline stages
- **Performance monitoring**: Memory usage, processing speed per audio minute

### File I/O Patterns
- **Atomic writes**: Temporary file + rename for database updates
- **Backup strategy**: Timestamped backups before each update
- **Validation**: Verify written JSON before replacing original
- **Directory management**: Safe creation and cleanup of temporary files

### Testing Strategy
- **Multi-layer approach**: Unit, integration, and property-based testing
- **AI-specific tests**: Deterministic output, boundary cases, quality thresholds
- **Resumability testing**: Verify pipeline restart from any checkpoint
- **Real audio fixtures**: Small sample files for integration tests

### Interface Design
- **CLI-first approach**: Click framework for professional command-line interface
- **Configuration-driven**: All behavior controlled via YAML config files
- **Python API**: Easy to add later by exposing existing pipeline functions
- **Extensible**: Structure supports batch processing and advanced options

## Critical Technical Findings

### **Validated Configuration Values**
From Colombian Spanish testing (Juan Gabriel Vásquez audio):

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
```

### **Critical Implementation Requirement: Smart Buffering**
**Validated Issue**: Colombian Spanish continuous speech has 0ms word gaps
- **Problem**: Fixed 50ms buffer captures next word start
- **Example**: "buenas" ends 0.540s → "tardes" starts 0.540s (0ms gap)
- **Solution Required**: Adaptive buffering based on actual word gaps
- **Implementation**: Check `end_time[n] vs start_time[n+1]` before adding buffer

### **Performance Characteristics**
- **Transcription bottleneck**: 99.9% of time (231.6ms/word)
- **Clip extraction**: <1ms per clip (negligible)
- **Scaling**: Linear with audio duration (~44min for 81min audio)

## Implementation Plan & Testing Checkpoints

### **Strategy: Bulletproof Incremental Development**
**Sequential Testing Pyramid**: Unit → Integration → End-to-End. Each layer must pass before proceeding to next. Tests are defined upfront and cannot be changed during implementation.

### **Testing Progression for Each Stage**
1. **Unit Tests**: Test individual functions in isolation with mocks
2. **Integration Tests**: Test module interactions with real dependencies  
3. **End-to-End Tests**: Test complete user workflows with real data
4. **Demo Scripts**: Manual validation and visual confirmation

**CRITICAL RULE**: No progression until ALL tests in current layer pass completely.

### **Stage 1: Foundation (Config + Models + Logging)**
**Deliverables**: `shared/config.py`, `shared/models.py`, `shared/logging_config.py`, `shared/exceptions.py`

**Unit Tests (MUST PASS FIRST):**
1. **Config Unit Tests** (`tests/unit/test_config.py`)
   - `test_load_valid_yaml()`: Load valid config without errors
   - `test_invalid_yaml_raises_error()`: Invalid YAML raises ConfigError
   - `test_missing_section_raises_error()`: Missing required section fails
   - `test_environment_override()`: Environment variable overrides config value
   - `test_config_validation()`: Pydantic validation catches invalid types

2. **Models Unit Tests** (`tests/unit/test_models.py`)
   - `test_entity_creation()`: Create valid Entity with all fields
   - `test_entity_invalid_timestamps()`: end_time <= start_time raises ValueError
   - `test_entity_serialization()`: Entity.json() produces valid JSON
   - `test_word_database_creation()`: Create WordDatabase with entities
   - `test_speaker_info_validation()`: SpeakerInfo validates required fields

3. **Logging Unit Tests** (`tests/unit/test_logging.py`)
   - `test_logger_initialization()`: Initialize structured logger
   - `test_session_id_binding()`: Session ID appears in all log entries
   - `test_context_binding()`: Context fields (stage, recording_id) logged
   - `test_log_levels()`: DEBUG, INFO, WARNING, ERROR levels work
   - `test_structured_output()`: Log output contains expected JSON fields

4. **Exceptions Unit Tests** (`tests/unit/test_exceptions.py`)
   - `test_exception_hierarchy()`: All exceptions inherit from PipelineError
   - `test_exception_messages()`: Error messages contain helpful context
   - `test_exception_chaining()`: Original errors preserved in chain

**Integration Tests (MUST PASS SECOND):**
1. **Config Integration** (`tests/integration/test_config_integration.py`)
   - Load real `config.yaml` and validate all sections
   - Override config with environment variables
   - Test config with missing optional sections

**End-to-End Tests (MUST PASS THIRD):**
1. **Foundation Integration Test** (`tests/e2e/test_stage1_e2e.py`)
   - Load config.yaml, create models, initialize logging in sequence
   - Full workflow: Config → Entity creation → Logging → JSON serialization
   - Verify complete foundation stack works together

**Demo Script (FINAL VALIDATION)**: `demos/demo_foundation.py`
**Success Criteria**: 
- **16 unit tests pass** (4 per module × 4 modules)
- **1 integration test passes** 
- **1 end-to-end test passes**
- **Demo script runs without errors**

**Testing Commands**:
```bash
pytest tests/unit/test_config.py -v          # Must pass before proceeding
pytest tests/unit/test_models.py -v          # Must pass before proceeding  
pytest tests/unit/test_logging.py -v         # Must pass before proceeding
pytest tests/unit/test_exceptions.py -v      # Must pass before proceeding
pytest tests/integration/test_config_integration.py -v  # Must pass before proceeding
pytest tests/e2e/test_stage1_e2e.py -v       # Must pass before proceeding
python demos/demo_foundation.py              # Must run successfully
```

### **Stage 2: Audio Processing**
**Deliverables**: `audio_to_json/audio_processor.py`

**End-to-End Tests (ALL MUST PASS):**
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

**Test Audio Files Required**:
- `fixtures/spanish_30sec_16khz.wav`
- `fixtures/spanish_30sec_44khz.wav`
- `fixtures/corrupted.wav`

**Pytest Suite**: `tests/integration/test_stage2_audio.py`
**Demo Script**: `demos/demo_audio.py`
**Success Criteria**: All 3 test scenarios pass, processes real audio files

### **Stage 3: Transcription Engine**
**Deliverables**: `audio_to_json/transcription.py`

**End-to-End Tests (ALL MUST PASS):**
1. **Successful Transcription**
   - Transcribe Spanish audio file with word timestamps
   - Verify word count > 0 and < 1000 for 30-second file
   - Verify all words have start_time < end_time
   - Verify confidence scores between 0.0 and 1.0

2. **Whisper Configuration**
   - Use "base" model as specified in config
   - Enable word timestamps in output
   - Process with temperature=0.0 for deterministic output

3. **Edge Case Handling**
   - Process very quiet audio (near silence)
   - Process audio with background noise
   - Verify error handling for invalid audio data

**Test Audio Files Required**:
- `fixtures/spanish_clear_30sec.wav` (clear speech)
- `fixtures/spanish_noisy_30sec.wav` (background noise)
- `fixtures/spanish_quiet_30sec.wav` (low volume)

**Pytest Suite**: `tests/integration/test_stage3_transcription.py`
**Demo Script**: `demos/demo_transcription.py`
**Success Criteria**: All 3 test scenarios pass, real Whisper transcription works

### **Stage 4: Entity Creation & Quality Filtering**
**Deliverables**: `audio_to_json/entity_creation.py`

**End-to-End Tests (ALL MUST PASS):**
1. **Entity Creation**
   - Convert Whisper words to valid Entity objects
   - Generate unique entity_ids in format "word_001", "word_002"
   - Assign entity_type="word" to all entities
   - Calculate duration field correctly (end_time - start_time)

2. **Quality Filtering**
   - Filter out words with confidence < min_confidence (0.5)
   - Filter out words shorter than min_word_duration (0.1s)
   - Filter out words longer than max_word_duration (3.0s)
   - Verify filtered count logged correctly

3. **Speaker Assignment**
   - Assign default speaker_id="speaker_0" when no speakers provided
   - Handle None speaker_mapping gracefully
   - Preserve speaker assignment in entity creation

**Test Data Required**:
- Mock transcription with mix of high/low confidence words
- Mock transcription with very short and very long words

**Pytest Suite**: `tests/integration/test_stage4_entities.py`
**Demo Script**: `demos/demo_entities.py`
**Success Criteria**: All 3 test scenarios pass, quality filtering works correctly

### **Stage 5: Database Writing**
**Deliverables**: `audio_to_json/database_writer.py`

**End-to-End Tests (ALL MUST PASS):**
1. **Atomic Database Writing**
   - Write WordDatabase to JSON file atomically
   - Verify backup created before write
   - Verify JSON validates against schema after write
   - Test rollback on write failure

2. **JSON Structure Validation**
   - Output contains metadata, speaker_map, entities sections
   - All entities have required fields (entity_id, entity_type, text, etc.)
   - JSON is valid and parseable
   - Pretty printing works when enabled

3. **File Safety**
   - Handle existing database file (backup + replace)
   - Handle write permission errors gracefully
   - Clean up temporary files on success and failure

**Pytest Suite**: `tests/integration/test_stage5_database.py`
**Demo Script**: `demos/demo_database.py`
**Success Criteria**: All 3 test scenarios pass, atomic writes work

### **Stage 6: Full Pipeline Integration**
**Deliverables**: `audio_to_json/pipeline.py`

**End-to-End Tests (ALL MUST PASS):**
1. **Complete Audio-to-JSON Pipeline**
   - Process real Spanish audio file end-to-end
   - Verify output JSON contains expected word count (±20%)
   - Verify all entities have valid timestamps and confidence scores
   - Verify processing completes within reasonable time

2. **Resumability**
   - Stop pipeline after transcription stage
   - Resume from transcription and complete successfully
   - Verify intermediate files created and used correctly

3. **Error Handling**
   - Graceful failure on invalid audio file
   - Graceful failure on Whisper model loading error
   - Proper error logging and cleanup

**Test Audio Files Required**:
- `fixtures/spanish_complete_test.wav` (2-3 minute Spanish audio)

**Pytest Suite**: `tests/integration/test_stage6_pipeline.py`
**Demo Script**: `demos/demo_pipeline.py`
**Success Criteria**: All 3 test scenarios pass, full pipeline works end-to-end

### **Stage 7: Speaker Integration**
**Deliverables**: `audio_to_json/speaker_identification.py`

**End-to-End Tests (ALL MUST PASS):**
1. **Manual Speaker Mapping**
   - Apply provided speaker map to entities
   - Verify speaker_id assignment based on timestamps
   - Handle overlapping speaker segments correctly

2. **Default Speaker Handling**
   - Assign default speaker when speaker_mapping=None
   - Create appropriate speaker_map in output JSON
   - Handle unknown speakers gracefully

3. **Multi-Speaker Scenarios**
   - Process audio with multiple speaker segments
   - Verify speaker boundaries respected
   - Verify speaker metadata preserved in output

**Pytest Suite**: `tests/integration/test_stage7_speakers.py`
**Demo Script**: `demos/demo_speakers.py`
**Success Criteria**: All 3 test scenarios pass, speaker mapping works

### **Stage 8: CLI Interface**
**Deliverables**: `cli/main.py`, `cli/commands.py`

**End-to-End Tests (ALL MUST PASS):**
1. **Basic CLI Commands**
   - `pronunciation-clips process audio.wav` completes successfully
   - CLI shows progress and completion message
   - Output file created in expected location

2. **Configuration Handling**
   - CLI uses default config.yaml
   - CLI accepts custom config with --config flag
   - CLI shows helpful error for missing config

3. **Error Display**
   - CLI shows user-friendly error for invalid audio
   - CLI shows help text when run without arguments
   - CLI exit codes correct (0 for success, 1 for error)

**Pytest Suite**: `tests/integration/test_stage8_cli.py`
**Demo Script**: Manual CLI testing
**Success Criteria**: All 3 test scenarios pass, full user workflow works

## Automated Testing Framework

### **Pytest Configuration**
- All tests runnable with `pytest tests/integration/`
- Each stage has dedicated test file
- Real audio fixtures in `tests/fixtures/`
- Comprehensive test coverage for each checkpoint

### **Sequential Testing Commands**
```bash
# Stage progression commands
make test-unit-stage1      # Run all Stage 1 unit tests
make test-integration-stage1   # Run Stage 1 integration tests  
make test-e2e-stage1      # Run Stage 1 end-to-end tests
make demo-stage1          # Run Stage 1 demo script

# Full stage validation
make test-stage1          # Run all Stage 1 tests (unit → integration → e2e → demo)
```

### **Pre-Implementation: E2E Test Skeleton Setup**
**BEFORE any coding begins**, create skeleton E2E tests for each stage using custom scripts:

```bash
# Create E2E test skeletons first
python setup_e2e_tests.py    # Creates skeleton tests for all 8 stages
pytest tests/e2e/ --dry-run  # Verify all tests discoverable (will fail, that's expected)
```

**Purpose**: Define exact success criteria and interfaces before implementation starts.

### **Development Workflow Per File**
1. **Write function/class**
2. **Write unit tests** for that function/class
3. **Run unit tests** - must pass before continuing
4. **Write integration tests** (if needed)
5. **Run integration tests** - must pass before continuing  
6. **Only after ALL tests pass** - proceed to next function

### **Stage Progression Rules**
- **No file creation** until its unit tests are written and passing
- **No integration testing** until all unit tests pass
- **No end-to-end testing** until all integration tests pass  
- **No demo script** until all end-to-end tests pass
- **No next stage** until current stage demo runs successfully
- **Git commit required** after each stage's E2E tests pass

### **Git Commit Strategy**
Each stage completion creates a stable checkpoint:

```bash
# Pre-implementation setup
git add tests/ e2e_test_setup_plan.md
git commit -m "Setup E2E test framework for all 8 stages

- Created skeleton E2E tests defining success criteria
- Test fixtures and configuration ready
- Makefile commands for test execution
- Clear interfaces forced through test requirements"

# Stage 1 completion
git add src/shared/ tests/unit/test_*shared* tests/integration/ tests/e2e/test_stage1*
git commit -m "Stage 1: Foundation complete - config, models, logging

- All 16 unit tests passing
- Integration tests passing  
- E2E test passing: config → models → logging → JSON
- Demo script runs successfully
- Foundation ready for pipeline stages"

# Stage 2 completion  
git add src/audio_to_json/audio_processor.py tests/unit/test_audio* tests/e2e/test_stage2*
git commit -m "Stage 2: Audio processing complete

- Audio loading and validation working
- Format conversion (44.1kHz → 16kHz) working
- Metadata extraction accurate
- Error handling for invalid files
- All unit, integration, and E2E tests passing"

# Continue pattern for all stages...
```

### **Commit Benefits**
- **Stable checkpoints**: Can always revert to last working stage
- **Clear progress tracking**: Each commit represents fully validated functionality
- **Debugging aid**: Easy to isolate when issues were introduced
- **Confidence building**: Each commit proves stage completeness

### Module-Specific Validation
- **Module 1**: Audio formats, sample rates, Whisper confidence thresholds, speaker diarization
- **Module 2**: Selection criteria, duration limits, clip naming conflicts

## Data Structure Design Decisions

### Entity Structure
- **Generic entities**: `word_occurrences` renamed to `entities` for extensibility
- **Multiple entries per word**: Each spoken instance gets its own record
- **Flat array structure**: Optimized for pandas operations and SQL migration
- **Unique entity IDs**: Enable precise tracking and updates
- **Entity types**: Currently `"word"` only, designed for future `"sentence"` and `"phrase"`

### Speaker Management
- **Speaker mapping**: Separate map linking IDs to names/metadata
- **Flexible identification**: Support both named speakers and unknown speakers
- **Filter capability**: Easy querying by speaker name or characteristics

### Processing Pipeline Compatibility
- **Pipeline stages**: Designed for transcription → selection → clip extraction
- **State tracking**: `processed` flag enables resumable operations
- **Atomic updates**: Structure supports concurrent clipping script updates

## Clip Storage

### Directory Structure
- **Flat structure**: Single `clips/` directory for all audio clips
- **Naming convention**: `{text}_{entity_type}_{entity_num}_{speaker}_{start}-{end}.wav`
- **Example**: `hola_word_001_maria_1.23-1.67.wav`

### Benefits
- Simple filesystem operations and atomic writes
- Human-readable filenames for easy browsing
- No directory management overhead
- Compatible with JSON database organization

## Future Extensions (Not Implemented Initially)

### Sentence/Phrase Support
**Note**: The JSON structure now supports this extensibility, but sentence/phrase functionality will not be implemented in the initial MVP.

Future sentence/phrase entities would extend the current structure:

```json
{
  "entity_id": "sentence_001", 
  "entity_type": "sentence",
  "text": "Hola, ¿cómo estás?",
  "start_time": 1.23,
  "end_time": 3.45,
  "word_ids": ["word_001", "word_002", "word_003"],
  "word_count": 3,
  "speaker_id": "0",
  "recording_id": "rec_audio1_wav",
  "processed": false,
  "clip_path": null
}
```

Additional fields for sentences/phrases:
- `word_ids`: References to constituent word entities
- `word_count`: Number of words (easily computed, can be added later)

## Migration Path

### JSON to SQLite
- **Easy conversion**: `pd.read_json()` → `df.to_sql()`
- **Normalized structure**: Current design maps directly to relational tables
- **Query optimization**: Flat structure enables efficient indexing and joins