# Coordination Plan Template

**Feature Name**: [FROM CONTEXT EXTRACTION]
**Target Specification Level**: Coordination (Implementation Management)

---

## Implementation Overview

### [UNIT_NAME_1]
**Implementation Focus**: [Brief description of what this unit accomplishes]

### [UNIT_NAME_2] 
**Implementation Focus**: [Brief description of what this unit accomplishes]

### [UNIT_NAME_3]
**Implementation Focus**: [Brief description of what this unit accomplishes]

---

## Execution Sequence

### Dependency Chain
**Sequential Dependencies**:
- [UNIT_A] → [UNIT_B] → [UNIT_C]

### Parallel Execution Sets
**Concurrent Groups**:
- Group 1: {[UNIT_D], [UNIT_E]}
- Group 2: {[UNIT_F], [UNIT_G]}

### Critical Path
**Longest Chain**: [UNIT_SEQUENCE]
**Estimated Duration**: [TIMEFRAME]

---

## Handoff Specifications

### [HANDOFF_1]
**Source**: [UNIT_A]
**Target**: [UNIT_B] 
**Interface**: [FILE_FORMAT/DATA_TYPE]
**Validation**: [COMPLETION_CRITERIA]

### [HANDOFF_2]
**Source**: [UNIT_B]
**Target**: [UNIT_C]
**Interface**: [FILE_FORMAT/DATA_TYPE] 
**Validation**: [COMPLETION_CRITERIA]

---

## Context Management

### Context Distribution
**[UNIT_NAME_1]**:
- Context Source: [EXTRACTION_SECTIONS]
- Estimated Size: [TOKEN_COUNT/LINES]

**[UNIT_NAME_2]**:
- Context Source: [EXTRACTION_SECTIONS] 
- Estimated Size: [TOKEN_COUNT/LINES]

### Agent Requirements
**[UNIT_NAME_1]**: [AGENT_TYPE] - [SPECIALIZATION_REASON]
**[UNIT_NAME_2]**: [AGENT_TYPE] - [SPECIALIZATION_REASON]

---

## Completion Criteria

### Individual Unit Success
**[UNIT_NAME_1]**: [COMPLETION_INDICATORS]
**[UNIT_NAME_2]**: [COMPLETION_INDICATORS]

### Integration Validation
**Cross-Unit Tests**: [VALIDATION_REQUIREMENTS]
**System Integration**: [INTEGRATION_TESTS]

### Overall Completion
**Feature Complete**: [FINAL_SUCCESS_CRITERIA]
**Quality Gates**: [QUALITY_VALIDATION]

---

## Error Handling Strategy

### Failure Isolation
**Independent Failures**: [UNITS_THAT_CAN_FAIL_ALONE]
**Cascading Failures**: [FAILURE_PROPAGATION_CHAINS]

### Recovery Procedures
**[ERROR_SCENARIO_1]**: [RECOVERY_APPROACH]
**[ERROR_SCENARIO_2]**: [RECOVERY_APPROACH]

### Rollback Requirements
**[UNIT_NAME]** failure: [ROLLBACK_SCOPE]
**Integration** failure: [INTEGRATION_ROLLBACK]

---

## Resource Requirements

### Context Limits
**High Context Units**: [UNIT_NAMES]
**Standard Context Units**: [UNIT_NAMES]

### Specialized Capabilities  
**[CAPABILITY_TYPE]**: [REQUIRED_FOR_UNITS]
**[CAPABILITY_TYPE]**: [REQUIRED_FOR_UNITS]

---

## Coordination Notes

### Execution Considerations
**[CONSIDERATION_1]**: [IMPACT_AND_MITIGATION]
**[CONSIDERATION_2]**: [IMPACT_AND_MITIGATION]

### Integration Risks
**[RISK_CATEGORY]**: [MITIGATION_STRATEGY]
**[RISK_CATEGORY]**: [MITIGATION_STRATEGY]