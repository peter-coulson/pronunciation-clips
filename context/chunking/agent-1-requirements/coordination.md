# Agent 1: Requirements Coordination

## Execution Flow

## Sequential Phase Execution

**Main Agent**: Handles input validation and coordination
**Context Isolation**: Use Task tool to spawn separate subagents for knowledge generation and context extraction phases.

### Main Agent: Input Validation
**Input**: Original template
**Process**: Template-agnostic validation of minimal context sections
**Output**: Validated input or rejection with specific gaps

**Validation Logic:**
- **Required Sections**: Technical Overview, Integration Landscape, Quality Standards
- **Pass**: All sections complete, coherent, non-contradictory
- **Fail**: Any section empty, incomplete, or contradictory - reject with detailed explanation of why each insufficient section fails validation requirements

### Phase 1: Knowledge Requirements Generation Subagent
**Input**: Validated template + `knowledge-mapping.md` methodology + ABSTRACTION_FRAMEWORK.md
**Process**: Apply risk-knowledge mapping to populate template
**Output**: Completed KNOWLEDGE_REQUIREMENTS_TEMPLATE.md
**Subagent Task**: "Generate knowledge requirements from validated template using knowledge-mapping.md methodology"

### Phase 2: Context Extraction Subagent
**Input**: Knowledge requirements + `context-extraction.md` methodology + Context system access
**Process**: Research and extract available information
**Output**: Completed CONTEXT_EXTRACTION_OUTPUT.md with gaps identified
**Subagent Task**: "Extract context information using context-extraction.md methodology to populate template"

## Handoff Requirements

**Main Agent → Phase 1**: Validated template or rejection with specific gaps
**Phase 1 → Phase 2**: Fully populated knowledge requirements template
**Phase 2 → Output**: Complete context extraction with missing items documented

