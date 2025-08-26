# Planning Module

## Overview
Stateless agent system for transforming requirements into executable specifications through systematic knowledge integration and context extraction.

## Core Framework
- **ABSTRACTION_FRAMEWORK.md** - Foundation specification levels, knowledge categories, and risk-knowledge mapping

## Context-and-Requirements Agent
Primary agent for preparing planning inputs through validation, knowledge generation, and context research.

### Entry Points by Role
- **Operators**: Start with `templates/REQUIREMENTS_LEVEL_INPUT.md` 
- **Developers**: Review `methodology/context-and-requirements/coordination.md`
- **Maintainers**: Begin with `ABSTRACTION_FRAMEWORK.md`

### Agent Files
**Methodology**: `/methodology/context-and-requirements/`
- `coordination.md` - Agent phases and handoffs
- `knowledge-mapping.md` - Risk-knowledge mapping process  
- `context-extraction.md` - Information research methodology

**Templates**: `/templates/`
- `REQUIREMENTS_LEVEL_INPUT.md` - Input specification format
- `KNOWLEDGE_REQUIREMENTS_TEMPLATE.md` - Generated knowledge needs
- `CONTEXT_EXTRACTION_OUTPUT.md` - Researched context output

## Agent Flow
Input Template → Validation → Knowledge Requirements → Context Extraction → Planning Ready

## Usage
All agents operate statelessly with document-based handoffs. No sessions folder usage during development.