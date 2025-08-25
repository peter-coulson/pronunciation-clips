# Phase Handoff Specification

## Planning Phase Outputs (Context Packages)

- `COORDINATION-PLAN.md` - Detailed execution sequence, timing estimates, checkpoints, dependency analysis
- `to_be_decided/chunk-[N]-[name]/CONTEXT.md` - Complete implementation contexts

## Execution Phase Outputs (Handoff Documents)

- `to_be_decided/chunk-[N]-[name]/HANDOFF.md` - Handoff to the next dependent agent

## Template Abstraction Level Analysis

### Target Abstraction Levels

#### COORDINATION-PLAN.md: Levels 2-4
- **Level 2**: Execution sequence, architectural patterns, dependency analysis
- **Level 3**: Context packages, integration boundaries, major interfaces  
- **Level 4**: Quality gates, validation criteria, checkpoint requirements

#### CONTEXT_TEMPLATE.md: Levels 4-5
- **Level 4**: Testing requirements, behavioral specifications, performance criteria
- **Level 5**: Implementation strategy, algorithmic approaches, code structure templates

#### HANDOFF_TEMPLATE.md: Levels 5-6
- **Level 5**: Algorithm specifications, integration patterns, implementation workflows
- **Level 6**: Exact method contracts, import statements, integration method signatures

### Planning Agent Guidelines

**COORDINATION-PLAN**: Target Levels 2-4, avoid implementation details
**CONTEXT**: Target Levels 4-5, avoid function signatures  
**HANDOFF**: Require Levels 5-6, ensure tested implementation contracts
