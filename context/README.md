# Context Management System

## Purpose
This context system solves the token efficiency problem in complex Claude Code projects by implementing progressive disclosure of project information. Instead of loading all project details into every conversation, contexts are loaded only when relevant to the current task.

## Architecture

### Four-Domain Structure
```
/context/
├── domains/           # Core knowledge domains
├── workflows/         # Task-oriented contexts  
├── stages/            # Development stage contexts
└── reference/         # Quick lookup contexts
```

### Role Separation
- **CLAUDE.md**: Runtime navigation hub for Claude (< 30 lines)
- **Context files**: Detailed implementation knowledge loaded on demand
- **README.md**: Framework documentation (this file)

## Core Components

### domains/ - Knowledge Domains
- **architecture.md**: System design, patterns, dependencies
- **standards.md**: Coding practices, conventions, error handling
- **testing.md**: Test strategies, fixtures, validation rules
- **data.md**: Models, schemas, data processing logic
- **deployment.md**: Build, configuration, environment setup

### workflows/ - Task-Oriented Contexts
- **current-task.md**: Active work status and objectives
- **debugging.md**: Error patterns and troubleshooting approaches
- **extending.md**: Feature addition and scaling patterns
- **refactoring.md**: Code improvement strategies
- **performance.md**: Optimization approaches

### stages/ - Development Stage Contexts
- **stage1-foundation.md**: Core infrastructure setup
- **stage2-audio.md**: Audio processing implementation
- **[stage-N].md**: Stage-specific implementation details

### reference/ - Quick Lookup
- **apis.md**: Key interfaces and contracts
- **configs.md**: Settings, parameters, examples
- **troubleshooting.md**: Common issues and solutions

## Design Principles

### Progressive Disclosure
- Load only contexts relevant to current task
- CLAUDE.md provides lightweight navigation to detailed contexts
- Avoid token waste from unused information

### Single Source of Truth
- Each concept documented in exactly one context file
- Cross-references use explicit links: `See /context/domain/file.md`
- No duplication between contexts

### Token Efficiency
- Context files focused on single concerns
- Reference patterns instead of embedding detailed content
- Conditional loading based on task requirements

### Maintenance Discipline  
- Update contexts immediately after implementation changes
- Version control all context files with code changes
- Remove obsolete contexts to prevent confusion

## Usage Patterns

### New Chat Startup
Load: `CLAUDE.md` + `workflows/current-task.md`

### Implementation Work
Add: `domains/standards.md` + `domains/testing.md`

### Architecture Decisions
Add: `domains/architecture.md`

### Debugging Sessions
Add: `workflows/debugging.md`

### Stage Transitions
Update: relevant `stages/stage-N.md` files

## Benefits Achieved

### Token Efficiency
- **Before**: 72-line CLAUDE.md with all project details
- **After**: 29-line navigation hub + targeted context loading
- **Result**: ~60% reduction in baseline token usage

### Knowledge Organization
- Clear domain separation prevents context mixing
- Progressive detail levels (summary → implementation → reference)
- Easy navigation between related concepts

### Maintenance Simplicity
- Single location for each type of information
- Clear update responsibilities and timing
- Version-controlled knowledge evolution

## Context Loading Strategy

### By Task Type
1. **Research/Understanding**: Load relevant domain contexts
2. **Implementation**: Load standards + testing + stage contexts  
3. **Debugging**: Load debugging + troubleshooting contexts
4. **Architecture**: Load architecture + reference contexts

### By Development Phase
1. **Planning**: Load architecture + current-task contexts
2. **Building**: Load standards + testing + stage contexts
3. **Debugging**: Load debugging + troubleshooting contexts
4. **Extending**: Load extending + architecture contexts

## Maintenance Guidelines

### When to Update Contexts
- **Immediately** after stage completion
- **Before** starting new development phases  
- **When** adding new architectural patterns
- **During** refactoring or major changes

### What to Update
- `current-task.md`: After every significant milestone
- `architecture.md`: When patterns or dependencies change
- `stages/`: When implementation details are finalized
- `reference/`: When APIs or interfaces evolve

### How to Maintain Quality
- Keep context files focused on single concerns
- Test context effectiveness by starting fresh chats
- Remove contexts that are no longer relevant
- Ensure cross-references remain valid

## Framework Portability

This context system is designed for reuse across projects. The structure and principles remain constant while content adapts to specific implementations.

### Portable Elements
- Four-domain structure (domains/workflows/stages/reference)
- Progressive disclosure patterns
- Token efficiency principles
- Maintenance discipline

### Project-Specific Elements  
- Actual domain content (architecture decisions, standards)
- Stage definitions and progression
- Specific workflow patterns
- Reference materials and APIs

Future development will extract portable templates from this working implementation.