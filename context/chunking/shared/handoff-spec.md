# Phase Handoff Specification

## Planning Phase Outputs (Context Packages)

- `COORDINATION-PLAN.md` - Execution sequence, timing estimates, dependency analysis
- `to_be_decided/chunk-[N]-[name]/CONTEXT.md` - Filtered behavioral contexts (levels 4-5)

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

**COORDINATION-PLAN**: Target Levels 2-4, focus on execution sequence
**CONTEXT**: Target Levels 4-5, filtered behavioral requirements only
**HANDOFF**: Target Levels 5-6, document actual implementation contracts

### Execution Simplicity Principle
Planning phase handles complexity through comprehensive context extraction and intelligent filtering. Execution agents receive focused contexts and maintain implementation flexibility.
