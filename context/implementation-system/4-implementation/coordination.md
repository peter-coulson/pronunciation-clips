# Agent 4: Implementation Coordination

## Agent Execution Logic & Sub-Agent Flow

**Sequential Processing Model**: Two specialized sub-agents operating in sequence with document-based handoffs.

### Sub-Agent 1: Test Generation
**Function**: Transform immutable test specifications into executable test implementations
**Input**: Level 4 test specifications + testing context from chunking module
**Output**: Executable E2E and integration test files, test support infrastructure

### Sub-Agent 2: Unit Implementation  
**Function**: Test-driven implementation using generated tests as behavioral contracts
**Input**: Generated tests + behavioral specifications + integration contracts
**Output**: Working implementations + handoff documentation

## Execution Flow

```
Test Generation → Implementation → Final Validation → Complete
```

### Stage 1: Test Generation Sub-Agent
- Execute test-generation/ sub-agent
- **Success**: Executable test files created + sub-agent reports SUCCESS
- **Critical Failure**: Sub-agent cannot resolve E2E/integration test issues OR other unresolvable problems → Return control to user

### Stage 2: Implementation Sub-Agent
- Execute unit-implementation/ sub-agent  
- **Success**: Working code + HANDOFF.md created + all tests pass + sub-agent reports SUCCESS
- **Critical Failure**: Sub-agent cannot resolve test failures OR other unresolvable problems → Return control to user

### Stage 3: Final Validation
- Verify HANDOFF.md exists
- Verify working implementation files exist
- **Success**: Agent 4 complete
- **Critical Failure**: Missing outputs → Return control to user

## Critical Constraints

- **Test Immutability**: E2E tests cannot be modified during implementation
- **Contract Fulfillment**: All tests must pass before completion
- **Stateless Operation**: Each sub-agent operates independently
- **Context Compliance**: All outputs respect infrastructure constraints
- **Critical Failure Definition**: Any problem sub-agents cannot resolve independently

## Progress Tracking

**Implementation Status**: Update CLAUDE.md with current stage:
```
# Agent 4 Implementation Status
Last Completed Stage: [Stage 1: Test Generation | Stage 2: Implementation | Stage 3: Final Validation]
```

## Integration Points

- **Planning Module**: Receives immutable test specifications
- **Execution Preparation Module**: Receives testing context and execution strategy
- **Dependent Units**: Provides stable integration contracts via handoff documentation