# Agent 4: Implementation Module Information

## Agent Purpose & Usage

**Primary Function**: Transforms Level 4 behavioral specifications into working code (Level 7 implementation) while ensuring all contracts are fulfilled through mandatory test validation.

**Core Responsibilities**:
- Transform behavioral specifications into executable test implementations
- Implement test-driven development workflow for chunk completion
- Generate stable handoff contracts for dependent chunks
- Validate implementation through comprehensive testing gates

**Sub-Agent Structure**:
- **test-generation/**: Transforms immutable Level 4 test specifications into executable test implementations
- **chunk-implementation/**: Executes test-driven implementation using generated tests as behavioral contracts

**Input Processing**:
- **CONTEXT.md** (Required): Level 4 behavioral specifications, interface contracts, implementation requirements, required test gates
- **HANDOFF.md** (Optional): Implementation summaries and integration contracts from dependent chunks

**Output Generation**:
- **HANDOFF.md**: Level 5-6 specifications, implementation summaries, integration requirements
- **Executable test implementations**: Complete test suites for validation
- **Working code implementations**: Test-driven implementations meeting all behavioral contracts

**Success Criteria**:
- All unit tests, integration tests, and chunk-level E2E tests pass
- Contract fulfillment achieved through test validation
- Complete handoff specifications provided for dependent chunks

## Agent Execution Logic & Sub-Agent Flow

**Sequential Processing Model**: Two specialized sub-agents operating in sequence with document-based handoffs.

### Sub-Agent 1: Test Generation
**Function**: Transform immutable test specifications into executable test implementations
**Input**: Level 4 test specifications + testing context from chunking module
**Output**: Executable E2E and integration test files, test support infrastructure

### Sub-Agent 2: Chunk Implementation  
**Function**: Test-driven implementation using generated tests as behavioral contracts
**Input**: Generated tests + behavioral specifications + integration contracts
**Output**: Working implementations + handoff documentation

### Execution Flow
```
Input Processing → Test Generation → Implementation → Test Validation → Handoff Generation
```

**Critical Constraints**:
- **Test Immutability**: E2E tests cannot be modified during implementation
- **Contract Fulfillment**: All tests must pass before completion
- **Stateless Operation**: Each sub-agent operates independently
- **Context Compliance**: All outputs respect infrastructure constraints

**Integration Points**:
- **Planning Module**: Receives immutable test specifications
- **Chunking Module**: Receives testing context and execution strategy
- **Dependent Chunks**: Provides stable integration contracts via handoff documentation