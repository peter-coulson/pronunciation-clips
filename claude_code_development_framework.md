# Claude Code Development Framework

## Purpose & Scope
This document serves as the master development strategy for complex Claude Code projects. It defines portable methodologies, patterns, and systems that can be applied across different project types while maintaining consistency and quality.

The framework addresses three core challenges:
1. **Specification Quality**: Front-loading critical decisions to prevent late-stage rework
2. **Context Management**: Efficient information organization for token-constrained environments
3. **Implementation Discipline**: Technical enforcement mechanisms that maintain standards

## Overview
This framework enables rapid, high-quality software development using Claude Code by combining upfront planning with rigorous testing discipline and technical enforcement mechanisms.

## Development Process (11 Stages)

### **1. Define Business Logic & Goals**
- Articulate core problem and success criteria
- Define scope boundaries (MVP vs future state)
- Establish user workflows and value propositions

### **2. Initial Technology Testing**
- Run basic scripts to validate technology choices
- Test integration points and performance characteristics
- Identify technical constraints and requirements

### **3. Gather Technical Knowledge**
- Document findings from testing in markdown
- Capture performance metrics, configuration values
- Record critical implementation insights

### **4. Refine Project Goals & Architecture**
- Update business logic based on technical findings
- Design for future extensibility and integration
- Create CLAUDE.md with refined project vision

### **5. Define Standards & Practices**
- Establish coding standards and conventions
- Define error handling patterns
- Set logging and observability requirements

### **6. Design Specifications & Architecture**
- Make architectural decisions through collaborative discussion
- Create detailed implementation plan
- Define module structure and responsibilities
- **Add initial testing results back into context once specifications are completed for final modifications**
- This prevents solution anchoring while incorporating real-world constraints

### **7. Define Testing Strategy**
- Establish test layer progression (Unit → Integration → E2E)
- Create immutable E2E test contracts
- Define success criteria for each stage

### **8. Sequential Implementation Stages**
- Order modules with clear dependencies
- Define start/finish parameters for each stage
- Create stage gate requirements

### **9. End-to-End Test Definition**
- Write comprehensive E2E tests before implementation
- Include integration with dependent modules
- Ensure extensive functional coverage

### **10. Finalize CLAUDE.md Instructions**
- Document testing rules and progression requirements
- Define commit/push strategy and cleanup rules
- Establish technical enforcement mechanisms

### **11. Technical Enforcement Setup**
- Implement rules through settings.json, permissions.deny
- Create pre-commit hooks and validation scripts
- Enable automated compliance checking

### **12. Implementation with Full Permissions**
- Execute implementation following established framework
- Maintain discipline through technical enforcement
- Validate against original specifications

## Key Framework Principles

### **Front-Load Critical Decisions**
- All architectural decisions made before implementation
- Immutable test contracts prevent scope creep
- Technical constraints identified early

### **Rigorous Testing Discipline**
- E2E tests define success criteria upfront
- Unit tests for every file/change
- Integration tests before module completion
- Never modify E2E tests during implementation

### **Technical Enforcement**
- Use Claude Code settings and permissions for hard limits
- Automate rule compliance checking
- Prevent common violation patterns

### **Staged Progression**
- Clear stage gates with measurable criteria
- No advancement until all tests pass
- Git commits only after stage completion

## Critical Success Factors

### **Specification Quality**
- Explicit data types and interfaces
- Clear automation vs manual boundaries
- Negative examples and anti-patterns
- Performance and storage implications

### **Communication Patterns**
- Upfront clarification over post-hoc justification
- Verify understanding at each milestone
- Ask specification questions immediately

### **Process Discipline**
- Follow test layer progression religiously
- Maintain clean working directory
- Document all deviations with approval
- Regular rule compliance audits

## Context Management System

