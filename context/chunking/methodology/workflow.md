# Chunking System Workflow

## Input Structure
The input to this system will come from a combination of:
- Repository main context for generic project wide guidelines
- A highly detailed file containing all the necessary specifications for the chunking system to implement the changes

This should allow for very little decisions made by the chunking system as they should be predefined in this file or in the repository context.

## System Foundation
The foundation of the system is its test driven framework. This starts with the main predefined E2E testing scenarios in the input file. These E2E tests will be solely for the entire implementation and not at the chunk level.

## Scale Requirements
**Target**: 15-20 chunks (medium to medium/large modules)
**Justification**: Coordination overhead exceeds implementation time without automation at this scale

## Architecture Constraints
- **Task Tool**: Stateless agent invocation via documents
- **Sequential Execution**: No parallel coordination complexity
- **Document-Based Handoffs**: File system communication only

### **Chunk Scale Limits**
- **Minimum**: 4 chunks (below this, use single-session implementation)
- **Maximum**: 25 chunks (above this, consider module decomposition)
- **Optimal**: 8-20 chunks for most modules

**Validation Required**: Chunking Analysis Agent must validate chunk count against limits before proceeding

## Agent Specialization

### **Planning Phase Agents**
The system employs specialized agents for upfront analysis and preparation:

#### **Input Validation Agent**
- **Purpose**: Validates specification completeness
- **Output**: Validation report identifying gaps

#### **E2E Setup Agent**  
- **Purpose**: Sets up E2E tests (only agent with E2E modification rights)
- **Output**: Operational E2E test confirmation

#### **Chunking Analysis Agent** (Critical Success Path)
- **Purpose**: Complete module decomposition and coordination artifact creation

**Phase A - Scale Validation**:
- **Chunk Count Estimation**: Analyze module complexity to estimate required chunks (4-25 range)
- **Scale Assessment**: Validate appropriateness for chunking vs single-session implementation
- **User Decision Point**: Require explicit approval if outside optimal limits

**Phase B - Chunk Definition** (to be defined later):
- **Interface Contracts**: Specify exact input/output relationships between chunks
- **Dependency Mapping**: Create sequential execution order with no parallel coordination complexity

**Phase C - Context Preparation**:
- **Implementation Contexts**: 3-4K token focused contexts for each chunk (sufficient for implementation without additional analysis)
- **Integration Guidance**: How each chunk integrates with existing codebase patterns
- **Contract Specifications**: Detailed interface requirements with examples and validation criteria

**Critical Outputs**:
- `SCALE-VALIDATION.md` - Chunk count estimate, appropriateness assessment, user decision documentation
- `DEPENDENCY-CHART.md` - Sequential execution order for main agent coordination
- `COORDINATION-PLAN.md` - Detailed execution sequence, timing estimates, checkpoints
- `chunks/chunk-[N]-[name]/CONTEXT.md` - Complete implementation contexts (no additional analysis required)
- `chunks/chunk-[N]-[name]/CONTRACTS.yaml` - Interface specifications and validation criteria

**Success Criteria**: Scale validation approved, all chunk boundaries clearly defined with working interfaces, implementation contexts complete and sufficient

### **Implementation Phase Agents**

#### **Implementation Agents** (Sequential Execution)
- **Purpose**: Execute individual chunks using prepared contexts
- **Input**: Prepared context + handoff documents + interface contracts
- **Output**: Handoff document for dependent chunks
- **Success Criteria**: Tests pass, contracts satisfied, handoff complete


## Testing Strategy

### **E2E Test Rules**
- **Input Specification**: E2E tests must be specified in the main input file
- **Immutability Principle**: Once E2E tests are created by E2E Setup Agent, they cannot be modified by any subsequent agent
- **Implementation Timing**: E2E tests created before any chunk implementation begins

### **Unit and Integration Test Requirements**
- **Contract Fulfillment**: Chunk contracts are only fulfilled when all unit tests, integration tests, and potentially E2E tests pass for the chunk
- **Test Specification Location**: Must still decide exactly where in the system all of these tests are specified
- **Final Validation**: All tests including E2E tests must pass at the end before completion (main agent validates and corrects)

