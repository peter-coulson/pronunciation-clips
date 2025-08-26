# Template-to-Requirements Agent Coordination

## Agent Boundaries

**Scope**: Transform any input template to knowledge requirements and context extraction
**Template Agnostic**: Works with any new template structure without modification
**Stateless Operation**: Single session with document-based handoffs between phases

## Core Responsibilities

1. **Input Template Validation** - Verify template completeness and structure
2. **Knowledge Requirements Generation** - Apply risk-knowledge mapping framework  
3. **Context Research** - Extract available information from context system

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
- **Fail**: Any section empty, incomplete, or contradictory - reject with specific gaps identified

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

## Template Agnostic Principles

- Validation logic focuses on minimal context completeness, not specific template structure
- Knowledge mapping applies universal risk-knowledge framework regardless of input format
- Context extraction methodology remains constant across all template types
- New templates require no changes to core coordination or methodology files