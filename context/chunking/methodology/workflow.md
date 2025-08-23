# Chunking System Workflow

## Input Structure

### Dual Template Strategy
The system uses two template types to optimize input quality:

**User-Facing Template (Simplified)**:
- Domain expert friendly format
- Focuses on business requirements and implementation decisions
- Excludes overwhelming system coordination details
- Optimized for completion rates and cognitive load

**System Template (Complete)**:
- Contains comprehensive requirement analysis
- Ensures agents make zero implementation assumptions
- Generated through translation from user input
- Combined with auto-populated repository context

### Input Sources
The complete system input comes from:
1. **User Template**: Simplified specification completed by domain expert
2. **Repository Context**: Auto-populated project guidelines and standards
3. **System Translation**: Input Validation Agent transforms user template to complete specification

This dual approach maximizes input quality while ensuring agents have complete context with minimal decision-making requirements.

## Failure Handling & Recovery (to be defined later)

**Initial Approach**: Start with minimal failure handling that can be implemented and improved as the MVP is used in production

## Workflow Steps

### **Phase 1: Planning & Preparation**

#### **1. Input Validation & Translation**
- **Agent**: Input Validation Agent
- **Input**: User-facing template (simplified)
- **Process**: 
  1. Validate user specification completeness
  2. Translate to complete system template
  3. Integrate with auto-populated repository context
  4. Identify and flag any remaining gaps
- **Output**: Complete system template with validation report
- **Success Gate**: System template complete with all critical requirements specified

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