# Testing Strategy — Current Implementation

## Test Suite Status ✅ COMPLETE + ENHANCED
**Total Test Files**: 29 across all layers
- **Unit Tests**: 11 files testing individual components (includes diarization)
- **Integration Tests**: 7 files testing stage interactions  
- **E2E Tests**: 9 files testing complete workflows (includes diarization)
- **Shared Infrastructure**: conftest.py with fixtures + test data
- **Test Categorization**: Quick (<15s) and Extensive (≥15s) test markers

## Test Infrastructure
### Fixtures (`tests/fixtures/`)
- **Hybrid Duration Audio Files**: Multi-duration test coverage
  - **5-second clips**: Fast smoke testing (`spanish_clear_5sec.wav`)
  - **15-second clips**: Medium coverage testing 
    - `spanish_clear_15sec.wav` - Speaker transitions
    - `spanish_multi_15sec.wav` - Multi-speaker scenarios
    - `spanish_noisy_15sec.wav` - Noise resilience
  - **30-second clips**: Full conversation testing
    - `spanish_30sec_16khz.wav` - Standard format
    - `spanish_30sec_44khz.wav` - High sample rate  
    - `spanish_clear_30sec.wav` - Clear pronunciation
    - `spanish_noisy_30sec.wav` - Background noise testing
    - `spanish_quiet_30sec.wav` - Low volume testing
  - **120-second clips**: Extended testing (`spanish_complete_test.wav`)
- **Test Configuration**: `test_config.yaml` with testing-optimized settings
- **Expected Outputs**: Directory for validation data

### Shared Fixtures (`conftest.py`)
- **temp_dir**: Isolated temporary directories
- **test_config_path**: Standard test configuration
- **test_audio_fixtures**: All audio file paths mapped
- **mock_transcription_data**: Sample Whisper output
- **expected_entity_fields**: Entity validation schema

## Test Layer Architecture

### Unit Tests (`tests/unit/`) — 11 Files
**Component Isolation Testing**
- `test_config.py` - YAML configuration loading
- `test_models.py` - Pydantic Entity/WordDatabase validation  
- `test_exceptions.py` - Custom exception hierarchy
- `test_logging_config.py` - Structured logging setup
- `test_audio_processor.py` - Audio format handling
- `test_transcription.py` - Whisper integration
- `test_entity_creation.py` - Word-to-entity conversion
- `test_database_writer.py` - JSON atomic operations
- `test_pipeline.py` - Pipeline orchestration logic
- `test_cli.py` - Click CLI interface
- `test_diarization.py` - Speaker diarization components

### Integration Tests (`tests/integration/`) — 7 Files
**Stage Interaction Testing**
- `test_stage1_foundation_integration.py` - Config + Models + Logging
- `test_stage2_audio_integration.py` - Audio processing workflows
- `test_stage3_transcription_integration.py` - Audio → Transcription
- `test_stage4_entities_integration.py` - Transcription → Entities  
- `test_stage5_database_integration.py` - Entities → Database
- `test_stage6_pipeline_integration.py` - Complete pipeline flows
- `test_stage8_cli_integration.py` - CLI → Pipeline integration

### End-to-End Tests (`tests/e2e/`) — 9 Files
**Complete Workflow Testing**
- `test_stage1_foundation_e2e.py` - Config loading → Entity creation → JSON serialization
- `test_stage2_audio_e2e.py` - Audio file → Validated audio processing
- `test_stage3_transcription_e2e.py` - Audio → Whisper → Timestamped words
- `test_stage4_entities_e2e.py` - Transcription → Validated entities
- `test_stage5_database_e2e.py` - Entities → Database → Retrieval
- `test_stage6_pipeline_e2e.py` - Audio file → Complete database
- `test_stage7_speakers_e2e.py` - Multi-speaker audio → Speaker-tagged entities
- `test_stage8_cli_e2e.py` - CLI commands → File outputs
- `test_diarization_e2e.py` - **Hybrid Testing**: Speaker diarization workflows with multi-duration coverage

## Test Execution Infrastructure

