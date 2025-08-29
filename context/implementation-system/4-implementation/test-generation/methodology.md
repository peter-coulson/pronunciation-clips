# Test Generation Methodology

## Sub-Agent Purpose
Transforms immutable Level 4 test specifications (see @ABSTRACTION_FRAMEWORK.md) and testing context into executable test implementations that validate system behavior at both E2E and integration levels.

## Input Requirements

### Level 4 Test Specifications (Immutable)
- **LEVEL_4_E2E_TEST_SPECIFICATION.md**: Method signatures, validation targets, test fixtures, success assertions, performance thresholds, error test signatures, test data schemas
- **LEVEL_4_INTEGRATION_TEST_SPECIFICATION.md**: Integration test methods, mock signatures, data flow tests, error integration signatures, contract validation signatures, state consistency tests

### Testing Context
- **TEST_CONTEXT_TEMPLATE.md**: Testing framework constraints, infrastructure patterns, quality standards, existing test analysis, development integration patterns

## Execution Pipeline

### Phase 1: Specification Parsing
- Extract structured test data from Level 4 specifications
- Validate specification completeness and format
- Create internal representation without modifying source files

### Phase 2: Context Analysis  
- Parse testing infrastructure constraints
- Identify existing test patterns and conventions
- Extract framework versions and configuration requirements

### Phase 3: Rule-Based Mapping
- Map specification elements to test implementation patterns
- Apply context constraints to test structure decisions
- Generate test method signatures and assertion strategies

### Phase 4: Template-Based Generation
- Select appropriate templates based on test type and context
- Inject parsed data and context into templates
- Generate executable test files with proper imports and setup

### Phase 5: Validation
- Verify generated tests match specification requirements
- Ensure pattern consistency with context constraints
- Validate executable syntax and structure

## Output Generation
- **Executable E2E Test Files**: Direct specification implementation
- **Executable Integration Test Files**: Component boundary validation
- **Test Support Files**: Fixtures, mocks, helpers as needed
- **Configuration Files**: Test-specific configuration alignment

## Critical Constraints
- **Specification Immutability**: Cannot modify input test specifications under any circumstances
- **Stateless Operation**: Each execution operates independently without persistent state
- **Context Compliance**: All outputs must respect infrastructure constraints and patterns
- **Quality Standards**: Generated tests must meet all specified coverage and performance requirements
- **Critical Failure Protocol**: Any problem this sub-agent cannot resolve independently constitutes critical failure → return control to coordination agent → escalate to user

## Success Criteria
- **Executable Tests**: All generated tests run successfully in target environment
- **Pattern Consistency**: Tests follow established project testing patterns and conventions
- **Specification Compliance**: All test assertions validate exact behaviors specified in Level 4 contracts
- **Infrastructure Integration**: Tests integrate seamlessly with existing CI/CD and development workflows