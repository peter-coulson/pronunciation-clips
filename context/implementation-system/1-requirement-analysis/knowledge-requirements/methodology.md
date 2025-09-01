# Knowledge Requirements Generation Methodology

## Process

### Phase 1: System Information Validation
**Input**: sessions/[session-name]/input/user-requirements.md  
**Validation**: Verify minimal system information section completeness
- Technical Overview: Technologies, architecture, deployment environment
- Integration Landscape: Dependencies, communication patterns  
- Quality Standards: Testing approach, quality tools, documentation

**Failure**: Reject if any section empty, incomplete, or contradictory

### Phase 2: Template Population
**Input**: Validated system information  
**Process**: Apply risk-knowledge mapping framework to populate REQUIREMENTS_INPUT_TEMPLATE.md  
**Logic**: See @ABSTRACTION_FRAMEWORK.md for Risk-Knowledge Mapping and Knowledge Independence Progression definitions

**Output**: Populated template with specific knowledge requirements for this change