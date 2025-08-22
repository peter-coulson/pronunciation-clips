# Chunking System Workflow

## Input Structure
The input to this system will come from a combination of:
- Repository main context for generic project wide guidelines
- A highly detailed file containing all the necessary specifications for the chunking system to implement the changes

This should allow for very little decisions made by the chunking system as they should be predefined in this file or in the repository context.

## System Foundation
The foundation of the system is its test driven framework. This starts with the main predefined E2E testing scenarios in the input file. These E2E tests will be solely for the entire implementation and not at the chunk level.

## Scale Requirements & Automation Justification

### **Scope Expansion Context**
This system targets implementation scopes significantly larger than the experimental MVP:
- **Experimental MVP**: 5 chunks, 4.2 hours, manual coordination feasible
- **Target Scope**: 15-20 chunks (medium to medium/large modules), requiring systematic automation
- **Coordination Complexity**: Manual approaches scale poorly (O(n²) handoff complexity)

### **Why Automation is Critical at Scale**
At 15-20 chunks, manual coordination becomes a bottleneck:
- **Context Assembly**: 15-20 context files requiring manual creation and maintenance
- **Dependency Management**: Complex inter-chunk relationships requiring systematic tracking  
- **Handoff Quality**: 15-20 critical handoff documents that must maintain experimental standards
- **Error Recovery**: Manual determination of restart points when chunks fail mid-implementation

**Conclusion**: Coordination overhead would exceed implementation time without automation. The chunking system provides essential orchestration for complex module development.

## System Architecture Validation

### **Claude Code Tool Constraints**
The system design works within Claude Code's current limitations:
- **Task Tool**: Stateless agent invocation - agents receive complete context via documents
- **No Native Coordination**: Dependency management handled through upfront planning rather than runtime coordination
- **Document-Based Communication**: File system handoffs align with available tools

### **Architecture Strengths**
- **Complexity Isolation**: Planning complexity contained in Chunking Analysis Agent
- **Tool Alignment**: Task tool perfect for focused, single-purpose implementation agents
- **Failure Isolation**: Clear boundaries for debugging and restart scenarios
- **Sequential Execution**: Eliminates parallel coordination complexity while maintaining benefits

### **Chunk Scale Limits & Validation**

#### **Minimum Chunk Threshold: 4 chunks**
**Rationale**: Below 4 chunks, coordination overhead exceeds chunking benefits:
- **Fixed Coordination Cost**: Template setup, context preparation, and main agent orchestration represent significant overhead
- **Tool Overhead**: Task agent invocation and document-based handoffs have per-chunk costs
- **Experimental Validation**: 5-chunk MVP worked well, suggesting 4 is practical minimum
- **User Decision Point**: Modules requiring <4 chunks should use standard single-session implementation

#### **Maximum Chunk Threshold: 25 chunks**  
**Rationale**: Above 25 chunks, sequential coordination becomes unwieldy:
- **Sequential Time Scaling**: No parallel benefits mean linear time growth with coordination overhead
- **Context Management Burden**: 25+ contexts (75-100K total tokens) approaches management complexity limits
- **Main Agent Coordination**: Human review and validation capacity constraints
- **Error Recovery Complexity**: More chunks increase potential failure points and restart complexity
- **Handoff Quality Risk**: Quality maintenance becomes difficult at scale without very careful oversight

#### **Optimal Range: 8-20 chunks**
Based on experimental results and system design:
- **Proven Range**: 15-20 chunks identified as target for "medium to medium/large modules"  
- **Sweet Spot**: 8-12 chunks for most modules requiring chunking approach
- **Quality Maintenance**: Handoff quality easier to maintain in this range
- **Coordination Efficiency**: Main agent coordination remains manageable

#### **Pre-Implementation Validation Requirements**
The **Chunking Analysis Agent** must provide rough chunk count estimates and validate against limits:

**Required Outputs**:
- **Estimated Chunk Count**: [X] chunks based on module analysis
- **Scale Validation**: ✅/⚠️/❌ within recommended limits (4-25 chunks)
- **Scope Recommendation**: 
  - `<4 chunks`: "Consider single-session implementation instead"
  - `4-25 chunks`: "Chunking system recommended" 
  - `>25 chunks`: "WARNING: Approaching coordination complexity limits - consider module decomposition"

**User Decision Points**:
- **Below minimum**: System should recommend against chunking approach
- **Above maximum**: System should warn about coordination complexity and suggest module splitting
- **Edge cases**: User can override with explicit acknowledgment of trade-offs

## Agent Specialization

### **Planning Phase Agents**
The system employs specialized agents for upfront analysis and preparation:

