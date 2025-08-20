# CLAUDE.md — Pronunciation Clip Generator

## Current State
**Stage**: Foundation Setup  
**Phase**: Context System Implementation  
**Tests Status**: Not yet created

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

## Quick Commands
- **Tests**: `./pytest_venv.sh tests/e2e/ -v`
- **Stage Check**: Git status + test results validation
- **Clean Home**: Remove temp scripts after checkpoints

## Colombian Spanish Focus  
Zero-gap buffering for continuous speech processing (details in `/context/domains/data.md`)
