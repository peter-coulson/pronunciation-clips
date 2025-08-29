# [CHUNK NAME] CONTEXT - [Brief Description]

## Chunk Scope: [Clear Scope Statement]
**Files**: [Specific files to be modified/created with size estimates]
**Token Budget**: [Estimated context size, aim for <3K]
**Dependencies**: [List of previous chunks this depends on]

## Required Interfaces (from Previous Chunks)
```[language]
# Stable interfaces from previous chunks - IMPLEMENTED AND TESTED
[Code showing interfaces this chunk can rely on]
```

## Output Contracts (for Future Chunks)
```[language]
# Interfaces this chunk will provide - CONTRACT
[Code showing what this chunk will deliver to future chunks]
```

## System Integration Context
**Architecture Placement**: [Where this component fits in system architecture]
**Integration Patterns**: [Existing system patterns this chunk must follow]
**Existing Components**: [Key components this chunk interacts with]

## Implementation Requirements

### Core [Component] Responsibilities
- [Primary responsibility 1]: [Behavioral expectation]
- [Primary responsibility 2]: [Behavioral expectation]  
- [Key abstraction]: [What this component should encapsulate]

### [Key Requirement Category 1]
- [Specific requirement 1]
- [Specific requirement 2]
- [Specific requirement 3]

### [Key Requirement Category 2]
- [Specific requirement 1]
- [Specific requirement 2]
- [Specific requirement 3]

### Performance Considerations
- [Performance requirement 1]
- [Performance requirement 2]
- [Performance requirement 3]

## Quality Validation Requirements
- [Behavioral validation 1]: [Expected behavior to verify]
- [Behavioral validation 2]: [Expected behavior to verify]
- [Performance criteria]: [Measurable quality thresholds]

## Required Test Gates
### Integration Tests (Must Pass Before Proceeding)
- **[Integration Test Name]**: [Specific pre-defined test from coordination plan]
  - **Purpose**: [What interface/contract this validates]
  - **Command**: [How to execute this test]

### E2E Tests (Must Pass Before Proceeding)  
- **[E2E Test Name]**: [Specific pre-defined test from coordination plan]
  - **Purpose**: [What user workflow this validates]
  - **Command**: [How to execute this test]

## Focus Areas
- **[Priority 1]**: [Brief description of key focus area]
- **[Priority 2]**: [Brief description of key focus area]
- **[Priority 3]**: [Brief description of key focus area]

## Applied Context Knowledge

### Constraint Knowledge Applied
**Implementation Constraints**: [CONSTRAINT_LIST]

### Integration Knowledge Applied  
**Integration Points**: [INTEGRATION_REQUIREMENTS]

### Pattern Knowledge Applied
**Implementation Patterns**: [PATTERN_LIST]

### Convention Knowledge Applied
**Implementation Conventions**: [CONVENTION_LIST]