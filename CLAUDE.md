# CLAUDE.md — Pronunciation Clip Generator

## Context Navigation
- **Architecture & Design**: `/context/domains/architecture.md`
- **Standards & Practices**: `/context/domains/standards.md`  
- **Testing Strategy**: `/context/domains/testing.md`
- **Current Work**: `/context/workflows/current-task.md`
- **Stage Details**: `/context/stages/stage1-foundation.md`
- **System Principles**: `/context/PRINCIPLES.md`

## Quick Commands
- **Quick Tests**: `./pytest_venv.sh tests/ -m quick -v` (~12s)
- **Full Tests**: `./pytest_venv.sh tests/ -v` (~25s)  
- **Diarization Tests**: `ENABLE_DIARIZATION_TESTS=true ./pytest_venv.sh tests/e2e/test_diarization_e2e.py -m quick -v` (~9s)
- **Transcription Tests**: `./pytest_venv.sh tests/e2e/test_stage3_transcription_e2e.py -v` (~4s)
- **Stage Check**: Git status + test results validation
- **Clean Home**: Remove temp scripts after checkpoints

## Implementation Options
- **Transcription**: faster-whisper with CPU optimization
- **Diarization**: PyAnnote with MPS acceleration and pipeline caching
- **Batch Processing**: Optimized multi-file processing with model caching

## Colombian Spanish Focus  
Zero-gap buffering for continuous speech processing (details in `/context/domains/data.md`)