### **Structure Organization**
```
/context/
├── domains/           # Core knowledge domains
│   ├── architecture.md    # System design, patterns, dependencies
│   ├── standards.md      # Coding practices, conventions, patterns
│   ├── testing.md        # Testing strategies, fixtures, validation
│   ├── data.md           # Models, schemas, processing logic
│   └── deployment.md     # Build, config, environment setup
├── workflows/         # Task-oriented contexts  
│   ├── current-task.md   # Active work context
│   ├── debugging.md      # Error patterns, troubleshooting
│   ├── extending.md      # Adding features, scaling patterns
│   ├── refactoring.md    # Code improvement strategies
│   └── performance.md    # Optimization approaches
├── stages/            # Development stage contexts
│   ├── stage1-foundation.md
│   ├── stage2-audio.md
│   └── [continue for each stage]
└── reference/         # Quick lookup contexts
    ├── apis.md           # Key interfaces, contracts
    ├── configs.md        # Settings, parameters, examples  
    └── troubleshooting.md # Common issues, solutions
```

### **CLAUDE.md Entry Point Strategy**
- **Lightweight router**: Navigation hub, current state, core rules only
- **Progressive disclosure**: Load detailed contexts only when needed
- **Token efficiency**: Keep entry point under 30 lines
- **Context links**: Explicit references to relevant context files

### **Context Distribution Principles**

#### **What Goes in CLAUDE.md (Root)**
- Current project state and active stage
- Core development rules (immutable tests, sequential stages)
- Navigation links to context domains
- Quick command references

#### **What Goes in Domain Files**
- **standards.md**: Coding practices, error handling, conventions
- **testing.md**: Test strategies, fixtures, validation rules
- **architecture.md**: Module structure, dependencies, interfaces
- **[stage-N].md**: Stage-specific implementation details

### **Token Efficiency Guidelines**
- **Conditional loading**: Load contexts only when relevant to current task
- **Reference patterns**: Use `See /context/domain/file.md` instead of embedding
- **Context versioning**: Update contexts with stage progression
- **Avoid duplication**: Single source of truth for each concept

### **Context Usage Patterns**
- **New chat startup**: Load only CLAUDE.md + current-task.md
- **Debugging session**: Add workflows/debugging.md
- **Architecture changes**: Load domains/architecture.md
- **Code implementation**: Add domains/standards.md + domains/testing.md
- **Stage transitions**: Update stage-specific contexts

### **Context Maintenance Rules**
- Update contexts immediately after stage completion
- Version control all context files with code changes  
- Remove obsolete contexts to prevent confusion
- Keep context files focused on single concerns
- Test context effectiveness by starting fresh chats

## Context System Design Rationale

### **Problem Statement**
Complex Claude Code projects face a token efficiency crisis: loading all project context into every conversation wastes tokens and reduces focus. Traditional approaches either overwhelm Claude with irrelevant details or provide insufficient context for quality work.

### **Solution Architecture**
The four-domain context system implements progressive disclosure through:

1. **Role Separation**: CLAUDE.md serves as lightweight navigation hub (< 30 lines) while detailed contexts load on demand
2. **Domain Organization**: Knowledge separated into logical domains (architecture, standards, testing, data, deployment) 
3. **Task-Oriented Loading**: Context selection based on current work type (implementation, debugging, extending)
4. **Single Source of Truth**: Each concept documented exactly once with explicit cross-references

### **Current Implementation: MVP Manual System**
**Status**: Manual context loading with organizational benefits only

**What Works Now:**
- Clean 4-domain file organization enables easy navigation
- CLAUDE.md navigation hub provides clear entry points
- Progressive disclosure reduces cognitive load
- Structured contexts improve information findability

**What Doesn't Work Yet:**
- No automated context selection (Claude chooses files manually)
- No XML wrapping or structured document processing
- Context rules exist as documentation only
- Metadata headers serve no functional purpose

### **Future Enhancement Path: Automated Context Management**

#### **Phase 1: Smart Context Selection (Token Savings: 20-40%)**

