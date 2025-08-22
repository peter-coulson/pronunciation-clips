# Chunking System Workflow

## Input Structure
The input to this system will come from a combination of:
- Repository main context for generic project wide guidelines
- A highly detailed file containing all the necessary specifications for the chunking system to implement the changes

This should allow for very little decisions made by the chunking system as they should be predefined in this file or in the repository context.

## System Foundation
The foundation of the system is its test driven framework. This starts with the main predefined E2E testing scenarios in the input file. These E2E tests will be solely for the entire implementation and not at the chunk level.

## Agent Specialization
The system employs specialized agents coordinated by the main agent:
- **Input validation agent** - Validates specification file completeness and clarity
- **E2E setup agent** - Sets up and validates E2E tests (with separate permissions)
- **Chunking analysis agent** - Divides tasks into chunks and defines dependencies
- **Implementation agents** - Execute chunks in parallel where possible
- **Context update agent** - Updates main context system (possibly specialized)

**Coordination**: The main agent can coordinate up to 10 subagents simultaneously and handles final E2E validation and bug fixing directly (no separate final validation agent needed).

**Failure Handling**: For MVP, simple failure modes are implemented with iterative improvements planned. Agent coordination failures are escalated to the main agent for resolution.

## Permission System
- **E2E test protection**: Enforced via different agent permissions
- **Override mechanism**: Requires user decision when E2E tests need modification
- **Permission enforcement**: Maintained during implementation phase

## Communication System
- **Handoff templates**: Standardized markdown files built from templates between dependent agents
- **Template-based communication**: Ensures consistent information transfer between agents

**CRITICAL SUCCESS FACTOR**: Handoff document quality is the make-or-break element of the entire chunking system. High-quality handoffs enable zero-friction implementation and are essential for system effectiveness.

**Required Handoff Elements**:
- Comprehensive interface specifications with examples
- Complete integration patterns and context
- Error handling and fallback strategies
- Performance requirements and validation criteria
- Clear success criteria and testing requirements

**Reference Examples**: See `/context/chunking/examples/HANDOFF-2.md` and `/context/chunking/examples/DIARIZATION_CHUNK2_CONTEXT.md` for proven handoff patterns (load only with explicit user permission due to context size).

## Workflow Steps

### 1. Input Validation
The system should start by validating this file with a specific agent, checking it has all the necessary details and that it is clear.

### 2. E2E Test Setup
The chunking system will first set-up the E2E tests in the main tests folder and validate they are running. This should be done by an agent with separate permissions. Then all further agents will not have permissions to edit these files. We may need to override these whilst running due to bugs in the tests, however, that will be something the user must decide so permission restrictions hold.

### 3. Chunking Analysis
The system will then run a chunking analysis that will likely require a specialized agent, to divide the full tasks into chunks. The chunking division agent should also probably define:
- The success criteria and the tests for each chunk
- Any E2E tests that would be valuable across a few chunks
- Integration tests
- The dependency tree of chunks to determine which can be ran in parallel
- Any contracts if we are using them

### 4. Implementation
The system then implements the main code of the project, as defined by the chunking agent. Running the tasks in parallel if possible, and using handoff markdown files built from templates between dependent agents. The agent cannot mark the task complete without all tests passing unless there is some catastrophic failure.

**Failure Criteria**:
- **Test-passing requirement**: All tests must pass before task completion
- **Catastrophic failure exception**: Only exception to test-passing requirement
- **Distinction**: Clear separation between recoverable issues vs. catastrophic failure

### 5. Final Validation
Once all coding has been completed, the main agent will run the E2E tests + all other tests. It will implement any bug fixes it finds from these E2E tests until everything is working. It will then generate the final report with the full details of the implementation.

### 6. Context System Update
Then the main agent will update the main context system with the results of the chunking procedure and all relevant files. This may or may not need a specialized agent to be decided later. It will then also update a file tracking the general system success and review future implementations / optimizations.

## System Orchestration
The entirety of this will be ran by the main agent through claude code. The main agent will be keeping the rest of the context system up to date with progress as we go along, including the main claude.md file in the case of a failure.

**Coordination State Management**:
- **Main agent tracking**: Coordinates all specialized agents throughout process
- **Progress updates**: Continuous updates to context system during execution
- **CLAUDE.md updates**: Real-time updates, especially in case of failure
- **State consistency**: Maintains coordination state across agent hierarchy

## Target Scope
The target change size of this system is at minimum a large single file implementation and at maximum a medium to medium/large sized module.

---

## Proven Patterns from Experimental Implementation

*Note: These patterns were validated in the experimental diarization implementation but are not absolute requirements for the new system. They represent what worked effectively and should inform design decisions.*

### Context Management Patterns (Experimental Results)
- **Context Size**: 3-4K token contexts proved effective (vs original 2K target)
- **Context Sufficiency**: 4.8/5 average rating across implementation sessions
- **Context Organization**: Focused, relevant context eliminated decision paralysis and maintained velocity

### Contract-First Development (Experimental Results)
- **Interface Accuracy**: 95% contract prediction accuracy prevented integration issues
- **Upfront Design**: Interface contracts defined before implementation eliminated friction
- **Integration Reliability**: Zero integration failures between chunks when contracts were accurate

### Error Handling Framework (Experimental Results)
- **Graceful Degradation**: Systematic fallback patterns prevented cascade failures
- **Error Isolation**: Chunk boundaries provided effective error containment
- **Quality Validation**: Automated result validation with fallback mechanisms

### Implementation Velocity Patterns (Experimental Results)
- **Development Speed**: 120% of expected timeline (4.2 hours vs 5-7 hour target)
- **Focus Maintenance**: 4.8/5 average scope discipline across sessions
- **Sequential Dependencies**: Clear dependency chains enabled predictable implementation flow

### Quality Assurance Patterns (Experimental Results)
- **E2E Test Immutability**: Once defined, tests remained unchanged throughout implementation
- **Test-Driven Boundaries**: E2E tests naturally defined optimal chunk boundaries
- **Validation Effectiveness**: All technical targets achieved with comprehensive test coverage

*These patterns should be considered when designing the new automated system, but may be improved upon or adapted based on automation requirements and integration needs.*