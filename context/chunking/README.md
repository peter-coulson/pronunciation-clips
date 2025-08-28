# Agent-Based Chunking System

A sequential agent system that transforms user specifications into implemented code through 4 independent agents. Each agent operates statelessly with document-based handoffs, enabling maximum simplicity, modularity, and operational robustness.

## Core Goals

1. **Maximum Simplicity** - Each directory = one complete, independent agent
2. **Perfect Modularity** - Zero dependencies between agent directories  
3. **Repository Agnostic** - Works with any codebase without complex setup
4. **Stateless Design** - Document-based handoffs enable independent agent execution

## Agent Structure

### Agent 1: Requirements [~4K tokens]
**Repository-agnostic requirements processing**
- **Location**: `agent-1-requirements/`
- **Process**: Input validation + knowledge mapping + context research  
- **Inputs**: User requirements template
- **Outputs**: Validated requirements + knowledge requirements + context extraction

### Agent 2: Planning [~8K tokens] 
**System specification generation**
- **Location**: `agent-2-planning/`
- **Process**: Architecture + interface + behavior specification
- **Inputs**: Complete knowledge foundation from Agent 1
- **Outputs**: System design specifications (L2-L4 specifications)

### Agent 3: Chunking [~6K tokens]
**Execution preparation & optimization** 
- **Location**: `agent-3-chunking/`
- **Process**: Boundary analysis + context filtering + coordination planning
- **Inputs**: System specifications from Agent 2
- **Outputs**: Execution strategy (coordination plan + context templates per chunk)

### Agent 4: Implementation [~8K tokens]
**Test-driven code generation**
- **Location**: `agent-4-implementation/`
- **Process**: Test generation + test-driven implementation + integration
- **Inputs**: Execution strategy from Agent 3
- **Outputs**: Working code + handoff documentation

## Agent Flow

```
Agent 1: Requirements → Agent 2: Planning → Agent 3: Chunking → Agent 4: Implementation
```

**Handoff Protocol**: Standardized file names with predictable relative paths
- Each agent knows exactly what files to expect from previous agents
- No file discovery or coordination overhead required
- Perfect independence maintained through the entire chain

## Directory Structure

### Development Structure (Current)
```
ABSTRACTION_FRAMEWORK.md           # Core framework
CLAUDE.md                          # Project instructions  
README.md                          # This file

agent-X-template/                  # General agent structure  
├── README.md                      # Agent purpose & usage
├── coordination.md                # Agent execution logic & sub-agent flow
└── sub-agent-name/               # Each sub-agent owns its complete functionality
    ├── methodology.md            # Sub-agent's specific methodology
    └── templates/                # Templates created by this sub-agent
        └── [output-templates]    # All outputs from this sub-agent

experiment/                        # Operational learnings (preserved)
```

### Operational Structure (Sessions)
```
sessions/
└── {session-name}/
    ├── 1-requirements/
    │   ├── requirements.md
    │   ├── knowledge-requirements.md
    │   └── context-extraction.md
    ├── 2-planning/
    │   ├── architecture.md
    │   ├── interface.md
    │   └── behavior.md
    ├── 3-chunking/
    │   ├── coordination-plan.md
    │   └── context-templates/
    └── 4-implementation/
        └── handoffs/
```

## Operational Benefits

**Perfect Independence**: Each agent knows exactly what files to expect, never needs discovery  
**Session Isolation**: Multiple projects/executions never interfere  
**System Independence**: No dependencies on external context system  
**Simple Cleanup**: Delete entire session directory  
**Clear Traceability**: Complete project flow in one session directory  
**Operational Robustness**: Supports concurrent sessions with different projects

## Token Efficiency

**Total System Capacity**: ~26K tokens across 4 agents (optimal distribution)
**Per-Agent Optimization**: Each agent operates within 4-8K token sweet spot
**No Token Waste**: Eliminated all duplicate methodology and coordination overhead