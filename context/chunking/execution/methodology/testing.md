# Execution Phase Testing Strategy

## Contract Fulfillment Testing
- **Contract Fulfillment**: Chunk contracts are only fulfilled when all unit tests, integration tests, and chunk-level E2E tests pass for the chunk
- **Final Validation**: All tests including module-level E2E tests must pass at the end before completion (main agent validates and corrects)

## Two-Level E2E Testing During Execution
- **Module-Level E2E Tests**: Test the complete feature end-to-end (created by E2E Setup Agent at start)
- **Chunk-Level E2E Tests**: Test individual chunks in isolation but end-to-end within their scope (specified in chunk contracts)
- **Purpose**: Module-level ensures integration, chunk-level ensures component correctness

## E2E Test Immutability
- **Immutability Principle**: Once E2E tests are created by E2E Setup Agent, they cannot be modified by any implementation agent
- **Implementation Timing**: E2E tests created before any chunk implementation begins