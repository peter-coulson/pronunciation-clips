# Context Gathering Methodology

## Overview
> Universal methodology for embedded context gathering across all agents
> Eliminates knowledge-requirements and knowledge-extraction agent dependencies

## Universal 4-Step Process

### Step 1: Create Context Requirements Document
#### Purpose
Identify and document exactly what context, files, patterns, and domain knowledge the agent needs to complete its core task. Creates a concrete requirements specification that prevents assumptions and guides targeted context loading.

#### Process
- Analyze input specifications to determine context needs
- Identify required domain files from `/context/domains/`
- Identify required repository patterns and existing code
- Specify validation criteria for context completeness
- Use `/shared/templates/context-requirements.md` template

#### Deliverables
- Completed context requirements document
- Clear list of files/patterns to load
- Success criteria for context validation

#### Success Criteria
- All context needs explicitly identified
- Requirements are specific and actionable
- Validation criteria are measurable
- No assumptions about available context

### Step 2: Load Context and Create Partial Output Document
#### Purpose
Load identified context and create the agent's target output document with initial structure and any content that can be determined from loaded context alone. Prevents context corruption by capturing early insights before deep analysis.

#### Process
- Load all files specified in requirements document
- Read and organize loaded context by relevance
- Create target output document structure
- Fill in sections that can be completed from loaded context
- Use `/shared/templates/context-load-report.md` to document what was loaded

#### Deliverables
- Partially completed output document
- Context load report documenting what was loaded
- Clear indication of sections requiring further analysis

#### Success Criteria
- All required context successfully loaded
- Output document structure matches agent's specification
- Context load report confirms requirement coverage
- Partial content reflects only loaded context, no speculation

### Step 3: Complete Output Document
#### Purpose
Apply domain expertise and analysis to complete the output document using loaded context. Focus purely on task execution without additional context loading.

#### Process
- Analyze loaded context to complete remaining sections
- Apply domain-specific methodologies and patterns
- Ensure all outputs are grounded in loaded context
- Complete all required sections per agent specification

#### Deliverables
- Fully completed output document ready for validation
- All sections filled with context-grounded content

#### Success Criteria
- Output document is complete per agent specification
- All content is traceable to loaded context
- Domain expertise appropriately applied
- Output meets handoff requirements for next agent

### Step 4: Validate and Confirm Handoff Readiness
#### Purpose
Verify output completeness, validate against original context requirements, and confirm the deliverable is ready for the next stage in the implementation system.

#### Process
- Cross-check output against context requirements document
- Verify all required sections are complete and accurate
- Validate content quality and consistency
- Confirm handoff requirements are met
- Document any gaps or limitations

#### Deliverables
- Validation report confirming output quality
- Confirmed handoff readiness or identified gaps
- Updated output document if corrections needed

#### Success Criteria
- Output fully satisfies context requirements
- All quality checks pass
- Next agent can proceed without additional context gathering
- Clear handoff with no ambiguities or assumptions
