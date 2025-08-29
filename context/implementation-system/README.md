# Stage-Based Implementation System

A sequential processing system that transforms user specifications into implemented code through 4 independent stages. Each stage operates with isolated processing and document-based handoffs, enabling maximum simplicity, modularity, and operational robustness.

## Core Goals

1. **Maximum Simplicity** - Each directory = one complete, independent stage
2. **Perfect Modularity** - Zero dependencies between stage directories  
3. **Repository Agnostic** - Works with any codebase without complex setup
4. **Stateless Design** - Document-based handoffs enable independent stage execution

## Stage Structure

### Stage 1: Requirements 
**Repository-agnostic requirements processing**
- **Location**: `1-requirement-analysis/`
- **Process**: Input validation + knowledge mapping + context research  
- **Inputs**: User requirements template
- **Outputs**: Validated requirements + knowledge requirements + context extraction

### Stage 2: Planning 
**System specification generation**
- **Location**: `2-specification-design/`
- **Process**: Architecture + interface + behavior specification
- **Inputs**: Complete knowledge foundation from Stage 1
- **Outputs**: System design specifications (L2-L4 specifications)

### Stage 3: Execution Preparation 
**Execution preparation & optimization** 
- **Location**: `3-implementation-preparation/`
- **Process**: Implementation segmentation + context filtering + coordination planning
- **Inputs**: System specifications from Stage 2
- **Outputs**: Execution strategy (coordination plan + context templates per unit)

### Stage 4: Implementation 
**Test-driven code generation**
- **Location**: `4-code-generation/`
- **Process**: Test generation + test-driven implementation + integration
- **Inputs**: Execution strategy from Stage 3
- **Outputs**: Working code + handoff documentation

## Stage Flow

```
Stage 1: Requirements → Stage 2: Planning → Stage 3: Execution Preparation → Stage 4: Implementation
```

**Handoff Protocol**: Standardized file names with predictable relative paths
- Each stage knows exactly what files to expect from previous stages
- No file discovery or coordination overhead required
- Perfect independence maintained through the entire chain

## Directory Structure

### Development Structure (Current)
```
ABSTRACTION_FRAMEWORK.md           # Core framework
CLAUDE.md                          # Project instructions  
README.md                          # This file

X-template/                        # General stage structure  
├── README.md                      # Stage purpose & usage
├── coordination.md                # Stage execution logic & sub-process flow
└── sub-process-name/             # Each sub-process owns its complete functionality
    ├── methodology.md            # Sub-process's specific methodology
    └── templates/                # Templates created by this sub-process
        └── [output-templates]    # All outputs from this sub-process

proof-of-concept/                  # Operational learnings (preserved)
```

### Operational Structure (Sessions)
```
sessions/
└── {session-name}/
    ├── 1-requirement-analysis/
    │   ├── requirements-input.md
    │   ├── knowledge-requirements.md
    │   └── context-extraction.md
    ├── 2-specification-design/
    │   ├── architecture-specification.md
    │   ├── interface-specification.md
    │   └── behavior-specification.md
    ├── 3-implementation-preparation/
    │   ├── coordination-plan.md
    │   └── context-templates/
    └── 4-code-generation/
        └── handoffs/
```

## Template Naming Standards

**Template Convention:** `{ROLE}_{TYPE}_TEMPLATE.md`
- Templates are stored in `sub-process-name/templates/` directories
- All templates use UPPERCASE with underscores and `_TEMPLATE.md` suffix

**Filled Template Convention:** `{role}-{type}.md`
- Filled templates use lowercase with hyphens
- Direct correspondence to template names for easy traceability

## Operational Benefits

**Perfect Independence**: Each stage knows exactly what files to expect, never needs discovery  
**Session Isolation**: Multiple projects/executions never interfere  
**System Independence**: No dependencies on external context system  
**Simple Cleanup**: Delete entire session directory  
**Clear Traceability**: Complete project flow in one session directory  
**Operational Robustness**: Supports concurrent sessions with different projects
