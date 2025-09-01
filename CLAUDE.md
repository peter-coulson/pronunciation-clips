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
- **Diarization Tests**: `./pytest_venv.sh tests/e2e/test_diarization_e2e.py -m quick -v` (~9s)
- **Stage Check**: Git status + test results validation
- **Clean Home**: Remove temp scripts after checkpoints

## Colombian Spanish Focus  
Zero-gap buffering for continuous speech processing (details in `/context/domains/data.md`)
