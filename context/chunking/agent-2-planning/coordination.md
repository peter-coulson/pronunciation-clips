# Agent 2: Planning Coordination

## Execution Logic
Sequential execution of two independent sub-agents that transform requirements into implementation specifications through Level 4.

## Sub-Agent Flow

### Phase 1: Architecture-Interface Sub-Agent
**Location**: `architecture-interface/`
**Inputs**: 
- REQUIREMENTS_LEVEL_INPUT.md
- CONTEXT_EXTRACTION_OUTPUT.md

**Process**: Execute architecture-interface sub-agent methodology
**Outputs**: 
- Level 2 Architecture Specification
- Level 3 Interface Specification

**Failure Handling**: If Phase 1 fails, halt entire Agent 2 execution and raise issue to user.

### Phase 2: Behavior-Specification Sub-Agent  
**Location**: `behaviour-specification/`
**Inputs**:
- REQUIREMENTS_LEVEL_INPUT.md (original)
- CONTEXT_EXTRACTION_OUTPUT.md (original)
- Level 2 Architecture Specification (from Phase 1)
- Level 3 Interface Specification (from Phase 1)

**Process**: Execute behavior-specification sub-agent methodology
**Outputs**:
- Level 4 Behavior Specification
- Level 4 E2E Test Specification  
- Level 4 Integration Test Specification

## Context Handoffs
**Template Location**: Each sub-agent outputs to its own `templates/` directory
**Handoff Method**: Phase 2 sub-agent reads completed templates from Phase 1 sub-agent's templates directory

## Coordination Responsibilities
1. Execute architecture-interface sub-agent first
2. Verify Phase 1 completion before proceeding
3. Execute behaviour-specification sub-agent second
4. Provide template locations to sub-agents
5. Handle execution failures by stopping and reporting to user

**Note**: Sub-agents operate entirely independently - coordination layer only manages execution sequence and template location references.