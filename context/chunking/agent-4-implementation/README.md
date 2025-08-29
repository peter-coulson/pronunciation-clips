# Agent 4: Implementation

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