# Phase Handoff Specification

## Planning Phase Outputs (Context Packages)

- `COORDINATION-PLAN.md` - Execution sequence, timing estimates, dependency analysis
- `to_be_decided/chunk-[N]-[name]/CONTEXT.md` - Filtered behavioral contexts (levels 4-5)

## Execution Phase Outputs (Handoff Documents)

- `to_be_decided/chunk-[N]-[name]/HANDOFF.md` - Handoff to the next dependent agent

## Template Abstraction Level Analysis

### Target Abstraction Levels

#### CONTEXT_TEMPLATE.md: Levels 4
- **Level 4**: Testing requirements, behavioral specifications, performance criteria

#### HANDOFF_TEMPLATE.md: Levels 5-6
- **Level 5**: Algorithm specifications, integration patterns, implementation workflows
- **Level 6**: Exact method contracts, import statements, integration method signatures

### Execution Simplicity Principle
Planning phase handles complexity through comprehensive context extraction and intelligent filtering. Execution agents receive focused contexts and maintain implementation flexibility.
