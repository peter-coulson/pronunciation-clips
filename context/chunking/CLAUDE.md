# Agent-Based Chunking System Development

## ⚠️ CRITICAL CONTEXT WARNING ⚠️
**ALWAYS question whether context is absolutely necessary within this file.**
- Keep context as concise as possible
- Avoid verbose explanations or extensive background information
- If you're adding context, ask yourself: "Is this essential for the current development task?"
- **When in doubt, leave it out**

## Current Phase: System Development
We are currently **developing** the agent-based chunking system, not operating it. This involves:
- Building methodology files and agent instruction templates
- Creating communication standards and validation procedures
- Defining workflow patterns and coordination mechanisms

**Note**: The `sessions/` folder is for actual implementation when the system is operationally used within the larger context system. We do not use sessions during development.

## Development Standards
- Always read necessary methodology files before implementing new components
- Follow single responsibility principle for methodology content division
- Adhere to the DRY (Don't Repeat Yourself) principle to minimize redundancy in methodology and implementation
- Maintain a proper configuration file for all constants to ensure easy updates and consistency across the project

## Project Context
@context/chunking/README.md
Only pull when planning which area to implement next: '@context/chunking/PLANNING.md' 

## Implementation Priority Order
1. **Template specification standards** (communication backbone) - Dual template strategy implementation
2. Methodology to prompt translation (agent instructions)
3. Phase B implementation (module decomposition)

## Current Priority: Input Template Design Strategy
Working on dual template approach with Input Validation Agent for translation.

**Temporary Analysis File**: `@context/chunking/input_template_requirements.md`
- Contains comprehensive requirement analysis
- **DO NOT MODIFY** - Used for systematic categorization analysis only
- Will be refined after boundary definition is complete

## Critical Constraints
- Stateless agent design (Task tool limitations)
- Document-based handoffs only
- Sequential execution (no parallel coordination)
- Repository agnostic design