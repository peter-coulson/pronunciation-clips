# Architecture & Design

## MVP Scope
- Local-only inputs: accept audio files from disk; no URLs or cloud sources
- Focus on a scalable pipeline; UI and long-term APIs are out of scope

## System Architecture
Separate stages: media preparation → transcription/alignment → selection → clip extraction/export

## Design Objectives
- Support variable granularity: subword, word, phrase, sentence
- Support multiple selection methods: input word list, syllable/length limits, sentence boundaries, simple quality/duration filters
- Ensure quality: safe boundaries (no overlaps), configurable buffers, min/max duration, consistent sample rate/channels
- Reproducible outputs: deterministic given inputs + config; log basic provenance
- Scalable processing: stream/chunk long recordings; allow resumable runs; efficient batch file I/O
- Proper data storage management for clips and words

## Module Structure
*To be defined during stage-specific architecture design*