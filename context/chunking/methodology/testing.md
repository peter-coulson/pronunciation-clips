# Testing Strategy

## System Foundation
The foundation of the system is its test driven framework. This starts with the main predefined E2E testing scenarios in the input file. These E2E tests will be solely for the entire implementation and not at the chunk level.

## Testing Strategy

### **E2E Test Rules**
- **Input Specification**: E2E tests must be specified in the main input file
- **Immutability Principle**: Once E2E tests are created by E2E Setup Agent, they cannot be modified by any subsequent agent
- **Implementation Timing**: E2E tests created before any chunk implementation begins

### **Unit and Integration Test Requirements**
- **Contract Fulfillment**: Chunk contracts are only fulfilled when all unit tests, integration tests, and potentially E2E tests pass for the chunk
- **Test Specification Location**: Must still decide exactly where in the system all of these tests are specified
- **Final Validation**: All tests including E2E tests must pass at the end before completion (main agent validates and corrects)

### **To Be Specified**
- How and where the unit, intergration, and E2E testing requirements for each chunk contracts are to be specified. 
- E2E testing requirements within chunks are seperate from the full module E2E tests at the start. These are E2E tests within a module. (This may not prove necessary in the final evaluation).