**Implementation:** Task Agent Integration
```markdown
## Dynamic Context Loading Protocol
For complex tasks requiring context understanding:
1. Use Task agent to analyze user request keywords
2. Agent reads context_rules.yaml for selection patterns
3. Agent loads only relevant context sections (not full files)
4. Agent returns XML-wrapped context for processing

Benefits:
- Selective content loading vs loading entire files
- Keyword-driven context selection
- 4,000-6,000 token savings per session
```

**Upgrade Indicators:**
- Context files growing beyond 200 lines each
- Frequently loading irrelevant context sections
- Claude showing confusion from information overload
- Token usage approaching conversation limits

#### **Phase 2: XML Document Processing (Processing Quality: 15-30% improvement)**

**Implementation:** Anthropic-Optimized Structure
```xml
<documents>
  <document index="N">
    <source>context/path/file.md</source>
    <last_updated>auto-generated</last_updated>
    <triggers>from-metadata-headers</triggers>
    <document_content>[selective content]</document_content>
  </document>
</documents>
```

**Benefits:**
- Precise source attribution: "from document 1, architecture.md"
- Noise reduction through clear document boundaries
- Enhanced Claude processing through structured inputs
- Better quote extraction and context referencing

**Upgrade Indicators:**
- Claude making attribution errors or vague references
- Need for precise source tracking across multiple contexts
- Complex multi-document reasoning tasks becoming common
- Quality issues from Claude processing mixed context sources

#### **Phase 3: Metadata-Driven Automation (Maintenance: 50% reduction)**

**Implementation:** YAML Frontmatter Processing
```yaml
---
triggers: ["architecture", "design", "dependencies"]
task_types: ["planning", "refactoring", "understanding"]  
load_with: ["standards.md", "current-task.md"]
relevance_score: 0.9
---
```

**Benefits:**
- Automatic context relevance scoring
- Smart co-loading of related contexts
- Maintenance rules automated through metadata
- Consistent context selection patterns

**Upgrade Indicators:**
- Managing 10+ context files becomes cumbersome
- Inconsistent context loading patterns between team members
- Need for automated context validation and maintenance
- Context relationships becoming complex and hard to track

### **Implementation Sequence & ROI Analysis**

#### **When to Upgrade: Clear Indicators**

**Phase 1 Triggers** (Smart Context Selection):
- Project context exceeds 50,000 tokens total
- Regularly loading 3+ context files for single tasks
- Token usage hitting session limits frequently
- 30+ minutes spent per session on context management

**Phase 2 Triggers** (XML Processing):
- Multi-document reasoning tasks common (>30% of sessions)
- Claude attribution becoming unreliable or vague
- Need for precise cross-reference tracking
- Complex context analysis requiring source isolation

**Phase 3 Triggers** (Metadata Automation):
- 15+ context files requiring management
- Team consistency issues with context loading
- Monthly context maintenance taking >2 hours
- Context relationship complexity causing errors

#### **ROI Estimates by Phase**

**Phase 1: Smart Selection**
- **Implementation Cost**: 2-4 hours setup
- **Token Savings**: 20-40% per session  
- **Time Savings**: 5-10 minutes per coding session
- **Break-even**: After ~20 coding sessions

**Phase 2: XML Processing**  
- **Implementation Cost**: 4-8 hours setup
- **Quality Improvement**: 15-30% better context processing
- **Attribution Accuracy**: 90%+ improvement
- **Break-even**: When multi-document tasks >30% of work

**Phase 3: Metadata Automation**
- **Implementation Cost**: 8-16 hours setup  
- **Maintenance Reduction**: 50% less context management overhead
- **Consistency Improvement**: 80%+ reduction in context selection errors
- **Break-even**: When context maintenance >2 hours/month

### **Portability Design**
The system separates portable structure from project-specific content:

#### **Portable Elements**
- Four-domain structure (domains/workflows/stages/reference)
- Progressive disclosure patterns and token efficiency principles
- Maintenance discipline and update timing rules
- Context loading strategies by task type
- Upgrade path and implementation phases

