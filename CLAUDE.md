# CLAUDE.md — Pronunciation Clip Generator

## Current State
**Primary Focus**: Chunking System Automation Development
**Stage**: Implementation Phase 2A - Core Automation Systems  
**Phase**: Building automated chunking based on proven experiment results
**Foundation**: Diarization chunking experiment achieved 5/5 effectiveness, 95% contract accuracy

## Core Rules
- **E2E Test Immutability**: Once created, E2E tests CANNOT be modified during implementation
- **Sequential Stages**: Must complete stages 1-8 in exact order. No skipping or parallel development
- **Stage Gates**: Each stage's E2E test must pass completely before proceeding
- **Test Progression**: Unit → Integration → End-to-End. Each layer must pass before next
- **Commit Discipline**: Git commit only after stage completion with all tests passing

## Context Navigation
- **Architecture & Design**: `/context/domains/architecture.md`
- **Standards & Practices**: `/context/domains/standards.md`  
- **Testing Strategy**: `/context/domains/testing.md`
- **Current Work**: `/context/workflows/current-task.md`
- **Stage Details**: `/context/stages/stage1-foundation.md`

## Chunking System Development
**Implementation Plan**: `CHUNKING_AUTOMATION_IMPLEMENTATION_PLAN.md` - Complete Phase 2A automation roadmap
**Context Organization**: `/context/chunking/README.md` - Organized experiment results and examples

### Chunking Context Loading
- **Critical Reference**: `/context/chunking/experiment/CHUNKING_LEARNINGS_LOG.md` - Proven 5/5 effectiveness results
- **Gold Standard Examples**: `/context/chunking/examples/HANDOFF-2.md` - Perfect handoff template
- **Context Templates**: `/context/chunking/examples/DIARIZATION_CHUNK2_CONTEXT.md` - Effective 3.5K token context
- **Framework Background**: `/context/chunking/framework/` - Design evolution and planning history

## Quick Commands
- **Tests**: `./pytest_venv.sh tests/e2e/ -v`
- **Stage Check**: Git status + test results validation
- **Clean Home**: Remove temp scripts after checkpoints

## Colombian Spanish Focus  
Zero-gap buffering for continuous speech processing (details in `/context/domains/data.md`)
