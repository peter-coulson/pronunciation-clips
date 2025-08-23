# Agent-Based Chunking System Development

## Development Standards
- Always read necessary methodology files before implementing new components
- Follow single responsibility principle for methodology content division
- Adhere to the DRY (Don't Repeat Yourself) principle to minimize redundancy in methodology and implementation
- Maintain a proper configuration file for all constants to ensure easy updates and consistency across the project

## Project Context
@context/chunking/README.md
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