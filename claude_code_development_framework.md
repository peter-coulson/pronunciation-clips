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

### **Portability Design**
The system separates portable structure from project-specific content:

#### **Portable Elements**
- Four-domain structure (domains/workflows/stages/reference)
- Progressive disclosure patterns and token efficiency principles
- Maintenance discipline and update timing rules
- Context loading strategies by task type

#### **Project-Specific Elements**
- Actual domain content (architecture decisions, coding standards)
- Stage definitions and implementation progression
- Workflow patterns specific to project type
- Reference materials and API contracts

#### **Framework Evolution Strategy**
1. **Perfect in current implementation**: Refine context system until proven effective
2. **Extract portable patterns**: Identify universal principles vs project-specific content
3. **Create template system**: Develop scaffolding for rapid setup in new projects
4. **Validate across project types**: Test portability with different development contexts