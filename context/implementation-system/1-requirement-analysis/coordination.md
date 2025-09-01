# Stage 1: Requirements Coordination

## Execution Flow

## Sequential Phase Execution

**Main Stage**: Handles input validation and coordination
**Process Isolation**: Use Task tool to spawn separate sub-processes for knowledge generation and knowledge extraction phases.

### Main Stage: Input Validation
**Input**: Original template
**Process**: Template-agnostic validation of minimal system information sections
**Output**: Validated input or rejection with specific gaps

**Validation Logic:**
- **Required Sections**: Technical Overview, Integration Landscape, Quality Standards
- **Pass**: All sections complete, coherent, non-contradictory
- **Fail**: Any section empty, incomplete, or contradictory - reject with detailed explanation of why each insufficient section fails validation requirements

### Phase 1: Knowledge Requirements Generation
**Process**: Apply risk-knowledge mapping framework to determine knowledge requirements
**Output**: Completed REQUIREMENTS_INPUT_TEMPLATE.md

### Phase 2: Knowledge Extraction
**Process**: Research and extract available information from knowledge repository
**Output**: Completed KNOWLEDGE_PACKAGE_TEMPLATE.md with gaps identified

## Handoff Requirements

**Main Stage → Phase 1**: Validated template or rejection with specific gaps
**Phase 1 → Phase 2**: Fully populated knowledge requirements template
**Phase 2 → Output**: Complete knowledge extraction with missing items documented

