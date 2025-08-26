# Agent-Based Chunking System

A two-phase chunking system that separates planning from execution. Phase 1 analyzes user specifications and determines optimal chunk divisions. Phase 2 implements the defined chunks. This division enables clean handoffs and focused development of each phase.

## Core Goals

1. **Clear Phase Separation** - Distinct planning and execution phases with clean handoffs
2. **Preserve Claude's Judgment** - Leverage proven architectural decision-making capabilities  
3. **Repository Agnostic** - Works with any codebase without complex setup
4. **Leverage Proven Patterns** - Built on experiment results (execution phase: 4.8/5 context management, 95% interface specification accuracy; planning phase was manually orchestrated)

## System Architecture

### Three-Phase Design

**Phase 1: Planning & Chunk Division**
- Analyzes user specifications
- Determines optimal chunk boundaries  
- Outputs standardized chunk definitions
- No implementation work

**Phase 2: Chunk Execution**  
- Receives validated chunk specifications
- Implements defined chunks
- Produces integrated results
- Separate system (future development)

**Phase 3: Main Agent Integration**
- Creates unified orchestration agent
- Combines Phase 1 and Phase 2 systems
- Provides seamless end-to-end automation
- Final system integration (future development)

### Repository Structure
```
repository/
├── .claude/agents/
│   ├── chunking-main.md           # Main agent (orchestrates both phases)
│   ├── chunk-planner.md           # Phase 1 specialist
│   └── chunk-executor.md          # Phase 2 specialist
├── context/
│   └── chunking/
│       ├── shared/                # Shared components
│       │   ├── workflow.md        # Overall end-to-end workflow
│       │   ├── coordination.md    # Main agent orchestration
│       │   └── handoff-spec.md    # Phase 1 → Phase 2 interface
│       ├── planning/              # Phase 1 components
│       │   ├── ABSTRACTION_FRAMEWORK.md  # Core specification levels & knowledge framework
│       │   ├── methodology/       # Context-and-requirements agent implementation
│       │   │   └── context-and-requirements/  # Agent coordination and processes
│       │   └── templates/         # Input specs, knowledge requirements, context extraction
│       ├── execution/             # Phase 2 components
│       │   ├── methodology/       # Implementation coordination
│       │   ├── instructions/      # Execution specialist behaviors
│       │   ├── templates/         # Implementation handoffs
│       │   └── sessions/          # Active implementation sessions
│       └── experiments/           # Proven results
└── src/                           # Implementation code
```

### Component Interaction

**Current State (Phase 1 Development):**
- Planning components operate independently
- Manual handoff to future execution system
- Shared components define interface standards

**Future State (Phases 2-3):**
- Main agent orchestrates both phases
- Standardized handoff specifications enable seamless transitions
- Execution system validates and implements planning outputs

## Current Development Focus

**Phase 1 System** - Currently under development:
- Context-and-Requirements Agent: Validates input templates, generates knowledge requirements, and extracts available context
- Specification transformation through 7-level progression (Requirements → Implementation)
- Risk-knowledge mapping for systematic context identification
- Clean handoff format definition for downstream planning

**Phase 2 System** - Future development:
- Will receive standardized chunk specifications
- Implementation coordination and execution  
- Result integration and validation
- Based on proven experimental patterns

**Phase 3 System** - Final integration:
- Unified main agent development
- End-to-end automation
- Complete system orchestration

## Experimental Context

The proven effectiveness metrics (4.8/5 context management, 95% interface specification accuracy) apply specifically to the execution phase patterns. The original planning phase was manually orchestrated, making Phase 1 development a new automation challenge.