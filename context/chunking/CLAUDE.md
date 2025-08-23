# Agent-Based Chunking System Development

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
Only pull when planning which area to implement next:
@context/chunking/PLANNING.md 

## Implementation Priority Order
1. Template specification standards (communication backbone)
2. Methodology to prompt translation (agent instructions)
3. Phase B implementation (module decomposition)

## Critical Constraints
- Stateless agent design (Task tool limitations)
- Document-based handoffs only
- Sequential execution (no parallel coordination)
- Repository agnostic design