# Context Gathering Methodology

## Overview
> Universal methodology for embedded context gathering across all agents
> Eliminates knowledge-requirements and knowledge-extraction agent dependencies

## Universal 3-Stage Process

### Stage 1: Identify Context Requirements
#### Purpose  
Identify and document exactly what context, files, patterns, and domain knowledge the agent needs to complete its core task. Creates a concrete requirements specification that prevents assumptions and guides targeted context loading.

#### Process
- Analyze input specifications to determine context needs
- Identify required domain files from `/context/domains/`
- Identify required repository patterns and existing code
- Specify validation criteria for context completeness
- Use `/shared/templates/CONTEXT_REQUIREMENTS_TEMPLATE.md` template

#### Deliverables
- Completed context requirements document
- Clear list of files/patterns to load
- Success criteria for context validation

#### Success Criteria
- All context needs explicitly identified
- Requirements are specific and actionable
- Validation criteria are measurable
- No assumptions about available context

### Stage 2: Load Required Context
#### Purpose
Systematically load all identified context and document what was obtained. Ensures comprehensive context gathering before task execution begins.

#### Process
- Load all files specified in requirements document
- Read and organize loaded context by relevance and priority
- Use `/shared/templates/CONTEXT_LOAD_REPORT_TEMPLATE.md` to document results
- Validate coverage against requirements document
- Flag any critical missing context that would block progress

#### Deliverables
- Context load report documenting what was loaded
- Organized context ready for task execution
- Coverage validation against requirements

#### Success Criteria
- All required context successfully loaded and documented
- Context load report confirms requirement coverage
- Any missing critical context identified and flagged
- Context is organized for efficient task execution

### Stage 3: Complete Output with Integrated Validation
#### Purpose
Execute the core task using loaded context and validate output completeness in a single integrated process. Ensures quality while eliminating redundant validation steps.

#### Process
- Create target output document structure
- Apply domain expertise and analysis to complete all sections
- Use loaded context to ground all decisions and outputs
- Continuously validate output against context requirements
- Cross-check completeness and quality during creation
- Confirm handoff requirements are met

#### Deliverables
- Fully completed output document ready for next agent
- Integrated validation confirming quality and completeness
- Clear handoff with no ambiguities or assumptions

#### Success Criteria
- Output document is complete per agent specification
- All content is traceable to loaded context
- Domain expertise appropriately applied
- Output fully satisfies context requirements
- Next agent can proceed without additional context gathering