### Hybrid Testing Strategy
**Quick Tests (Development)**: `<15s execution`
- **Basic Smoke**: `./pytest_venv.sh tests/ -m quick -v` (~12s total)
- **Unit Tests**: All unit tests marked as quick (~0.5s total)  
- **E2E Quick**: Essential E2E functionality validation (~10s total)
- **Diarization Quick**: 5s + 15s audio clips (~9s total)

**Extensive Tests (CI/Release)**: `≥15s execution`
- **Full Coverage**: `./pytest_venv.sh tests/ -v` (~25s total)
- **Diarization Full**: `ENABLE_EXTENSIVE_TESTS=true ./pytest_venv.sh tests/e2e/test_diarization_e2e.py -v`
- **Performance Tests**: Long-duration audio validation
- **Error Handling**: Complex failure scenarios

### Test Command Matrix
**Development Workflow**:
```bash
# Quick development cycle (~12s)
./pytest_venv.sh tests/ -m quick -v

# Diarization development (~9s) 
ENABLE_DIARIZATION_TESTS=true ./pytest_venv.sh tests/e2e/test_diarization_e2e.py -m quick -v

# Specific component testing
./pytest_venv.sh tests/unit/test_config.py -v
./pytest_venv.sh tests/e2e/test_stage1_foundation_e2e.py -v
```

**CI/Release Validation**:
```bash
# Full test suite (~25s)
./pytest_venv.sh tests/ -v

# Complete diarization coverage (~20s)
ENABLE_DIARIZATION_TESTS=true ENABLE_EXTENSIVE_TESTS=true ./pytest_venv.sh tests/e2e/test_diarization_e2e.py -v

# Performance validation
./pytest_venv.sh tests/ -m extensive -v
```

### Environment Variables
- **`ENABLE_DIARIZATION_TESTS`**: Controls diarization test execution (default: `true`)
- **`ENABLE_EXTENSIVE_TESTS`**: Controls extensive test execution (default: `false`)
- **`HUGGINGFACE_HUB_TOKEN`**: Required for diarization model access

### Test Environment
- **Virtual Environment**: `./venv/` with isolated dependencies
- **Test Configuration**: Optimized for speed (Whisper "base" model)
- **Output Isolation**: `tests/output/` directory for test artifacts
- **Audio Processing**: Multi-duration Spanish audio for comprehensive testing
- **Pytest Markers**: Structured test categorization with `pytest.ini`

## Diarization Testing Module

### Test Coverage Strategy
The diarization module uses **hybrid duration testing** for optimal coverage vs speed:

**5-Second Tests (Smoke)**: Fast validation (~3s each)
- `test_basic_diarization_quick_e2e()` - Core functionality
- Basic speaker detection and segment validation

**15-Second Tests (Medium Coverage)**: Speaker transitions (~12s each)  
- `test_speaker_transitions_medium_e2e()` - Multi-speaker scenarios
- Coverage for speaker change detection and transition accuracy

**30-Second Tests (Full Coverage)**: Complete conversations (~20s each)
- `test_complete_conversation_full_e2e()` - Long-duration accuracy
- Complex multi-speaker interaction patterns

### Diarization Test Categories
**Core Functionality** (Quick):
- Speaker detection and segmentation
- Entity assignment to speakers
- Single-speaker fallback handling
- Disabled diarization compatibility

**Advanced Scenarios** (Extensive):
- Multi-speaker conversation flows
- Performance within realtime limits
- Error handling and recovery
- Model loading failure scenarios

### Dependencies & Setup
- **HuggingFace Token**: Required in `.env` for model access
- **PyAnnote Models**: Downloaded on first run (~500MB)
- **Fast Execution**: Optimized for development workflow (<15s total)

## Critical Testing Rules ✅ IMPLEMENTED + ENHANCED
- **E2E Test Immutability**: All 8 E2E tests complete and locked
- **Stage Gates**: Each stage fully tested before progression  
- **Test Layer Progression**: Unit → Integration → E2E all implemented
- **Real Audio Testing**: 6 authentic Spanish audio fixtures
- **Performance Baselines**: Test configuration optimized for CI/CD

## Version Control Strategy ✅ ACTIVE
- **Stage-Based Commits**: Each major commit represents complete stage
- **Test Validation**: All tests passing before stage completion
- **Atomic Implementation**: Complete stage functionality per commit