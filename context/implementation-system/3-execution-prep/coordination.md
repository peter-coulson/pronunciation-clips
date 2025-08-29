# Agent 3 Coordination: Execution Logic & Sub-Agent Flow

## Primary Agent Role

The Agent 3 coordinator provides simple sequential orchestration of the three execution preparation phases. It maintains no state and performs no validation - serving purely as an execution pipeline that loads each sub-agent with the appropriate context and handles failure scenarios.

## Execution Flow

### Sequential Pipeline
```
Phase 1: Boundary Analysis → Phase 2: Context Filtering → Phase 3: Coordination Synthesis
```

**Execution Logic**:
1. Execute Phase 1 with required inputs
2. On successful completion, execute Phase 2 with Phase 1 outputs + required inputs  
3. On successful completion, execute Phase 3 with Phase 1-2 outputs + required inputs
4. On successful completion, handoff final coordination plan to Agent 4

## Phase Orchestration

### Phase 1: Boundary Analysis
**Process**: Analyze system interfaces and behavioral dependencies to establish chunk boundaries
**Output**: `BOUNDARY_ANALYSIS_TEMPLATE.md`

### Phase 2: Context Filtering  
**Process**: Generate implementation-ready context templates for each chunk with testing standards
**Output**: `TEST_CONTEXT.md` + chunk-specific `CONTEXT_TEMPLATE.md` files

### Phase 3: Coordination Synthesis
**Process**: Integrate boundary analysis and context filtering into unified execution coordination plan
**Output**: `COORDINATION_PLAN.md`

## Error Handling

### Failure Response
**Policy**: Abort entire process on any phase failure
**Action**: Return control to user with failure details for debugging
**Rationale**: Phases have full context for validation - coordination agent cannot meaningfully recover from phase failures

### Error Propagation
- Phase failures immediately terminate the execution preparation process
- No retry logic or error recovery attempts
- User receives full error context for manual intervention

## Context Management

### Context Accumulation
The coordinator maintains access to original inputs throughout execution and accumulates phase outputs to provide subsequent phases with complete required context.

### Context Passing Protocol
Each phase receives required inputs:
- Original planning inputs (maintained throughout pipeline)  
- Previous phase outputs (accumulated as pipeline progresses)
- No additional context filtering or validation by coordinator

## Handoff Protocol

### To Agent 4 (Implementation)
**Deliverable**: Complete coordination plan from Phase 3
**Format**: Complete coordination plan with execution sequence and context templates
**Validation**: None (delegated to receiving agent)

## Operational Principles

1. **Simplicity**: No logic beyond sequential execution
2. **Delegation**: All validation and quality control handled by phases  
3. **Transparency**: Failures immediately surface to user with full context
4. **Statelessness**: No state maintained between executions