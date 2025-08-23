# Agent Architecture

## Scale Requirements
**Target**: 5-20 chunks (small to medium-large modules)
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
- **Purpose**: Template translation and validation
- **Input**: User-facing template (simplified)
- **Process**: Validate completeness, translate to system template, integrate repository context
- **Output**: Complete system template with validation report

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
- **Interface Specifications**: Specify exact input/output relationships between chunks
- **Dependency Mapping**: Create sequential execution order with no parallel coordination complexity

**Phase C - Context Preparation**:
- **Implementation Contexts**: 3-4K token focused contexts for each chunk (sufficient for implementation without additional analysis)
- **Integration Guidance**: How each chunk integrates with existing codebase patterns
- **Interface Specifications**: Detailed interface requirements with examples and validation criteria

**Critical Outputs**:
- `SCALE-VALIDATION.md` - Chunk count estimate, appropriateness assessment, user decision documentation
- `DEPENDENCY-CHART.md` - Sequential execution order for main agent coordination
- `COORDINATION-PLAN.md` - Detailed execution sequence, timing estimates, checkpoints
- `chunks/chunk-[N]-[name]/CONTEXT.md` - Complete implementation contexts (no additional analysis required)

**Success Criteria**: Scale validation approved, all chunk boundaries clearly defined with working interfaces, implementation contexts complete and sufficient

### **Implementation Phase Agents**

#### **Implementation Agents** (Sequential Execution)
- **Purpose**: Execute individual chunks using prepared contexts
- **Input**: Prepared context + handoff documents + interface specifications
- **Output**: Handoff document for dependent chunks
- **Success Criteria**: Tests pass, interface specifications satisfied, handoff complete

## Target Scope
The target change size of this system is at minimum a large single file implementation and at maximum a medium to medium/large sized module.