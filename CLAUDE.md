## CLAUDE.md — Pronunciation Clip Generator: MVP Objectives & Coding Practices

### Scope (MVP)
- Local-only inputs: accept audio files from disk; no URLs or cloud sources.
- Focus on a scalable pipeline; UI and long-term APIs are out of scope.

### Objectives (Specific)
- Separate stages: media preparation → transcription/alignment → selection → clip extraction/export.
- Support variable granularity: subword, word, phrase, sentence.
- Support multiple selection methods: input word list, syllable/length limits, sentence boundaries, simple quality/duration filters.
- Ensure quality: safe boundaries (no overlaps), configurable buffers, min/max duration, consistent sample rate/channels.
- Reproducible outputs: deterministic given inputs + config; log basic provenance.
- Scalable processing: stream/chunk long recordings; allow resumable runs; efficient batch file I/O.
- Proper data storage management for clips and words

### Best Coding Practices
- Single responsibility
  - Keep modules and functions focused; avoid hidden coupling.
  - Prefer pure, deterministic functions from explicit inputs + config.
- Clear contracts
  - Type hints on public functions; concise docstrings describing inputs/outputs and failure modes.
  - Avoid implicit globals; pass configuration explicitly.
- Error handling
  - Raise specific exceptions with context; do not swallow errors.
  - Validate inputs early (paths, durations, timestamps).
- Testing (prioritize failure cases)
  - Unit tests for boundary math (buffers, zero-gap, min/max duration).
  - Filename/path safety tests (accents/special chars, collisions).
  - Selection logic tests (word list, syllable/length, sentence splits).
- Configuration
  - Centralized config; no magic constants in code.
  - Environment overrides allowed but must be observable (e.g., logged).
- Performance & resiliency
  - Streaming I/O for long media; bounded memory usage.
  - Batch filesystem operations; atomic writes to prevent partial artifacts.
  - Resumable checkpoints at stage boundaries.
- Observability
  - Structured, leveled logging with context (source, stage, clip counts, timings).
  - Minimal metrics: processed duration, clips generated, failures, elapsed times.
- Files & metadata hygiene
  - Stable, human-readable filenames; path-safe normalization.
  - Consistent directory layout; do not duplicate raw sources in exports.
  - Record minimal provenance (config snapshot/hash and creation time).
  - Ensure the home directory is kept clean from temporary scripts after every checkpoint.

### Testing Strategy (CRITICAL)
- **E2E Test Immutability**: Once E2E test skeletons are created, they CANNOT be modified during implementation. This forces proper interface design upfront.
- **Test-First Progression**: No code implementation until its E2E test exists and defines success criteria.
- **Stage Gates**: Each stage's E2E test must pass completely before proceeding to next stage.
- **Real Audio Required**: Replace synthetic test fixtures with authentic Spanish audio samples.
- **Fixture Immutability**: Test audio files cannot be modified once E2E tests are written.
- **Performance Baselines**: Test audio must allow validation of performance thresholds (transcription speed, memory usage).

### Implementation Discipline
- **Sequential Development**: Stages 1-8 must be completed in exact order. No parallel development.
- **No Skipping**: Cannot proceed to Stage N+1 until Stage N's E2E test passes completely.
- **No Backtracking**: Once a stage's E2E test passes, its implementation is locked unless critical bugs found.
- **Test Layer Progression**: Unit → Integration → End-to-End. Each layer must pass before proceeding to next.

### Version Control Strategy
- **Checkpoint Commits**: Required git commit after each stage's E2E tests pass.
- **Atomic Stage Commits**: Each commit represents a fully functional, tested stage.
- **No Partial Commits**: Never commit incomplete implementations.
- **Commit Message Format**: "Stage N: [Description] complete - [E2E validation summary]"
- **Push Requirement**: MUST push to remote after every commit to ensure backup and progress tracking.

### Colombian Spanish Specific Requirements
- **Smart Buffering Implementation**: Fixed 50ms buffer causes word overlap in Colombian Spanish continuous speech.
- **Zero-Gap Detection**: Must check `word[n].end_time == word[n+1].start_time` before adding buffer.
- **Gap-Based Buffering**: Only add buffer when natural gaps exist between words.
- **Validated Configuration**: Use proven thresholds from Colombian Spanish testing (min_confidence: 0.8, syllable_range: [2, 6]).