#### **Input Validation Agent**
- **Purpose**: Validates specification file completeness and clarity
- **Output**: Validation report to main agent identifying gaps or issues
- **Success Criteria**: Specification contains all required elements for chunking system

#### **E2E Setup Agent**  
- **Purpose**: Sets up and validates E2E tests with separate permissions
- **Output**: Test setup report confirming E2E tests are operational
- **Permission Model**: Only agent with E2E test modification rights
- **Success Criteria**: All E2E tests can be executed and have clear pass/fail states

#### **Chunking Analysis Agent** (Critical Success Path)
- **Purpose**: Performs comprehensive module analysis and creates all coordination artifacts
- **Pre-Analysis Validation**:
  - **Chunk Count Estimation**: Provide rough estimate of required chunks (4-25 range validation)
  - **Scale Assessment**: Validate scope is appropriate for chunking system vs single-session implementation
  - **Complexity Analysis**: Assess if module benefits from chunking approach
- **Core Outputs**:
  - `SCALE-VALIDATION.md` - Chunk count estimate and scale appropriateness assessment  
  - `DEPENDENCY-CHART.md` - Sequential execution order for main agent
  - `COORDINATION-PLAN.md` - Detailed execution sequence and timing
  - `chunks/chunk-[N]-[name]/CONTEXT.md` - Ready-to-use contexts for each implementation agent
  - `chunks/chunk-[N]-[name]/CONTRACTS.yaml` - Interface specifications and validation criteria
- **Analysis Scope**: 
  - **Scale Validation**: Chunk count estimation and appropriateness assessment against 4-25 limits
  - Module decomposition into optimal chunk boundaries
  - Sequential dependency chain mapping (no parallel complexity)
  - Interface contract definition between chunks
  - Context preparation for implementation agents
- **Success Criteria**: 
  - Scale validation complete with user decision point if outside recommended limits
  - All implementation contexts are complete and require no additional analysis
  - Chunk count within operational range or explicit user override documented

### **Implementation Phase Agents**

#### **Implementation Agents** (Sequential Execution)
- **Purpose**: Execute individual chunks using prepared contexts and handoffs
- **Input Sources**:
  - Prepared context from Chunking Analysis Agent
  - Handoff documents from previous implementation agents (dependency chain)
  - Interface contracts requiring satisfaction
- **Output**: Handoff document for dependent chunks with working interfaces
- **Execution Model**: **Sequential only** - one agent at a time to eliminate coordination complexity
- **Success Criteria**: All unit tests passing, interface contracts satisfied, handoff document complete

### **Coordination Model: Sequential Execution**
- **Main Agent Orchestration**: Sequences implementation agents one at a time based on dependency chart
- **No Parallel Coordination**: Eliminates complexity of managing simultaneous agent execution
- **Document-Based Handoffs**: Each agent receives complete context via prepared documents
- **Failure Isolation**: Failed chunks can be restarted independently with same context
- **Stateless Agents**: Each Task invocation is independent, relying only on document-based context

### **Failure Handling Strategy**
- **Planning Phase Failures**: Regenerate analysis with updated specifications
- **Implementation Failures**: Restart individual chunks with same prepared context
- **Integration Failures**: Main agent handles cross-chunk debugging and resolution
- **Catastrophic Failures**: Escalate to user for manual intervention

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

### **Phase 1: Planning & Preparation**

#### **1. Input Validation**
- **Agent**: Input Validation Agent
- **Process**: Validate specification file completeness and clarity
- **Output**: Validation report to main agent
- **Success Gate**: Specification contains all required elements for chunking system
- **Escalation**: If validation fails, return to user for specification enhancement

#### **2. E2E Test Setup**  
- **Agent**: E2E Setup Agent (separate permissions)
- **Process**: Set up and validate E2E tests in main tests folder
- **Output**: Test setup report confirming operational E2E tests
- **Permission Model**: Only agent with E2E test modification rights
- **Success Gate**: All E2E tests executable with clear pass/fail states
- **Protection**: All subsequent agents cannot modify E2E tests

#### **3. Comprehensive Chunking Analysis** (Critical Success Path)
- **Agent**: Chunking Analysis Agent  
- **Process**: Scale validation followed by complete module decomposition and coordination artifact creation
- **Phase A - Scale Validation**:
  - **Chunk Count Estimation**: Analyze module complexity and estimate required chunks
  - **Scale Assessment**: Validate against 4-25 chunk operational limits
  - **User Decision Point**: If outside limits, provide recommendations and require user override
  - **Go/No-Go Gate**: Proceed only if scale is appropriate or user explicitly accepts complexity trade-offs
