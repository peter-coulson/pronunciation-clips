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
**Process**: Apply risk-knowledge mapping to populate KNOWLEDGE_REQUIREMENTS_TEMPLATE.md  
**Logic**: For each level transition, map universal risk types to knowledge categories:
- System-Breaking → Constraint Knowledge
- Integration-Breaking → Integration Knowledge  
- Maintenance-Breaking → Pattern Knowledge
- Quality-Breaking → Convention Knowledge

**Context Independence Rules**:
- Infrastructure Knowledge: Not required after Architecture Level (2)
- Domain Knowledge: Not required after Behavior Level (4)
- Technology/Quality/Codebase Knowledge: Required through Implementation Level (7)

**Output**: Populated template with specific knowledge requirements for this change