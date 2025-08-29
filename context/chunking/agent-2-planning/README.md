# Agent 2: Planning

## Agent Purpose
Iteratively converts high-level business logic into lower-level implementation specifications, stopping at Level 4. This approach prevents over-specification that would limit future agents' freedom for trial-and-error using Test-Driven Development (TDD), particularly beneficial for medium to large-scale changes.

**Exception**: End-to-end and integration tests are specified to Level 6 as they are implemented before any code and remain immutable. Since there's no trial-and-error benefit for these tests, full change context specification provides maximum value.

## Inputs
- **REQUIREMENTS_LEVEL_INPUT.md** - Completed requirements template from user
- **CONTEXT_EXTRACTION_OUTPUT.md** - Filled context extraction template from agent-1-requirements

Together, these inputs detail change goals plus system standards context required for implementation at every specification level, forcing adherence to project standards.

## Outputs
Complete implementation plan through Level 4 specification (see @ABSTRACTION_FRAMEWORK.md for specification level definitions):
- **Level 2**: Architecture Specification 
- **Level 3**: Interface Specification
- **Level 4**: Behavior Specification + E2E Test Specification + Integration Test Specification

## Usage Prerequisites
- High-quality completion of input templates
- No missing specifications in input files
- Context extraction must cover all required system knowledge

## Expected Outcomes
- All output templates filled to high quality
- No missing specifications
- No system context assumptions made
- Ready for agent-3-chunking consumption

## Agent Structure
- **architecture-interface/**: Creates Level 2 Architecture and Level 3 Interface specifications
- **behaviour-specification/**: Creates Level 4 Behavior and test specifications