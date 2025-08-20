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