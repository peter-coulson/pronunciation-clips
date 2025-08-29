# Knowledge Requirements Generation Methodology

## Process

### Phase 1: Context Validation
**Input**: REQUIREMENTS_LEVEL_INPUT.md  
**Validation**: Verify minimal context section completeness
- Technical Overview: Technologies, architecture, deployment environment
- Integration Landscape: Dependencies, communication patterns  
- Quality Standards: Testing approach, quality tools, documentation

**Failure**: Reject if any section empty, incomplete, or contradictory

### Phase 2: Template Population
**Input**: Validated context  
**Process**: Apply risk-knowledge mapping framework to populate KNOWLEDGE_REQUIREMENTS_TEMPLATE.md  
**Logic**: See @ABSTRACTION_FRAMEWORK.md for Risk-Knowledge Mapping and Context Independence Progression definitions

**Output**: Populated template with specific knowledge requirements for this change