#### **Project-Specific Elements**
- Actual domain content (architecture decisions, coding standards)
- Stage definitions and implementation progression
- Workflow patterns specific to project type
- Reference materials and API contracts
- Specific context rules and metadata values

#### **Framework Evolution Strategy**
1. **Perfect in current implementation**: Refine context system until proven effective
2. **Extract portable patterns**: Identify universal principles vs project-specific content
3. **Create template system**: Develop scaffolding for rapid setup in new projects
4. **Validate across project types**: Test portability with different development contexts
5. **Assess token usage and upgrade indicators**: Track context complexity and automation needs

## Chunk Development System

### **Purpose & Scope**
The Chunk Development System addresses context window limitations and enables parallel execution for single modular units of code. It operates within the existing 11-stage framework, specifically enhancing Stage 12 implementation by breaking large modules into manageable, contract-driven development chunks.

### **Chunk Definition**
A **chunk** is a single modular unit of code that:
- Has a clear, testable interface contract
- Can be implemented within ~2000 token context window
- Represents a cohesive functional component
- Has well-defined inputs and outputs
- Can be tested independently with unit and integration tests
- Maps to one or more files/functions with logical boundaries

### **Chunk Development Principles**

#### **1. Context Containment**
- Each chunk maintains isolated context (~2000 tokens maximum)
- Interface contracts enable independence from other chunks
- Context handoffs provide clean continuation between chunks
- No global project context required during chunk implementation

#### **2. Contract-Driven Development**
- All chunk interfaces defined before implementation begins
- Interface contracts are immutable once chunk development starts
- Data structures, function signatures, and error handling specified upfront
- Contract compliance validated through automated testing

#### **3. Test Hierarchy Preservation**
- Unit tests written and passing before chunk completion
- Integration tests validate chunk interfaces work together
- E2E tests remain immutable and validate complete module functionality
- Test progression: Unit (per chunk) → Integration (chunk groups) → E2E (complete module)

#### **4. Parallel Execution Ready**
- Chunks designed for independent parallel development
- Dependencies explicitly declared through interface contracts
- No shared mutable state between parallel chunks
- Coordination points clearly defined for sequential dependencies

### **Chunk Development Architecture**

#### **Chunk Organization Structure**
```
module-implementation/
├── module-contracts.yaml          # Interface contracts for all chunks
├── chunks/
│   ├── chunk-01-foundation/
│   │   ├── CHUNK-CONTEXT.md       # Chunk-specific implementation context
│   │   ├── INTERFACE-CONTRACT.yaml # This chunk's input/output contracts
│   │   └── HANDOFF.md             # Generated context for next chunks
│   ├── chunk-02-processing/
│   └── chunk-03-integration/
├── tests/
│   ├── unit/                      # Per-chunk unit tests
│   ├── integration/               # Cross-chunk integration tests
│   └── e2e/                       # Complete module E2E tests
└── CHUNK-COORDINATION.md          # Overall progress and coordination
```

#### **Contract Definition System**
```yaml
# module-contracts.yaml
module_name: "CLI Interface"
total_chunks: 7
chunk_dependencies:
  chunk-02: [chunk-01]
  chunk-04: [chunk-01, chunk-02, chunk-03]
  chunk-07: [chunk-01, chunk-02, chunk-03, chunk-04, chunk-05, chunk-06]

contracts:
  chunk-01:
    name: "CLI Foundation & Configuration"
    inputs: []
    outputs:
      - CLIConfig: "Validated configuration object"
      - setup_logging(): "Logging configuration function"
    interface_file: "chunks/chunk-01-foundation/INTERFACE-CONTRACT.yaml"
    
  chunk-02:
    name: "Command Argument Parsing"
    inputs:
      - CLIConfig: "Configuration object structure"
    outputs:
      - parse_args(): "Function returning CLIConfig from CLI arguments"
      - validate_paths(): "Path validation function"
    interface_file: "chunks/chunk-02-processing/INTERFACE-CONTRACT.yaml"
```

