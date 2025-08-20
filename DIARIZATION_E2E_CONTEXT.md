# DIARIZATION E2E TEST CONTEXT - Session 0

## Critical Implementation Rule: E2E TESTS FIRST
**MANDATORY**: These tests must be implemented BEFORE any production code.
**IMMUTABLE**: Once written, these tests CANNOT be modified during implementation.
**PURPOSE**: Define exact success criteria for the entire diarization system.

## Test Suite Overview
Implement all 5 E2E tests from diarization_implementation.md specification:

1. **Basic Diarization Detection** - Multi-speaker audio detection
2. **Entity Assignment Integration** - Proper speaker ID assignment to entities  
3. **Speaker Labeling Post-Processing** - Name assignment workflow
4. **Single Speaker Fallback** - Graceful single-speaker handling
5. **Diarization Disabled Compatibility** - Backward compatibility validation

## Implementation Requirements

### File Location
- **Primary**: `tests/e2e/test_diarization_e2e.py`
- **Fixtures**: `tests/fixtures/` (audio files and expected outputs)
- **Configuration**: Test configuration with diarization enabled/disabled

### Test Implementation Pattern
```python
def test_[feature]_e2e():
    """
    Test: [Input] → [Process] → [Expected Output]
    
    Success Criteria:
    - [Specific measurable criteria]
    - [Performance requirements]
    - [Error handling validation]
    """
    # Arrange: Setup inputs and expected outputs
    # Act: Run complete pipeline process
    # Assert: Validate all success criteria met
```

### Required Test Fixtures
#### Audio Files
- `hotz_fridman_conversation.wav` (multi-speaker, existing)
- `two_speaker_clear.wav` (synthetic clear speaker changes)
- `juan_gabriel_single_speaker.wav` (single speaker, existing)

#### Expected Output Files
- `expected_diarization_segments.json` (known-good segments)
- `expected_speaker_distribution.json` (entity counts per speaker)

### Test Configuration Setup
```python
def load_config_with_diarization():
    """Load configuration with diarization enabled for testing."""
    
def load_config_disabled():
    """Load configuration with diarization disabled for compatibility testing."""
```

## Specific E2E Test Implementation

### Test 1: Basic Diarization Detection
**Validates**: Core ML diarization functionality
**Input**: Multi-speaker conversation audio
**Success Criteria**:
- Detect 2+ speakers in conversation
- Speaker segments have valid timestamps (start < end)
- Speaker IDs are integers (0, 1, 2...)
- Segments cover full audio duration
- No overlapping segments
- Confidence scores > 0.0

### Test 2: Entity Assignment Integration  
**Validates**: Complete pipeline with speaker assignment
**Input**: Multi-speaker audio → full pipeline processing
**Success Criteria**:
- Entities assigned to detected speakers (not all speaker_id: 0)
- Speaker distribution matches conversation pattern
- All entities have valid integer speaker IDs
- Speaker changes align with segment boundaries
- Max speaker percentage < 80% (no single speaker dominance)

### Test 3: Speaker Labeling Post-Processing
**Validates**: CLI speaker naming functionality
**Input**: Processed database + name mapping
**Success Criteria**:
- Speaker names correctly assigned to IDs  
- Speaker map updated with human-readable names
- Entity speaker_ids remain unchanged
- Database format maintained

### Test 4: Single Speaker Fallback
**Validates**: Graceful single-speaker handling
**Input**: Single-speaker audio
**Success Criteria**:
- Single speaker audio processed without errors
- All entities assigned speaker_id: 0
- No spurious speaker detection
- Performance not degraded

### Test 5: Diarization Disabled Compatibility
**Validates**: Backward compatibility
**Input**: Any audio with diarization disabled
**Success Criteria**:
- Works exactly like current system
- All entities get speaker_id: 0
- No performance impact
- No additional dependencies loaded

## Test Implementation Focus

### Error Handling Validation
- Missing dependency graceful fallback
- Audio file error handling
- Configuration error handling
- Model loading failure handling

### Performance Validation
- Processing speed within 2-4x realtime
- Memory usage <2GB for 10min audio
- No performance regression when disabled

### Integration Validation
- Complete pipeline integration
- CLI command functionality
- Database format consistency
- Configuration system integration

## Success Criteria for Session 0
- All 5 E2E tests implemented and documented
- Test fixtures properly configured and accessible
- Tests run and properly validate expected failures (before implementation)
- Clear, measurable success criteria defined for each test
- Tests are comprehensive enough to validate complete system

## Post-Implementation Validation
These E2E tests will be the final validation that the entire diarization system works correctly. They define the exact behavior expected from the implementation and serve as immutable contracts for success.