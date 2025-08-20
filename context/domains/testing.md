# Testing Strategy

## Critical Testing Rules
- **E2E Test Immutability**: Once E2E test skeletons are created, they CANNOT be modified during implementation. This forces proper interface design upfront
- **Test-First Progression**: No code implementation until its E2E test exists and defines success criteria
- **Stage Gates**: Each stage's E2E test must pass completely before proceeding to next stage
- **Real Audio Required**: Replace synthetic test fixtures with authentic Spanish audio samples
- **Fixture Immutability**: Test audio files cannot be modified once E2E tests are written
- **Performance Baselines**: Test audio must allow validation of performance thresholds (transcription speed, memory usage)

## Implementation Discipline
- **Sequential Development**: Stages 1-8 must be completed in exact order. No parallel development
- **No Skipping**: Cannot proceed to Stage N+1 until Stage N's E2E test passes completely
- **No Backtracking**: Once a stage's E2E test passes, its implementation is locked unless critical bugs found
- **Test Layer Progression**: Unit → Integration → End-to-End. Each layer must pass before proceeding to next

## Test Coverage Requirements
- Unit tests for boundary math (buffers, zero-gap, min/max duration)
- Filename/path safety tests (accents/special chars, collisions)
- Selection logic tests (word list, syllable/length, sentence splits)

## Version Control Strategy
- **Checkpoint Commits**: Required git commit after each stage's E2E tests pass
- **Atomic Stage Commits**: Each commit represents a fully functional, tested stage
- **No Partial Commits**: Never commit incomplete implementations
- **Commit Message Format**: "Stage N: [Description] complete - [E2E validation summary]"
- **Push Requirement**: MUST push to remote after every commit to ensure backup and progress tracking