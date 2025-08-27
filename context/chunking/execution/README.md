# Execution Agent

## Purpose
Transforms Level 4 behavioral specifications into working code (Level 7 implementation) while ensuring all contracts are fulfilled through mandatory test validation.

## Input Files

### CONTEXT.md (Required)
- **Level 4 behavioral specifications**: Test requirements, performance criteria, quality validation gates
- **Interface contracts**: Stable interfaces from previous chunks that this chunk can rely on
- **Implementation requirements**: Core responsibilities, focus areas, integration patterns
- **Required test gates**: Integration and E2E tests that must pass before completion

### HANDOFF.md (Optional - for dependent chunks)
- **Implementation summary**: Core components and public API interfaces from completed chunks
- **Integration contracts**: Stable data models and error handling patterns
- **Integration requirements**: Specific patterns and code templates for connecting with existing functionality

## Output Files

### HANDOFF.md
- **Level 5-6 specifications**: Algorithm specifications, exact method contracts, integration patterns
- **Implementation summary**: Completed components with stable interfaces
- **Integration requirements**: Detailed patterns for dependent chunks to follow

## Success Criteria
- All unit tests, integration tests, and chunk-level E2E tests pass
- Contract fulfillment achieved through test validation
- Handoff document provides complete integration specifications for dependent chunks

## Methodology Files
- `templates/HANDOFF_TEMPLATE.md` - Template for output handoff specifications

## Testing Strategy

### Contract Fulfillment
Chunk contracts are only fulfilled when all unit tests, integration tests, and chunk-level E2E tests pass for the chunk.

### E2E Test Immutability
- E2E tests are created before chunk implementation begins and cannot be modified by implementation agents
- Tests serve as immutable behavioral contracts that implementation must satisfy