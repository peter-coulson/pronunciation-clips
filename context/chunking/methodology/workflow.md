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
- **Purpose**: Module analysis and coordination artifact creation
- **Outputs**:
  - `SCALE-VALIDATION.md` - Chunk count estimate and appropriateness
  - `DEPENDENCY-CHART.md` - Sequential execution order
  - `COORDINATION-PLAN.md` - Execution sequence and timing
  - `chunks/chunk-[N]-[name]/CONTEXT.md` - Implementation contexts
  - `chunks/chunk-[N]-[name]/CONTRACTS.yaml` - Interface specifications
- **Success Criteria**: Scale validation complete, all contexts ready, no additional analysis required

### **Implementation Phase Agents**

#### **Implementation Agents** (Sequential Execution)
- **Purpose**: Execute individual chunks using prepared contexts
- **Input**: Prepared context + handoff documents + interface contracts
- **Output**: Handoff document for dependent chunks
- **Success Criteria**: Tests pass, contracts satisfied, handoff complete

### **Coordination Model**
- **Sequential only**: One agent at a time, no parallel coordination
- **Document-based handoffs**: Complete context via prepared documents
- **Failure isolation**: Failed chunks restart independently

### **Failure Handling**
- **Planning failures**: Regenerate analysis
- **Implementation failures**: Restart chunk with same context
- **Catastrophic failures**: Escalate to user

## Communication System
**CRITICAL SUCCESS FACTOR**: Handoff document quality is make-or-break for system effectiveness

**Required Handoff Elements**:
- Interface specifications with examples
- Integration patterns and error handling
- Performance requirements and success criteria

**Reference**: `/context/chunking/examples/HANDOFF-2.md` for proven patterns

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

## System Orchestration
- **Main agent coordination**: Runs entire process through claude code
- **Progress tracking**: Continuous context system and CLAUDE.md updates
- **State management**: Maintains coordination state across agent hierarchy

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