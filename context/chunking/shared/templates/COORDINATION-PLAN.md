# COORDINATION-PLAN: [Project Name]

## Overview
**Implementation Objective**: [Brief description of what will be built]
**Total Estimated Duration**: [X] hours across [N] chunks
**Target Architecture**: [High-level approach - e.g., ML integration, API system, data pipeline]

## Execution Sequence

### Chunk Dependencies
```mermaid
graph TD
    A[Chunk 1: [Name]] --> B[Chunk 2: [Name]]
    B --> C[Chunk 3: [Name]]
    C --> D[Chunk 4: [Name]]
```

### Sequential Implementation Order
1. **[Chunk 1 Name]** → **[Chunk 2 Name]** → **[Chunk 3 Name]** → **[Chunk N Name]**
2. **Critical Path**: [Chunks that cannot be parallelized] 
3. **Dependency Rationale**: [Why this order is required]

## Chunk Specifications

### Chunk 1: [Name]
- **Purpose**: [What this chunk achieves]
- **Duration Estimate**: [X] minutes
- **Dependencies**: [None | Previous chunks]
- **Key Deliverables**: 
  - [Specific interface/component 1]
  - [Specific interface/component 2]
- **Context Package Requirements** (~[X]K tokens):
  - **Specification Context**: [Handoff docs, requirements]
  - **Repository Context**: [Specific files to read - src/path/file.py, config files]
  - **Integration Patterns**: [Similar implementations for reference]
  - **Test Context**: [Existing test structures to follow]

### Chunk 2: [Name]
- **Purpose**: [What this chunk achieves]
- **Duration Estimate**: [X] minutes  
- **Dependencies**: Chunk 1 ([specific deliverables needed])
- **Key Deliverables**:
  - [Specific interface/component 1]
  - [Specific interface/component 2]
- **Context Package Requirements** (~[X]K tokens):
  - **Specification Context**: [Handoff from Chunk 1]
  - **Repository Context**: [Files to modify, integration points]
  - **Integration Patterns**: [Existing implementations to follow]
  - **Test Context**: [Test files and patterns]

[Repeat for each chunk...]

## Repository Context Strategy

### Phase 1: Foundation Context
**Target Files for Modification**:
- `[path/to/models]` - [Purpose - data structures, business logic, etc.]
- `[path/to/controllers]` - [Purpose - request handling, coordination]

**Integration Dependencies**:
- `[path/to/integration_layer]` - [What interfaces to use]
- `[path/to/configuration]` - [Configuration patterns to follow]

**Pattern References**:
- `[path/to/similar_implementation]` - [What patterns to follow]

### Phase 2: Implementation Context  
**Target Files for Enhancement**:
- `[path/to/main_system]` - [What functionality to add]
- `[path/to/data_pipeline]` - [Integration points]

**Quality References**:
- `[path/to/test_patterns]` - [Test structures to replicate]
- `[path/to/config_examples]` - [Configuration validation patterns]

[Continue for each major phase...]

## Integration & E2E Test Specifications

### System-Wide E2E Test Requirements
**Complete User Workflows**:
1. **[Primary User Journey]**: [Step-by-step scenario]
   - **Input**: [Initial conditions and user input]
   - **Expected**: [End-to-end behavior and outcomes]
   - **Validation**: [Success criteria and data verification]

2. **[Secondary User Journey]**: [Step-by-step scenario]
   - **Input**: [Initial conditions and user input]  
   - **Expected**: [End-to-end behavior and outcomes]
   - **Validation**: [Success criteria and data verification]

### Cross-Chunk Integration Tests
**[Chunk A] → [Chunk B] Interface**:
- **Contract**: [Specific interface being tested]
- **Test Data**: [Input data format and examples]
- **Expected Output**: [Exact data structure and behavior]
- **Error Scenarios**: [Failure modes to validate]

**[Chunk B] → [Chunk C] Interface**:  
- **Contract**: [Specific interface being tested]
- **Test Data**: [Input data format and examples]
- **Expected Output**: [Exact data structure and behavior]
- **Error Scenarios**: [Failure modes to validate]

### Test Execution Strategy
**Integration Test Order**: [Sequence for running cross-chunk tests]
**E2E Test Dependencies**: [Which components must be ready]
**Test Data Management**: [How test data is created/cleaned up]

## Critical Checkpoints

### Checkpoint 1: Foundation Validation (After Chunk [N])
**Validation Criteria**:
- [ ] [Core data models implemented and tested]
- [ ] [Configuration integration working]  
- [ ] [Basic interfaces defined]

**Exit Criteria**: [Specific tests passing, interface contracts verified]

### Checkpoint 2: Integration Validation (After Chunk [N])
**Validation Criteria**:
- [ ] [Key integrations working]
- [ ] [Error handling implemented]
- [ ] [Performance targets met]

**Exit Criteria**: [Integration tests passing, no regression]

[Continue for each major milestone...]

## Error Handling Strategy

### Chunk-Level Error Isolation
- **Pattern**: [How errors stay contained within chunk boundaries]
- **Fallback Strategy**: [What happens when chunk fails]
- **Recovery Process**: [How to resume after chunk failure]

### Integration Error Prevention
- **Interface Validation**: [How to verify contracts before handoff]
- **Context Validation**: [How to ensure context sufficiency]
- **Dependency Checking**: [How to verify prerequisites are met]

## Quality Gates

### Code Quality Standards
- **Test Coverage**: [Required coverage threshold per chunk]
- **Performance Targets**: [Specific performance requirements]
- **Integration Standards**: [How to verify clean integration]

### Documentation Requirements
- **Handoff Quality**: [Standards for inter-chunk handoffs]
- **Interface Documentation**: [Contract specification requirements]
- **Configuration Documentation**: [Setup and deployment requirements]

## Context Management Protocol

### Context Package Assembly
**Per Chunk Context Structure**:
1. **Handoff Document** (500-1K tokens): Previous chunk outputs and interfaces
2. **Specification Document** (500-1K tokens): Current chunk requirements  
3. **Repository Files** (1.5-2K tokens): Target files, integration points, patterns
4. **Test References** (500-1K tokens): Test structures and quality standards

### Context Quality Validation
- **Sufficiency Check**: [How to verify context completeness]
- **Relevance Filter**: [What context to exclude to avoid overload]
- **Integration Validation**: [How to ensure repository context accuracy]

## Success Metrics

### Technical Targets
- **Functionality**: [All required features implemented and tested]
- **Performance**: [Specific performance benchmarks met]
- **Quality**: [Test coverage and integration success rates]
- **Reliability**: [Error handling and fallback effectiveness]

### Process Targets  
- **Timeline**: [Implementation completed within estimated duration]
- **Context Efficiency**: [Context sufficiency rating >4/5 per chunk]
- **Integration Success**: [Zero interface rework between chunks]
- **Error Isolation**: [Chunk failures don't cascade to other chunks]

---

## Implementation Notes

### Repository Integration Points
**Critical Files**: [List of files that multiple chunks will interact with]
**Shared Interfaces**: [Common interfaces used across chunks]
**Configuration Touch Points**: [Config files that need updates]

### Coordination Handoff Requirements
**Between Chunks**: [What information must be passed between sequential chunks]
**Quality Validation**: [How to verify chunk outputs before proceeding]
**Error Recovery**: [Process for handling and recovering from chunk failures]

*This coordination plan provides the execution phase with complete dependency management, context specifications, and quality gates needed for successful chunked implementation.*