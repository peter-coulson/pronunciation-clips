# Implementation Segmentation Methodology

## Sub-Process Purpose
Executes test-driven implementation using generated tests as immutable behavioral contracts, transforming Level 4 behavioral specifications (see @ABSTRACTION_FRAMEWORK.md) into working code while ensuring contract fulfillment.

## Input Requirements

### Behavioral Specifications
- **CONTEXT.md** (Required): Level 4 behavioral specifications, interface contracts, implementation requirements, required test gates
- **HANDOFF.md** (Optional): Implementation summaries and integration contracts from dependent segments

### Generated Test Infrastructure
- **Executable E2E Test Files**: Immutable end-to-end validation contracts
- **Executable Integration Test Files**: Component boundary validation tests
- **Test Support Files**: Required fixtures, mocks, and utilities

## Test-Driven Implementation Process

### Phase 1: Input Analysis
- Parse CONTEXT.md for behavioral requirements and test gates
- Extract interface contracts from HANDOFF.md (if present)
- Identify implementation scope and dependencies

### Phase 2: Unit Test Creation
- Extract specific testing requirements from CONTEXT.md Quality Validation Requirements
- Apply testing patterns and conventions from Applied Context Knowledge sections
- Write unit tests covering all behavioral validations and performance criteria
- Create tests for all output contracts this segment must provide
- Verify tests fail initially (red phase)
- Confirm integration/E2E test infrastructure is functional

### Phase 3: Contract Implementation
- Implement public interfaces specified in CONTEXT.md output contracts
- Create minimal implementations that satisfy interface requirements
- Focus on stable API contracts for dependent segments

### Phase 4: Core Implementation
- Implement behavioral requirements to satisfy test criteria
- Follow established patterns from HANDOFF.md integration requirements
- Maintain focus on performance and quality validation requirements

### Phase 5: Test Validation
- Run unit tests until passing (green phase)
- Run integration/E2E test gates until passing
- Validate integration patterns work with dependency interfaces

### Phase 6: Handoff Generation
- Document implemented interfaces using IMPLEMENTATION_HANDOFF_TEMPLATE.md
- Provide integration patterns and requirements for dependent segments
- Include test validation results and performance benchmarks

## Testing Strategy

### Contract Fulfillment
Segment contracts are only fulfilled when all unit tests, integration tests, and segment-level E2E tests pass for the segment.

### E2E Test Immutability
- E2E tests are created before segment implementation begins and cannot be modified by implementation stages
- Tests serve as immutable behavioral contracts that implementation must satisfy

## Output Requirements
- **HANDOFF.md**: Level 5-6 specifications (see @ABSTRACTION_FRAMEWORK.md), algorithm specifications, exact method contracts, integration patterns
- **Working Implementation**: All code necessary to satisfy behavioral contracts
- **Test Validation Results**: Proof that all required tests pass

## Critical Constraints
- **Test Immutability**: Cannot modify E2E or integration test specifications
- **Contract Compliance**: All behavioral requirements must be satisfied through test validation
- **Integration Focus**: Must provide stable interfaces for dependent segments
- **Quality Gates**: All performance and quality criteria must be met
- **Critical Failure Protocol**: Any problem this sub-process cannot resolve independently (e.g., E2E/integration test errors without permission to fix, unresolvable implementation issues) constitutes critical failure → return control to coordination stage → escalate to user

## Success Criteria
- All unit tests, integration tests, and segment-level E2E tests pass
- Contract fulfillment achieved through test validation
- Handoff document provides complete integration specifications for dependent segments