- **Phase B - Core Analysis** (if scale validation passes):
  - Module boundary identification and chunk size optimization
  - Sequential dependency chain mapping (no parallel complexity)
  - Interface contract definition between all chunks
  - Context preparation for each implementation agent
- **Outputs Created**:
  - `SCALE-VALIDATION.md` - Chunk count estimate, scale appropriateness, and user decision documentation
  - `DEPENDENCY-CHART.md` - Sequential execution order for main agent coordination
  - `COORDINATION-PLAN.md` - Detailed execution sequence, timing estimates, and checkpoints
  - `chunks/chunk-[N]-[name]/CONTEXT.md` - Complete ready-to-use contexts for implementation agents
  - `chunks/chunk-[N]-[name]/CONTRACTS.yaml` - Interface specifications and validation criteria
- **Success Gate**: Scale validation approved, all implementation contexts complete, no additional analysis required during execution

### **Phase 2: Sequential Implementation**

#### **4. Sequential Chunk Implementation**
- **Coordination**: Main agent orchestrates based on dependency chart
- **Execution Model**: **Sequential only** - one implementation agent at a time
- **Per-Chunk Process**:
  1. **Context Loading**: Implementation agent receives prepared context + handoff from dependencies
  2. **Implementation**: Execute chunk implementation using provided specifications
  3. **Testing**: All unit tests must pass before completion
  4. **Contract Validation**: Verify all output contracts are satisfied
  5. **Handoff Generation**: Create handoff document for dependent chunks
- **Input Sources per Agent**:
  - Pre-prepared context from Chunking Analysis Agent
  - Handoff documents from completed dependency chunks
  - Interface contracts requiring satisfaction
- **Output per Agent**: Handoff document with working interfaces and implementation guidance
- **Failure Handling**: Failed chunks restart with same prepared context, no cascade failures

**Implementation Failure Criteria**:
- **Test-passing requirement**: All tests must pass before chunk completion
- **Contract satisfaction**: All output interfaces must work as specified
- **Catastrophic failure exception**: Only exception requires user intervention
- **Isolation principle**: Chunk failures don't affect completed chunks

#### **5. Implementation Coordination Details**
**Main Agent Responsibilities**:
- **Dependency Sequencing**: Execute chunks in dependency order from chart
- **Progress Tracking**: Monitor implementation progress and update coordination state
- **Context Assembly**: Ensure each implementation agent has complete context
- **Integration Validation**: Verify chunk handoffs work correctly
- **Error Recovery**: Handle chunk failures and determine restart procedures

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

## Critical Success Factors

### **1. Chunking Analysis Agent Quality** (Highest Priority)
The entire system success depends on this agent's analysis quality:
- **Context Preparation**: Must create contexts sufficient for implementation without additional analysis
- **Interface Accuracy**: Contract predictions must achieve >90% accuracy (proven standard from experimental results)
- **Dependency Mapping**: Sequential dependency chains must be accurate and complete
- **Scope Definition**: Chunk boundaries must align with natural implementation units

**Mitigation**: Invest heavily in this agent's prompts, validation procedures, and testing with pilot modules.

### **2. Handoff Document Standards** (Make-or-Break Element)
As validated in experimental implementation, handoff quality enables zero-friction implementation:
- **Interface Specifications**: Must include working examples and usage patterns
- **Implementation Context**: Complete integration patterns and error handling approaches
- **Success Criteria**: Clear validation requirements and testing specifications
- **Troubleshooting**: Common issues and resolution approaches

**Reference Standard**: Maintain quality equivalent to `/context/chunking/examples/HANDOFF-2.md` proven patterns.

### **3. Context Size Management**
- **Target**: 3-4K token contexts (validated experimental range)
- **Risk**: Chunking Analysis Agent requiring excessive context for large module analysis
- **Mitigation**: Focus agent on architectural analysis rather than detailed implementation planning

### **4. Sequential Execution Discipline**
- **Dependency Isolation**: Each chunk must complete fully before dependent chunks begin
- **Test Validation**: All unit tests and contract validation must pass before handoff
- **Scope Boundaries**: Implementation agents must stay within defined chunk boundaries
- **Error Isolation**: Failed chunks must not cascade to completed work

### **5. Tool Constraint Alignment**
- **Stateless Agent Design**: Each implementation agent must work independently with document-based context
- **Document-Based Coordination**: All inter-agent communication through file system handoffs
- **Task Tool Usage**: Focused, single-purpose agent invocations with complete context
- **No Runtime Coordination**: All dependency relationships resolved through upfront planning

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