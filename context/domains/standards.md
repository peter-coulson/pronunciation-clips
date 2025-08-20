# Standards & Practices

## Single Responsibility
- Keep modules and functions focused; avoid hidden coupling
- Prefer pure, deterministic functions from explicit inputs + config

## Clear Contracts
- Type hints on public functions; concise docstrings describing inputs/outputs and failure modes
- Avoid implicit globals; pass configuration explicitly

## Error Handling
- Raise specific exceptions with context; do not swallow errors
- Validate inputs early (paths, durations, timestamps)

## Configuration
- Centralized config; no magic constants in code
- Environment overrides allowed but must be observable (e.g., logged)

## Performance & Resiliency
- Streaming I/O for long media; bounded memory usage
- Batch filesystem operations; atomic writes to prevent partial artifacts
- Resumable checkpoints at stage boundaries

## Observability
- Structured, leveled logging with context (source, stage, clip counts, timings)
- Minimal metrics: processed duration, clips generated, failures, elapsed times

## Files & Metadata Hygiene
- Stable, human-readable filenames; path-safe normalization
- Consistent directory layout; do not duplicate raw sources in exports
- Record minimal provenance (config snapshot/hash and creation time)
- Ensure the home directory is kept clean from temporary scripts after every checkpoint