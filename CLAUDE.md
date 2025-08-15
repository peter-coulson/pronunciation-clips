## CLAUDE.md — Pronunciation Clip Generator: MVP Objectives & Coding Practices

### Scope (MVP)
- Local-only inputs: accept audio/video files from disk; no URLs or cloud sources.
- Language/model agnostic, but implementation-neutral in this doc.
- Focus on a scalable pipeline; UI and long-term APIs are out of scope.

### Objectives (Specific)
- Separate stages: media preparation → transcription/alignment → selection → clip extraction/export.
- Support variable granularity: subword, word, phrase, sentence.
- Support multiple selection methods: input word list, syllable/length limits, sentence boundaries, simple quality/duration filters.
- Ensure quality: safe boundaries (no overlaps), configurable buffers, min/max duration, consistent sample rate/channels.
- Reproducible outputs: deterministic given inputs + config; log basic provenance.
- Scalable processing: stream/chunk long recordings; allow resumable runs; efficient batch file I/O.
- Produce clips and minimal metadata suitable for later search/flashcards.

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