#### **Chunk Context Template**
```markdown
# CHUNK-CONTEXT.md Template
## Chunk Identification
- **Chunk ID**: [module]-[chunk-number]-[name]
- **Module**: [Parent module name]
- **Dependencies**: [List of required completed chunks]
- **Parallel Group**: [Group number for parallel execution]
- **Token Budget**: ~2000 tokens maximum

## Interface Contract
### Inputs (from dependencies)
```yaml
required_interfaces:
  - contract_name: "Type/description from dependency chunks"
```

### Outputs (for dependent chunks)
```yaml  
provided_interfaces:
  - contract_name: "Type/description this chunk provides"
```

## Implementation Scope
- **Files**: [Specific files and line ranges]
- **Functions**: [Primary functions to implement]
- **Classes**: [Classes to create/modify]
- **Dependencies**: [External libraries, internal modules]

## Context Loading Requirements
- **Load Files**: [Minimal set of files needed for context]
- **Load Contracts**: [Specific interface contracts needed]
- **Load Patterns**: [Existing code patterns to follow]

## Success Criteria
- **Unit Tests**: [Number] unit tests passing
- **Interface Compliance**: All output contracts satisfied
- **Performance Requirements**: [Specific performance criteria]
- **Integration Points**: Ready for dependent chunks

## Implementation Guidelines
- **Error Handling**: [Specific error handling requirements]
- **Logging**: [Logging requirements and patterns]
- **Code Style**: [Style guidelines and conventions]
- **Security Considerations**: [Security requirements]

## Future Extension Points
- **Parallel Agent Ready**: Context structured for potential agent specialization
- **Review Integration**: Prepared for separate review agent analysis
- **Test Agent Compatibility**: Test requirements specified for independent test generation
```

### **Chunk Development Process (MVP)**

#### **Phase 1: Chunk Planning & Contract Definition**
**Duration**: 30-60 minutes for complete module
**Deliverables**:
- Module breakdown into logical chunks (5-10 chunks typical)
- Complete interface contract definitions
- Dependency graph with parallel execution groups
- E2E test specification (immutable)

**Process**:
1. **Module Analysis**: Identify natural functional boundaries
2. **Chunk Sizing**: Ensure each chunk fits ~2000 token budget
3. **Interface Design**: Define all input/output contracts
4. **Dependency Mapping**: Create parallel execution groups
5. **E2E Test Creation**: Write immutable module-level tests

#### **Phase 2: Sequential Chunk Implementation**
**Duration**: 15-30 minutes per chunk
**Current MVP Approach**: Single-agent sequential development
**Future Enhancement**: Multi-agent parallel development

**Per-Chunk Process**:
1. **Context Loading**: Load CHUNK-CONTEXT.md + required contracts only
2. **Implementation**: Write production code within token budget
3. **Unit Testing**: Write and validate unit tests immediately
4. **Integration Validation**: Test chunk interfaces work with dependencies
5. **Handoff Generation**: Create context for dependent chunks

**Implementation Session Structure**:
```bash
# Session initiation
"Load CHUNK-CONTEXT.md for [chunk-id] and implement according to contract specifications"
"Token budget: 2000 tokens maximum"
"Focus only on this chunk's scope - ignore broader module context"

# Success validation
"Validate chunk completion:
1. All unit tests passing
2. Interface contracts satisfied  
3. Ready for dependent chunks
4. Generate HANDOFF.md for next chunks"
```

#### **Phase 3: Integration & Module Assembly**
**Duration**: 30-60 minutes
**Deliverables**:
- All chunks integrated and working together
- Integration tests passing
- E2E tests passing (validates complete module)
- Module ready for broader system integration

### **Parallel Execution Strategy (Future Enhancement)**

