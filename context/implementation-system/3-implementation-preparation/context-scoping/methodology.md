# Phase 2: Knowledge Context Division

## Objective
Transform Phase 1 segment boundaries into implementation-ready context templates while extracting system-wide testing context through unified knowledge filtering from the comprehensive knowledge base.

## Input Requirements
- **SEGMENTATION_ANALYSIS_TEMPLATE.md** (Primary - defines segments)
- **Level 2-6 Specification Templates** (Implementation requirements)
- **Context Extraction Output** (Knowledge base for filtering)

*Specification levels defined in @ABSTRACTION_FRAMEWORK.md*

## Process Steps

### Step 0: System-Wide Testing Context Extraction
Extract testing knowledge from Context Extraction Output to create execution-ready testing environment:
- **Testing Framework Constraints**: Framework versions, execution environments, assertion libraries
- **Testing Infrastructure Patterns**: Test organization, configuration management, quality standards
- **Testing Integration Patterns**: CI/CD integration, development workflow, error handling conventions
- **Existing Test Analysis**: Current test file patterns, established testing approaches, mock strategies
- **Test Data Management**: Fixture storage patterns, test data generation approaches, cleanup strategies
- **Development Integration**: Test execution commands, IDE integration patterns, debug configurations

### Step 1: Segment-Centric Specification Extraction
For each segment from implementation segmentation, extract relevant specifications across all levels:
- **Architecture (L2)**: Component relationships affecting this segment
- **Interface (L3)**: Contract definitions this segment implements/consumes  
- **Behavior (L4)**: Functional requirements within segment scope
- **Testing (L4 E2E/Integration)**: Validation requirements for segment boundaries

### Step 2: Real-Time Knowledge Filtering
Simultaneously apply filtered knowledge from Context Extraction based on extracted specifications (see @ABSTRACTION_FRAMEWORK.md for Universal Knowledge Categories definitions):

### Step 3: Context Template Population
Generate implementation-ready context templates with:
- Segment-specific specifications organized by abstraction level
- Filtered contextual knowledge mapped to specification elements
- Implementation guidance based on pattern/convention knowledge
- Risk prevention notes from constraint/integration knowledge

## Methodology Principles
1. **Dependency-Driven**: Specification extraction informed by Phase 1 dependencies
2. **Knowledge-Validated**: Every specification element validated against relevant knowledge categories
3. **Implementation-Ready**: Output templates contain both requirements and contextual guidance
4. **Risk-Preventive**: Knowledge filtering prevents Universal Risk Types (see @ABSTRACTION_FRAMEWORK.md)

## Output
- **TEST_CONTEXT.md**: System-wide testing knowledge for execution setup
- Implementation-ready **CONTEXT_TEMPLATE.md** files for each segment containing integrated specifications and filtered knowledge, ready for Phase 3 execution orchestration.

## Success Criteria
- System-wide testing context extracted for execution setup stage
- Each segment has complete specification coverage across relevant abstraction levels
- Knowledge filtering prevents Universal Risk Types per @ABSTRACTION_FRAMEWORK.md
- Context templates enable independent segment implementation
- Template token limits maintained for execution feasibility