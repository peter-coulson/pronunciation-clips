# Stage 4: Implementation Coordination

## Stage Execution Logic & Sub-Process Flow

**Sequential Processing Model**: Two specialized sub-processes operating in sequence with document-based handoffs.

### Sub-Process 1: Test Implementation
**Function**: Transform immutable test specifications into executable test implementations
**Input**: Level 4 test specifications + testing context from execution preparation module
**Output**: Executable E2E and integration test files, test support infrastructure

### Sub-Process 2: Segmented Implementation  
**Function**: Test-driven implementation using generated tests as behavioral contracts
**Input**: Generated tests + behavioral specifications + integration contracts
**Output**: Working implementations + handoff documentation

## Execution Flow

```
Test Generation → Implementation → Final Validation → Complete
```

### Stage 1: Test Implementation Sub-Process
- Execute test-implementation/ sub-process
- **Success**: Executable test files created + sub-process reports SUCCESS
- **Critical Failure**: Sub-process cannot resolve E2E/integration test issues OR other unresolvable problems → Return control to user

### Stage 2: Implementation Sub-Process
- Execute segmented-implementation/ sub-process  
- **Success**: Working code + HANDOFF.md created + all tests pass + sub-process reports SUCCESS
- **Critical Failure**: Sub-process cannot resolve test failures OR other unresolvable problems → Return control to user

### Stage 3: Final Validation
- Verify HANDOFF.md exists
- Verify working implementation files exist
- **Success**: Stage 4 complete
- **Critical Failure**: Missing outputs → Return control to user

## Critical Constraints

- **Test Immutability**: E2E tests cannot be modified during implementation
- **Contract Fulfillment**: All tests must pass before completion
- **Stateless Operation**: Each sub-process operates independently
- **Context Compliance**: All outputs respect infrastructure constraints
- **Critical Failure Definition**: Any problem sub-processes cannot resolve independently

## Progress Tracking

**Implementation Status**: Update CLAUDE.md with current stage:
```
# Stage 4 Implementation Status
Last Completed Stage: [Stage 1: Test Generation | Stage 2: Implementation | Stage 3: Final Validation]
```

## Integration Points

- **Planning Module**: Receives immutable test specifications
- **Execution Preparation Module**: Receives testing context and execution strategy
- **Dependent Units**: Provides stable integration contracts via handoff documentation