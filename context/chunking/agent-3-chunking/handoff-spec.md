# Phase Handoff Specification

## Planning Phase Outputs (Context Packages)

- `COORDINATION-PLAN.md` - Execution sequence, timing estimates, dependency analysis
- `TEST_CONTEXT.md` - Testing framework constraints, infrastructure patterns, quality standards
- `to_be_decided/chunk-[N]-[name]/CONTEXT.md` - Filtered behavioral contexts (levels 4-5)

## Template Abstraction Level Analysis

### Target Abstraction Levels

#### COORDINATION_PLAN_TEMPLATE.md: Level 2
- **Level 2**: System coordination, component dependencies, execution architecture

#### TEST_CONTEXT_TEMPLATE.md: Level 2  
- **Level 2**: Testing infrastructure, framework constraints, system patterns

#### CONTEXT_TEMPLATE.md: Level 4 + Upstream Context
- **Level 4**: Testing requirements, behavioral specifications, performance criteria
- **Level 3**: Interface contracts from previous chunks (always required)
- **Level 2**: System placement, integration points (when chunk integrates with existing systems)

### Execution Simplicity Principle
Planning phase handles complexity through comprehensive context extraction and intelligent filtering. Execution agents receive focused contexts and maintain implementation flexibility.
