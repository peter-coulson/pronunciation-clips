# Test-Driven Implementation Methodology

## Process Flow

### 1. Input Analysis
- Parse CONTEXT.md for behavioral requirements and test gates
- Extract interface contracts from HANDOFF.md (if present)
- Identify implementation scope and dependencies

### 2. Unit Test Creation
- Extract specific testing requirements from CONTEXT.md Quality Validation Requirements
- Apply testing patterns and conventions from Applied Context Knowledge sections
- Write unit tests covering all behavioral validations and performance criteria
- Create tests for all output contracts this chunk must provide
- Verify tests fail initially (red phase)
- Confirm integration/E2E test infrastructure is functional

### 3. Contract Implementation
- Implement public interfaces specified in CONTEXT.md output contracts
- Create minimal implementations that satisfy interface requirements
- Focus on stable API contracts for dependent chunks

### 4. Core Implementation
- Implement behavioral requirements to satisfy test criteria
- Follow established patterns from HANDOFF.md integration requirements
- Maintain focus on performance and quality validation requirements

### 5. Test Validation
- Run unit tests until passing (green phase)
- Run integration/E2E test gates until passing
- Validate integration patterns work with dependency interfaces

### 6. Handoff Generation
- Document implemented interfaces using HANDOFF_TEMPLATE.md
- Provide integration patterns and requirements for dependent chunks
- Include test validation results and performance benchmarks

## Success Criteria
All required tests pass and handoff contract is complete for dependent chunks.