### **To Be Specified**
- How and where the unit, intergration, and E2E testing requirements for each chunk contracts are to be specified. 
- E2E testing requirements within chunks are seperate from the full module E2E tests at the start. These are E2E tests within a module. (This may not prove necessary in the final evaluation).

## Templates & Communication Standards

### **Template Structure & Validation**
**CRITICAL SUCCESS FACTOR**: Template quality is the communication backbone - handoff document quality is make-or-break for system effectiveness

**Template Types**:
- **Input Specification Template**: Standardized format for user requirements input
- **Handoff Document Template**: Critical communication between dependent chunks
- **Context Package Template**: Standardized 3-4K token contexts for implementation agents
- **Summary Report Template**: Session completion and results documentation

### **Handoff Document Standards** (to be defined)
Based on validated patterns from `/context/chunking/examples/HANDOFF-2.md` and `/context/chunking/examples/DIARIZATION_CHUNK2_CONTEXT.md`

**Template Validation Required**: Template validation must occur at every stage (specific protocols to be defined)

## Failure Handling & Recovery (to be defined later)

**Initial Approach**: Start with minimal failure handling that can be implemented and improved as the MVP is used in production

## Workflow Steps

### **Phase 1: Planning & Preparation**

#### **1. Input Validation**
- **Agent**: Input Validation Agent
- **Output**: Validation report
- **Success Gate**: Specification complete

#### **2. E2E Test Setup**  
- **Agent**: E2E Setup Agent (only agent with E2E modification rights)
- **Output**: Operational E2E tests
- **Success Gate**: All tests executable

#### **3. Chunking Analysis** (Critical Success Path)
- **Agent**: Chunking Analysis Agent  
- **Phase A**: Scale validation (4-25 chunk limits)
- **Phase B**: Module decomposition and context preparation
- **Outputs**: SCALE-VALIDATION.md, DEPENDENCY-CHART.md, COORDINATION-PLAN.md, chunk contexts and contracts
- **Success Gate**: Scale validated, all contexts complete

### **Phase 2: Sequential Implementation**

#### **4. Sequential Chunk Implementation**
- **Coordination**: Main agent orchestrates based on dependency chart
- **Per-Chunk Process**: Context loading → Implementation → Testing → Contract validation → Handoff generation
- **Failure Handling**: Failed chunks restart with same context, no cascade failures

#### **5. Final Validation**
Main agent runs all tests, implements fixes until working, generates final report

#### **6. Context System Update**
Update main context system with results, track system success metrics

## Main Agent Coordination Architecture

### **Document-Based Coordination Model**
The system uses document-based coordination instead of programmatic dependency management:
- **Stateless Agent Design**: Each agent receives complete context via documents, no runtime state sharing
- **File System Handoffs**: All inter-agent communication through prepared documents and handoff files
- **No Runtime Coordination**: All dependency relationships resolved through upfront planning by Analysis Agent
- **Context Window Boundaries**: Child agents operate within 3-4K token contexts from prepared documents

**Why Document Coordination**: Aligns with Claude Code's Task tool constraints while ensuring reproducible, debuggable agent interactions

### **Main Agent Responsibilities** (to be fleshed out)
- **Process Orchestration**: Sequences all specialized agents based on dependency chart
- **Report Interpretation**: Analyzes sub-agent outputs for success/failure states and next actions
- **Final Validation**: Ensures all tests pass before completion, implements corrections as needed
- **Error Recovery**: Determines restart vs escalation procedures (protocols to be defined)

### **Progress Tracking Protocols**
- **Main Progress**: Chunking progress captured in CLAUDE.md
- **Minor Progress Tracking**: Still needs to be defined
- **State Management**: Tracks completion status of each agent across all phases

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

## Proven Patterns (Experimental Results)
- **Context Size**: 3-4K tokens effective (4.8/5 rating)
- **Contract Accuracy**: 95% interface prediction accuracy
- **Development Velocity**: 120% of expected timeline
- **Integration Failures**: Zero when contracts accurate
- **E2E Test Immutability**: Tests unchanged throughout implementation