#### **Current MVP: Sequential Within Parallel Groups**
```bash
# Group 1 (Independent) - Implemented sequentially
Implement chunk-01 → Complete
Implement chunk-02 → Complete  
Implement chunk-03 → Complete

# Group 2 (Depends on Group 1) - Implemented sequentially
Implement chunk-04 → Complete
Implement chunk-05 → Complete
Implement chunk-06 → Complete

# Group 3 (Integration)
Implement chunk-07 → Complete
```

#### **Future Enhancement: True Parallel Execution**
**Agent Specialization Options**:
- **Implementation Agent**: Focuses on production code only
- **Test Agent**: Specializes in comprehensive test coverage
- **Review Agent**: Analyzes security, performance, and quality
- **Coordination Agent**: Integrates outputs and resolves conflicts

**Parallel Session Structure (Future)**:
```bash
# Within each chunk - parallel agent execution
Task A: "Implementation Agent: Implement chunk using IMPLEMENTATION-CONTEXT.md"
Task B: "Test Agent: Write comprehensive tests using TEST-CONTEXT.md"  
Task C: "Review Agent: Analyze implementation using REVIEW-CONTEXT.md"
# Coordination: "Integrate outputs from all three agents"
```

### **Integration with 11-Stage Framework**

#### **Enhanced Stage 12: Implementation with Chunking**
**Traditional Stage 12**:
- Monolithic implementation approach
- Large context windows (50K+ tokens)
- Sequential development only

**Enhanced Stage 12 with Chunking**:
- **Stage 12a**: Chunk planning and contract definition
- **Stage 12b**: Parallel chunk implementation (by groups)
- **Stage 12c**: Module integration and E2E validation
- **Stage 12d**: System integration preparation

#### **Testing Strategy Integration**
- **Unit Tests**: Per-chunk, immediate feedback
- **Integration Tests**: Per-group, validates chunk contracts
- **E2E Tests**: Per-module, immutable validation of complete functionality
- **System Tests**: Cross-module, final validation

#### **Context Management Integration**
- **CLAUDE.md**: Updated with chunk completion status
- **Chunk Contexts**: Isolated, focused implementation contexts
- **Handoff Documents**: Clean context transfer between chunks
- **Coordination Context**: Overall progress and dependency tracking

### **Benefits & Trade-offs**

#### **Benefits**
- **Context Control**: 2K token chunks vs 50K+ monolithic contexts
- **Parallel Capability**: Independent chunks can be developed simultaneously
- **Error Isolation**: Chunk failures don't impact other chunks
- **Resumability**: Clean continuation points at chunk boundaries
- **Quality**: Focused testing and review per chunk
- **Scalability**: Large modules remain manageable

#### **Trade-offs**
- **Setup Overhead**: Contract definition and chunk planning required
- **Coordination Complexity**: Interface contracts must be managed
- **Integration Risk**: Chunks must work together correctly
- **Testing Overhead**: Multiple test levels required

#### **Risk Mitigation**
- **Interface Contracts**: Prevent integration issues through upfront design
- **Immutable E2E Tests**: Ensure module functionality is never compromised
- **Chunk Dependencies**: Explicit dependency management prevents conflicts
- **Context Handoffs**: Prevent rework and context loss

### **Success Metrics**
- **Development Speed**: 40-50% reduction in implementation time for large modules
- **Context Efficiency**: 95% reduction in token usage per development session
- **Quality Metrics**: Reduced defect density through focused testing
- **Maintainability**: Improved code organization and documentation
- **Team Scalability**: Foundation for parallel development adoption

### **Evolution Path**
1. **Current MVP**: Sequential chunk development with contract-driven interfaces
2. **Phase 2**: Parallel chunk execution within dependency groups
3. **Phase 3**: Multi-agent chunk development (implementation/test/review agents)
4. **Phase 4**: Automated chunk planning and contract generation
5. **Phase 5**: Cross-module chunk coordination and reuse

The Chunk Development System provides immediate benefits through context management and parallel execution capability while establishing the foundation for advanced multi-agent development workflows.