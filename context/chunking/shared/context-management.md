# Context Management for Chunked Implementation

## Key Insight from Experiment
Chunks cannot operate with only HANDOFF and CONTEXT specification documents. Each chunk requires a **complete context package** including targeted repository context.

## Context Package Components

### 1. Specification Documents (1-2K tokens)
- **HANDOFF document** from previous chunk (workflow + interfaces)
- **CONTEXT document** for current chunk (focused requirements)

### 2. Repository Context (2-3K tokens)
- **Target files** for modification (specific source files to change)
- **Integration points** (existing classes/modules to interface with)  
- **Pattern references** (similar existing implementations to follow)
- **Configuration files** (config and environment setup)
- **Related test files** (existing test patterns and structures)

## Context Selection Strategy

### What to Include
- **Direct modification targets** - Files this chunk will edit
- **Integration dependencies** - Files this chunk will call/import
- **Established patterns** - Similar existing implementations for consistency
- **Quality references** - Test structures and coding standards

### What to Exclude
- **Unrelated modules** - Code not connected to this chunk's scope
- **Full repository** - Avoid information overload
- **Implementation details** - Focus on interfaces and patterns

## Evidence from Experiment

**Average context per session**: 3-4K tokens (not 2K as originally targeted)
**Context sufficiency rating**: 4.8/5 across all sessions
**Missing context issues**: Occurred when repository integration points weren't provided
**Context quality**: High-quality handoffs + targeted repository context = zero integration failures