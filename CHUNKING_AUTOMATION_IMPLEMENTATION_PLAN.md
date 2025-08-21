# Chunking System Automation - Implementation Plan

## Project Overview

**Objective**: Build automated chunking development system based on proven manual experiment results  
**Foundation**: Diarization experiment achieved 5/5 effectiveness with 95% contract accuracy and 120% development velocity  
**Scope**: Automate the complete chunking workflow from E2E test analysis to handoff generation

## Development Management and Context Strategy

### **Session-Based Development Approach**

**Development Methodology**: Build automated chunking system using manual Claude Code workflow with integrated context management

**Session Structure**:
```
Session 0: Context Setup and E2E Test Definition
Session 1: Stage 1 - Handoff Generation Engine
Session 2: Stage 2 - Context Isolation Engine  
Session 3: Stage 3 - Contract Validation Framework
Session 4: Stage 4 - Sequential Orchestration System
Session 5: Stage 5 - E2E Integration System
Session 6+: Domain Validation Testing
```

**Context Management System**:
```
chunking-framework/
├── context/                     # INTEGRATED: Single context system
│   ├── domains/                 # IMPORTED: Architecture, standards, testing
│   ├── chunking/                # IMPORTED: Experiment results, handoff examples
│   ├── workflows/               # NEW: Session-based development workflow
│   │   ├── session-state.md     # Current session context and objectives
│   │   └── chunking-framework-development.md # Framework development workflow
│   ├── framework/               # NEW: Framework-specific context
│   │   ├── implementation-plan.md # This document
│   │   ├── progress-tracking.md   # Implementation progress
│   │   └── sessions/            # Session handoffs and completions
│   └── stages/                  # IMPORTED: Stage definitions adapted for framework
```

**Minimal Prompting Workflow**:
- **Session Start**: `"Start chunking framework session: [SESSION_NAME]"`
  - Auto-reads `context/workflows/session-state.md`
  - Loads required context files automatically
  - Creates TodoWrite objectives from session state
- **Session Complete**: `"Complete current session and prepare next: [NEXT_SESSION]"`
  - Auto-generates session handoff
  - Updates session-state.md for next session
- **Session Resume**: `"Resume chunking framework development"`
  - Auto-reads current session state and continues

**Development Benefits**:
- **Self-Contained**: Framework repo operates independently with essential context imported
- **Resumable Development**: Complete session state preservation enables recovery anywhere
- **Progressive Context**: Each session builds naturally on previous session results
- **Manual Process Excellence**: Build automation using proven manual Claude Code methods

### **Complete Session Workflow**

**Session Start Workflow**:
1. **User Prompt**: `"Start chunking framework session: [SESSION_NAME]"`
2. **Context Loading** (Automatic):
   - Read `context/workflows/session-state.md` for current objectives
   - Read `context/framework/implementation-plan.md` (relevant sections)
   - Read `context/framework/sessions/session-[N-1].md` (previous session results)
   - Read relevant examples from `context/chunking/examples/`
3. **Session Initialization**:
   - TodoWrite objectives from session state
   - Review success criteria and implementation boundaries
   - Confirm context completeness

**Session Implementation Workflow**:
4. **Development Phase**: Use standard Claude Code tools (Read, Write, Edit, Bash)
   - Implement session objectives using TDD approach
   - Create unit/integration tests as part of implementation
   - Validate against E2E tests and success criteria
5. **Testing Phase**: Run tests and validate implementation
   - Execute unit tests: `pytest tests/unit/`
   - Execute integration tests: `pytest tests/integration/`
   - Execute relevant E2E tests: `pytest tests/e2e/test_stage[N]_*.py`

**Session Completion Workflow**:
6. **User Prompt**: `"Complete current session and prepare next: [NEXT_SESSION_NAME]"`
7. **Session Handoff Generation** (Manual):
   - Write `context/framework/sessions/session-[N]-[NAME].md` (session completion handoff)
   - Edit `context/workflows/session-state.md` (prepare next session context)
   - Update `context/framework/progress-tracking.md` (mark completion status)
8. **Context Preparation for Next Session**:
   - Generate next session objectives based on implementation plan
   - Prepare required context files for next session
   - Document interfaces and dependencies created

**Session Recovery Workflow**:
- **User Prompt**: `"Resume chunking framework development"`
- **Context Restoration**: Auto-read current session state and continue from last checkpoint

### **System Analysis and Review Capabilities**

**Core Analysis Functions** (What the finished system will provide):
1. **Codebase Analysis**: Automated analysis of existing codebases to identify optimal chunk boundaries
2. **Interface Extraction**: AST-based extraction of classes, functions, and integration points
3. **Dependency Mapping**: Analysis of file dependencies and import relationships
4. **Context Packaging**: Automated selection and packaging of relevant context for each chunk
5. **Progress Tracking**: Systematic tracking of chunk completion and integration status

**Review and Validation Capabilities**:
- **Contract Validation**: Verify implementations match predicted interfaces
- **Integration Compatibility**: Ensure chunk handoffs work together seamlessly
- **Quality Assessment**: Compare generated handoffs against proven quality benchmarks
- **Context Sufficiency**: Validate context packages enable focused implementation

## Development Environment Setup

### **DevOps Configuration**

**Repository Structure**:
```bash
# Create framework subfolder (from pronunciation-clips root)
mkdir chunking-framework && cd chunking-framework
git init && git checkout -b develop
cd .. && echo "chunking-framework/" >> .gitignore
```

**Python Environment**:
```bash
cd chunking-framework
python -m venv venv && source venv/bin/activate
# pyproject.toml setup with lightweight dependencies (~20MB)
pip install -e ".[dev,test]" && pre-commit install
```

**Context Integration**:
```bash
# Import essential proven patterns
mkdir -p context/{domains,chunking,workflows,framework,stages}
cp -r ../context/domains/standards.md context/domains/
cp -r ../context/domains/architecture.md context/domains/
cp -r ../context/chunking/examples/ context/chunking/
cp ../CHUNKING_AUTOMATION_IMPLEMENTATION_PLAN.md context/framework/implementation-plan.md
```

### **Testing Framework Setup**

**Test Structure**:
```bash
mkdir -p tests/{unit,integration,e2e}
# Session 0 creates comprehensive E2E tests first
# Each implementation session creates corresponding unit/integration tests
```

**Testing Dependencies**:
```toml
[project.optional-dependencies]
test = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21", 
    "pytest-mock>=3.10",
    "pytest-benchmark>=4.0",  # Performance measurement
]
```

**Test Execution Strategy**:
- **E2E Tests**: Created in Session 0, guide all implementation
- **Unit Tests**: Created during each implementation session for immediate components
- **Integration Tests**: Created during each session for cross-component functionality
- **Test Validation**: Each session validates against relevant E2E test subset

## Test-Driven Development Strategy

### **TDD Philosophy: E2E Test Immutability + Lightweight Validation**

**Core Principle**: Define comprehensive E2E tests before any implementation, then build automation to pass these tests using lightweight validation rather than heavyweight NLP dependencies.

**Testing Architecture - Multi-Layer Validation**:
1. **Unit Tests** (Traditional TDD) - Deterministic components (AST parsing, file analysis)
2. **Structure Validation** - Document format compliance, template matching
3. **Interface Accuracy** - AST-based validation of predicted vs actual interfaces  
4. **Workflow Integration** - Claude Code script orchestration testing
5. **E2E Outcome Validation** - Complete chunking workflow effectiveness

### **Phase 1 TDD Implementation (Phase 2A Foundation)**

**Week 1: Define All E2E Tests Before Implementation**

**E2E Test Creation Sequence**:
```
tests/e2e/test_stage1_handoff_generation_e2e.py    # 90% handoff quality vs HANDOFF-2.md
tests/e2e/test_stage2_context_isolation_e2e.py     # 4.5+ context sufficiency, 3-4K tokens
tests/e2e/test_stage3_contract_validation_e2e.py   # 95% contract accuracy baseline
tests/e2e/test_stage4_orchestration_e2e.py         # Sequential workflow automation
tests/e2e/test_stage5_integration_e2e.py           # Complete system integration
tests/e2e/test_full_workflow_e2e.py                # End-to-end chunking effectiveness
```

**Lightweight Validation Dependencies (~20MB total)**:
- `pyyaml` (500KB) - Contract specifications and progress tracking
- `markdown` (200KB) - Handoff document parsing and structure validation
- `psutil` (500KB) - Performance monitoring and development velocity measurement
- **Built-in Python**: AST parsing, template matching, file analysis

**Key Testing Technologies**:

**Structure Validation** (No dependencies):
- Template compliance scoring using text pattern matching
- Required sections validation against HANDOFF-2.md structure
- Interface completeness ratios (documented/total interfaces)
- Context token counting with built-in tokenization

**Interface Accuracy** (Built-in AST):
- Parse implementations to extract actual classes/functions/methods
- Compare predicted interfaces vs AST-extracted reality
- Calculate precision/recall for interface predictions
- Validate data types and method signatures match contracts

**Workflow Integration** (Built-in subprocess):
- Test Claude Code script orchestration via bash command execution
- Validate automation script integration points work correctly
- Progress tracking validation through file system state
- Error handling and recovery testing

**Outcome Measurement**:
- Development velocity tracking through time measurement
- Focus maintenance through context usage analysis
- Integration reliability through handoff compatibility testing
- Contract accuracy through post-implementation validation

**TDD Implementation Sequence**:

**Red Phase** (Week 1): All E2E tests fail initially
- Define exact success criteria based on experiment metrics
- Create validation benchmarks using proven HANDOFF-2.md example
- Establish measurement baselines for all effectiveness metrics

**Green Phase** (Week 2-3): Implement minimal automation to pass tests  
- Focus on achieving benchmark quality through structure validation
- Implement Claude Code integration points with lightweight validation
- Build against proven templates rather than semantic sophistication

**Refactor Phase** (Week 4): Optimize for reliability and cross-domain effectiveness
- Improve validation accuracy based on test feedback
- Enhance automation quality through iterative refinement
- Optimize for consistent results across different implementation contexts

### **Cross-LLM Compatibility Testing Strategy**

**LLM Abstraction Design**: Framework tests automation outputs, not LLM-specific behavior
- Tests validate **Claude Code's chunking automation** produces quality results
- Validation logic is deterministic and LLM-agnostic
- Success measured through outcome effectiveness, not process specifics

**Future Expansion Notes**: 
- **Tech Stack Specialization**: Add domain-specific validation as needed (Python AST vs TypeScript parsing)
- **Enhanced Quality Metrics**: Consider NLP-based validation only if lightweight validation proves insufficient
- **Cross-Domain Patterns**: Systematic validation expansion based on actual usage patterns rather than theoretical coverage

## Repository Structure & DevOps Setup

### **Subfolder Repository Architecture**

**Repository Strategy**: Create `chunking-framework` as git-ignored subfolder within current repository, maintaining independent git history while enabling selective context import

**Hybrid Repository Structure**:
```
pronunciation-clips/                   # Main audio processing project
├── .gitignore                        # Add: chunking-framework/
├── chunking-framework/               # NEW: Independent git repository as subfolder
│   ├── .git/                        # Separate git history for framework
│   ├── CLAUDE.md                    # Framework-specific development instructions
│   ├── pyproject.toml               # Lightweight dependencies (~20MB)
│   ├── context/                     # IMPORTED proven patterns
│   │   ├── reference/               # Selective import from ../context/
│   │   │   ├── handoff-examples/    # HANDOFF-*.md templates
│   │   │   └── standards.md         # Proven development standards
│   │   └── development/             # Framework-specific context
│   │       ├── architecture/        # Framework design decisions
│   │       └── validation/          # Testing and quality patterns
│   ├── src/
│   │   └── chunking_framework/
│   │       ├── analysis/            # Interface analysis, AST parsing
│   │       ├── generation/          # Handoff generation, context isolation
│   │       ├── validation/          # Contract validation, integration testing
│   │       └── orchestration/       # Sequential workflow management
│   ├── templates/
│   │   ├── handoff_templates/       # Generated from proven examples
│   │   └── context_templates/       # Context packaging templates
│   ├── scripts/
│   │   ├── generate-handoff.py      # Claude Code integration scripts
│   │   ├── prepare-context.py
│   │   ├── validate-contracts.py
│   │   └── orchestrate-chunks.py
│   ├── tests/
│   │   ├── unit/                    # Deterministic component testing
│   │   ├── integration/             # Cross-component integration
│   │   └── e2e/                     # Complete workflow validation
│   └── .github/
│       └── workflows/               # Independent CI/CD for framework
├── context/                         # EXISTING: Audio project context (preserved)
│   ├── chunking/                    # Proven experiment results (preserved)
│   └── domains/                     # Audio-specific context (preserved)
└── src/audio_to_json/               # EXISTING: Audio processing (preserved)
```

**Architectural Benefits**:
- **Clean Separation**: Framework dependencies (~20MB) isolated from ML dependencies (~500MB+)
- **Independent Development**: Separate git history, branching, CI/CD, versioning
- **Proven Pattern Import**: Selective import of 4.8/5 effectiveness context patterns
- **Real-world Validation**: Audio project serves as primary testing scenario
- **Context Preservation**: Maintain proven context-with-code effectiveness

### **Modern Python DevOps Configuration**

**Core pyproject.toml Structure**:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "chunking-framework"
version = "0.1.0"
description = "Automated chunking system for development workflows"
authors = [{name = "Development Team", email = "dev@example.com"}]
license = {text = "MIT"}
requires-python = ">=3.9"

# Lightweight runtime dependencies (~20MB total)
dependencies = [
    "pyyaml~=6.0",      # 500KB - Contract specifications
    "markdown~=3.5",    # 200KB - Document parsing
    "psutil~=5.9",      # 500KB - Performance monitoring
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "ruff>=0.1.0",      # Fast linting and formatting
    "black>=23.0",      # Code formatting
    "mypy>=1.0",        # Type checking
    "pre-commit>=3.0",  # Git hooks
]
test = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "pytest-mock>=3.10",
    "pytest-benchmark>=4.0",  # Performance measurement
]
integration = [
    "subprocess32;python_version<'3.2'",  # Claude Code script testing
]

[project.scripts]
chunking-framework = "chunking_framework.cli:main"

# Development workflow scripts
[tool.hatch.envs.default.scripts]
test = "pytest {args:tests}"
test-unit = "pytest tests/unit/ -m unit"
test-integration = "pytest tests/integration/ -m integration"
test-e2e = "pytest tests/e2e/ -m e2e --tb=short"
lint = "ruff check src tests"
format = "black src tests"
typecheck = "mypy src"
quality = ["lint", "typecheck", "test-unit"]
validate = ["quality", "test-integration", "test-e2e"]
```

**Testing Configuration for TDD Approach**:
```toml
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--cov=src/chunking_framework",
    "--cov-report=html",
    "--cov-report=term-missing:skip-covered",
    "--cov-fail-under=90",
]
markers = [
    "unit: Unit tests for deterministic components",
    "integration: Integration tests for cross-component functionality",
    "e2e: End-to-end workflow validation tests",
    "slow: Tests that take >1 second to run",
    "benchmark: Performance measurement tests",
]
filterwarnings = [
    "error",
    "ignore::UserWarning",
    "ignore::DeprecationWarning",
]
```

**Code Quality Standards**:
```toml
[tool.ruff]
line-length = 88
target-version = "py39"
select = [
    "E",   # pycodestyle errors
    "F",   # Pyflakes
    "W",   # pycodestyle warnings
    "I",   # isort
    "N",   # pep8-naming
    "B",   # flake8-bugbear
    "A",   # flake8-builtins
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG", # flake8-unused-arguments
    "PTH", # flake8-use-pathlib
]
ignore = [
    "E501",  # Line too long (handled by black)
]

[tool.ruff.per-file-ignores]
"tests/**/*.py" = [
    "ARG",     # Unused function arguments in tests
    "S101",    # Use of assert in tests
]

[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
(
  /(
      \.eggs
    | \.git
    | \.mypy_cache
    | \.pytest_cache
    | build
    | dist
  )/
)
'''

[tool.mypy]
python_version = "3.9"
strict = true
warn_return_any = true
warn_unused_configs = true
show_error_codes = true

[[tool.mypy.overrides]]
module = "tests.*"
strict = false  # Relax strictness for test files
```

**Pre-commit Configuration** (`.pre-commit-config.yaml`):
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-PyYAML, types-psutil]
```

### **Development Workflow Standards**

**Branch Strategy**: 
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Individual development features
- `phase/2a-core-automation` - Phase-specific development

**Commit Standards**:
- Conventional commits format: `type(scope): description`
- Examples: `feat(handoff): add AST-based interface extraction`, `test(e2e): add workflow validation tests`

**Quality Gates**:
- All tests must pass before merge
- Code coverage ≥90% for new code
- Type checking with mypy strict mode
- Linting with ruff (zero violations)
- Pre-commit hooks must pass

## System Architecture & Integration Model

### **Hybrid Claude Code Integration Strategy**

**Architectural Decision**: Framework operates as independent subfolder with selective context import while maintaining proven development patterns

**Integration Pattern**:
- **Claude Code**: Interactive development, decision-making, implementation authority
- **Framework Scripts**: Analysis, template generation, validation, context preparation
- **Selective Import**: Proven context patterns imported without domain-specific bloat
- **Independent Testing**: Framework validates against audio project as real-world scenario

**Workflow Example**:
```bash
# 1. Claude Code analyzes completed chunk in audio project
cd chunking-framework
./scripts/analyze-completion.py --project=../src/audio_to_json --stage=foundation

# 2. Framework generates handoff using imported proven patterns
./scripts/generate-handoff.py --from=foundation --to=audio --templates=context/reference/handoff-examples/

# 3. Claude Code reviews generated handoff in framework context
# Uses Read/Edit tools within chunking-framework/ directory

# 4. Apply validated handoff to audio project implementation
cd ..
# Continue with audio project development using framework-generated guidance
```

### **Context Management Strategy**

**Selective Import Principle**: Preserve proven effectiveness patterns while eliminating domain bloat

**Context Import Strategy**:
```bash
# Import proven organizational patterns
cp -r context/domains/standards.md chunking-framework/context/reference/
cp -r context/chunking/examples/HANDOFF-*.md chunking-framework/context/reference/handoff-examples/

# Exclude domain-specific content
# Skip: context/domains/data.md (audio-specific)
# Skip: context/stages/ (audio project stages)
# Skip: context/workflows/ (audio project workflows)
```

**Benefits**:
- **Proven Patterns**: Import 4.8/5 effectiveness context methodology
- **Clean Architecture**: Framework context focused on chunking automation
- **Reduced Complexity**: No audio/ML specific context in framework
- **Validation Path**: Audio project tests framework in real-world scenario

### **Development Strategy**

**Phase 2A (Immediate)**: Subfolder framework development
- Initialize independent git repository in `chunking-framework/` subfolder
- Import selective context patterns from proven experiments
- Develop framework with audio project as primary validation scenario
- Maintain separate dependencies, CI/CD, and development lifecycle

**Phase 2B+ (Post-validation)**: Cross-domain expansion
- Validate framework effectiveness with audio project implementation
- Test framework with additional validation scenarios (React, database, API)
- Refine based on real-world usage patterns and effectiveness metrics
- Consider extraction to standalone repository if cross-domain proven

**Future Integration Options**:
- **MCP Tools**: Convert successful scripts to Claude Code MCP tools
- **Template Library**: Generalize successful patterns for cross-domain use
- **Standalone Distribution**: Extract to independent repository post-validation  

## Experiment Results Foundation

### **Proven Success Metrics** (From Diarization Implementation)
- **Context Management**: 4.8/5 average across 6 sessions (3.2K tokens average, target flexibility proven)
- **Contract Accuracy**: 95% (only minor gaps requiring minimal adjustments)  
- **Handoff Quality**: 5/5 (zero integration failures between chunks)
- **Focus Maintenance**: 4.8/5 (minimal scope creep, excellent boundary discipline)
- **Integration Reliability**: 5/5 (zero rework required, seamless chunk transitions)
- **Development Velocity**: 120% of expected (4.2 hours vs 5-7 hour target)

### **Critical Success Factors Identified**
1. **High-Quality Handoff Documents** - Most important factor enabling zero integration failures
2. **Contract-First Development** - Upfront interface design prevents integration friction
3. **Context Focus** - 3-4K token contexts with relevant files prevent decision paralysis
4. **Sequential Dependencies** - Clear linear progression enables predictable implementation
5. **E2E Test Contracts** - Immutable test specifications provide clear success criteria
6. **Error Isolation** - Chunk boundaries contain failures and simplify debugging

## Implementation Architecture

### **Claude Code Integration Specifications**

**Tool Integration Strategy**: Automation augments Claude Code capabilities without replacing interactive development

**Critical Design Constraints**:
1. **Claude Code Authority**: All implementation decisions remain with Claude Code
2. **Automation Support**: Scripts provide analysis, templates, validation - not autonomous implementation
3. **Context Preservation**: Maintain proven 3-4K token context effectiveness patterns
4. **Sequential Orchestration**: Claude Code manages chunk progression with automation assistance

**Integration Points**:
- **Analysis Phase**: Automation extracts interfaces, dependencies, patterns from completed implementations
- **Generation Phase**: Create handoff templates, context packages, contract specifications
- **Validation Phase**: Verify contract compliance, interface accuracy, integration compatibility
- **Orchestration Phase**: Prepare next chunk context, track progress, manage dependencies

### **Phase 2A: Core Automation System (2-3 weeks) - TDD Implementation**

#### **Stage 1: Handoff Generation Engine** 
**Duration**: 5-6 days  
**Priority**: Critical (Proven most important factor)
**TDD Approach**: E2E tests define 90% quality benchmark before implementation

**E2E Test Definition (Week 1)**:
```python
# tests/e2e/test_stage1_handoff_generation_e2e.py
def test_handoff_generation_achieves_benchmark_quality():
    """E2E: Generate handoff matching HANDOFF-2.md quality standards"""
    # Test validates: structure compliance, interface completeness, context adequacy
    
def test_handoff_interface_accuracy_90_percent():
    """E2E: Validate 90%+ interface prediction accuracy vs actual implementation"""
    # Test measures: predicted interfaces vs AST-extracted actual interfaces
    
def test_context_package_3k_to_4k_tokens():
    """E2E: Context packages consistently within proven effective range"""
    # Test validates: token count, relevance scoring, minimal external loading required
```

**Scope & Boundaries**:
- **Input**: Completed chunk implementation (source files, tests, git changes)
- **Output**: Comprehensive HANDOFF-{N}.md document matching proven quality standards
- **Boundaries**: Does NOT modify code, only analyzes and documents interfaces
- **Validation**: Lightweight structure validation + AST-based interface accuracy

**Core Components**:

1. **Interface Analyzer** (Unit + Integration Tests)
   - Extract classes, functions, data models using Python AST parsing
   - Identify input/output contracts and method signatures  
   - Detect integration points and dependencies through import analysis
   - Generate usage examples from actual implementation patterns

2. **Contract Specification Generator** (Unit + Integration Tests)
   - Auto-generate INTERFACE-CONTRACT.yaml from AST analysis
   - Map dependencies between chunks based on interface usage
   - Validate contract completeness against implementation via AST comparison
   - Predict requirements for dependent chunks using dependency analysis

3. **Context Preparation System** (Integration + E2E Tests)
   - Identify files required by dependent chunks through dependency graphs
   - Extract relevant code patterns and integration examples
   - Package focused context (3-4K tokens validated through tokenization)
   - Generate troubleshooting and debugging guidance

4. **Handoff Document Composer** (E2E Tests)
   - Template engine using proven HANDOFF-{0-5} structure validation
   - Automated generation of required sections with completeness checking
   - Quality validation against HANDOFF-2.md benchmark through structure comparison
   - Consistency checking for interface specifications via template matching

**TDD Success Criteria** (Measured by automated tests):
- **Structure Validation**: 95% template compliance vs HANDOFF-2.md format
- **Interface Accuracy**: 90% precision/recall vs AST-extracted actual interfaces  
- **Context Effectiveness**: 3-4K token packages with 4.5+ sufficiency simulation
- **Integration Readiness**: Generated handoffs enable zero-friction dependent chunk implementation

**Implementation Requirements**:
- Python AST parsing for deterministic interface extraction
- Git diff analysis for change identification  
- Template matching system based on proven handoff structures
- File dependency analysis through import graph construction

**Claude Code Integration** (Integration Tests):
- **Script Execution**: `./chunking-framework/scripts/generate-handoff.py --stage=completed --target=next`
- **Template Customization**: Claude Code reviews automated handoffs using Read/Edit tools
- **Quality Validation**: Automated comparison against HANDOFF-2.md benchmark
- **Context Packaging**: Automated preparation validated through token counting and relevance scoring

---

#### **Stage 2: Context Isolation Engine**
**Duration**: 4-5 days  
**Priority**: High (Context focus proven critical)
**TDD Approach**: E2E tests validate 4.5+ context sufficiency before implementation

**E2E Test Definition (Week 1)**:
```python
# tests/e2e/test_stage2_context_isolation_e2e.py  
def test_context_package_achieves_sufficiency_rating():
    """E2E: Context packages achieve 4.5+ sufficiency rating through simulation"""
    # Test simulates: chunk implementation with generated context, measures external loading
    
def test_context_token_count_optimization():
    """E2E: Context consistently 3-4K tokens with maximum relevance"""
    # Test validates: token counting accuracy, relevance scoring effectiveness
```

**Scope & Boundaries**:
- **Input**: Chunk specification, dependency handoffs, codebase structure
- **Output**: Focused context packages (3-4K tokens) for chunk implementation  
- **Boundaries**: Read-only codebase analysis, no code modification
- **Validation**: Token counting + relevance scoring + sufficiency simulation

**Core Components**:

1. **Smart File Selection**
   - Analyze interface dependencies to identify required files
   - Pattern recognition for relevant code examples and integration points
   - Exclude irrelevant files based on chunk scope
   - Prioritize context based on implementation patterns from experiment

2. **Context Relevance Scoring**
   - Weight files by relevance to chunk implementation scope
   - Filter out noise while preserving essential integration context
   - Balance between comprehensive and focused (3-4K token target)
   - Learn from successful context patterns in experiment

3. **Context Package Generation**
   - Structured context loading with clear file organization
   - Include integration examples and patterns from relevant files
   - Generate context summary with key focus areas  
   - Validate context completeness for chunk implementation

4. **Pattern Recognition System**
   - Learn from successful context patterns (HANDOFF examples)
   - Identify code patterns relevant to specific chunk types
   - Recognize integration points and dependency patterns
   - Extract architectural patterns for context inclusion

**Success Criteria**:
- Generate context packages that achieve 4.5+ sufficiency rating
- Context size consistently 3-4K tokens (proven effective range)
- Minimal external context loading required during implementation
- Context enables focused implementation without decision paralysis

**Claude Code Integration**:
- **Context Generation**: `./chunking-framework/scripts/prepare-context.py --chunk=target --dependencies=handoffs`
- **Relevance Scoring**: Automated file selection based on interface dependencies and proven patterns
- **Package Validation**: Claude Code reviews context completeness before chunk implementation
- **Progressive Loading**: Context packages integrate with existing /context/ system navigation

---

#### **Stage 3: Contract Validation Framework**
**Duration**: 4-5 days  
**Priority**: High (95% accuracy needs systematic validation)
**TDD Approach**: E2E tests validate 95% contract accuracy baseline before implementation

**E2E Test Definition (Week 1)**:
```python
# tests/e2e/test_stage3_contract_validation_e2e.py
def test_contract_validation_achieves_95_percent_accuracy():
    """E2E: Contract predictions achieve 95% accuracy vs actual implementations"""
    # Test measures: predicted contracts vs AST-extracted actual interfaces
    
def test_integration_compatibility_validation():
    """E2E: Validate integration compatibility between chunk handoffs"""
    # Test validates: handoff contracts work together without conflicts
```

**Scope & Boundaries**:
- **Input**: Interface contracts, chunk implementation, integration points
- **Output**: Validation reports and compliance verification
- **Boundaries**: Validates existing implementations, suggests fixes but doesn't modify
- **Validation**: AST-based contract comparison + integration compatibility testing

**Core Components**:

1. **Interface Compliance Checker**
   - Verify implementations match interface specifications exactly
   - Validate data types, method signatures, error handling patterns
   - Check integration points work as specified in contracts
   - Detect contract violations early in implementation

2. **Integration Validation System**
   - Test handoff compatibility between chunks automatically
   - Validate dependency resolution and interface satisfaction
   - Check error handling and graceful degradation patterns
   - Ensure backward compatibility where specified

3. **Success Criteria Automation**
   - Extract success criteria from E2E tests automatically
   - Generate validation checklists for chunk completion
   - Validate performance requirements and error handling
   - Check unit test coverage and integration requirements

4. **Contract Accuracy Tracking**
   - Measure actual vs predicted interface usage
   - Track contract modifications required during implementation
   - Learn from validation failures to improve contract prediction
   - Generate feedback for handoff generation improvement

**Success Criteria**:
- Achieve 95%+ contract accuracy (matching experiment results)
- Detect integration issues before chunk handoffs
- Validate implementations meet specifications without manual checking
- Provide clear guidance for contract violation resolution

**Claude Code Integration**:
- **Validation Execution**: `./chunking-framework/scripts/validate-contracts.py --implementation=current --contracts=handoffs`
- **Compliance Reporting**: Automated generation of validation reports for Claude Code review
- **Error Guidance**: Specific recommendations for resolving contract violations
- **Integration Testing**: Automated verification of handoff compatibility between chunks

---

#### **Stage 4: Sequential Orchestration System**
**Duration**: 3-4 days  
**Priority**: Medium (Sequential flow proven, needs automation)
**TDD Approach**: E2E tests validate sequential workflow automation before implementation

**E2E Test Definition (Week 1)**:
```python
# tests/e2e/test_stage4_orchestration_e2e.py
def test_sequential_workflow_automation():
    """E2E: Generate correct chunk sequence and session preparation automatically"""
    # Test validates: dependency ordering, session context preparation, progress tracking
    
def test_resumable_implementation_workflow():
    """E2E: Enable resumable implementation across multiple sessions"""
    # Test validates: progress state management, context restoration, dependency validation
```

**Scope & Boundaries**:
- **Input**: Module specification, E2E tests, chunk dependencies
- **Output**: Ordered chunk sequence, session preparation, progress tracking
- **Boundaries**: Orchestrates existing systems, doesn't implement chunks directly
- **Validation**: Dependency graph validation + progress state testing

**Core Components**:

1. **Dependency Graph Generator**
   - Analyze E2E tests to identify natural chunk boundaries
   - Build dependency graphs showing chunk relationships
   - Validate sequential dependencies and ordering constraints
   - Detect potential parallel execution opportunities (for Phase 3)

2. **Chunk Sequencing Engine**
   - Generate optimal sequential implementation order
   - Prepare session contexts and requirements for each chunk
   - Handle dependency resolution and prerequisite checking
   - Enable resumable implementation with progress tracking

3. **Session Preparation System**
   - Automated context loading for each chunk session
   - Preparation of required files, handoffs, and specifications
   - Generate session objectives and success criteria
   - Provide estimated time and complexity for each chunk

4. **Progress Tracking Framework**
   - Monitor chunk completion status and success criteria
   - Track integration validation between chunks
   - Generate progress reports and remaining work estimates
   - Handle error recovery and chunk dependency updates

**Success Criteria**:
- Generate correct sequential ordering matching manual experiment success
- Prepare complete session contexts requiring minimal setup time
- Track progress accurately with clear completion criteria
- Enable resumable implementation across multiple sessions

**Claude Code Integration**:
- **Orchestration Management**: `./chunking-framework/scripts/orchestrate-chunks.py --module=target --progress=.chunking/state.yaml`
- **Session Preparation**: Automated setup of context, handoffs, and objectives for each chunk
- **Progress Tracking**: Real-time updates to `.chunking/current-chunk.yaml` for resumable implementation
- **Dependency Resolution**: Automated validation of prerequisite completion before chunk progression

---

#### **Stage 5: E2E Integration System**
**Duration**: 3-4 days  
**Priority**: Medium (E2E tests proven effective for boundaries)
**TDD Approach**: E2E tests validate complete system integration before implementation

**E2E Test Definition (Week 1)**:
```python
# tests/e2e/test_stage5_integration_e2e.py
def test_complete_chunking_workflow_integration():
    """E2E: All automation stages work together for complete chunking workflow"""
    # Test validates: handoff generation → context isolation → contract validation → orchestration
    
def test_chunk_boundary_detection_accuracy():
    """E2E: Detect optimal chunk boundaries from E2E tests automatically"""  
    # Test validates: boundary detection vs proven 4-6 chunk effectiveness patterns
```

**Scope & Boundaries**:
- **Input**: E2E test specifications, module requirements
- **Output**: Chunk boundary analysis, success criteria extraction
- **Boundaries**: Analyzes existing tests, suggests boundaries but doesn't modify tests
- **Validation**: End-to-end workflow testing + boundary optimization validation

**Core Components**:

1. **Chunk Boundary Detection**
   - Analyze E2E tests to identify natural implementation boundaries
   - Map test scenarios to logical chunk divisions
   - Detect integration points and interface requirements from tests
   - Validate chunk boundaries against testing patterns

2. **Success Criteria Extraction**
   - Parse E2E tests to extract success criteria for each chunk
   - Generate validation checklists from test specifications
   - Map test requirements to implementation requirements
   - Create validation frameworks for chunk completion

3. **Test-Driven Contract Generation**
   - Generate interface contracts based on E2E test requirements
   - Extract data models and integration patterns from tests
   - Predict implementation interfaces from test scenarios
   - Validate contracts against test compatibility

4. **Module Analysis Engine**
   - Break down complex modules into manageable chunks (4-6 proven optimal)
   - Estimate implementation complexity and time requirements  
   - Identify technical dependencies and integration challenges
   - Generate module-level implementation roadmaps

**Success Criteria**:
- Detect chunk boundaries that enable 4.8+ focus maintenance
- Generate success criteria matching E2E test immutability principles
- Create contracts that achieve 95%+ accuracy in dependency prediction
- Enable module breakdown matching proven 4-6 chunk effectiveness

**Complete E2E Workflow Test (Week 1)**:
```python
# tests/e2e/test_full_workflow_e2e.py
def test_complete_automated_chunking_workflow():
    """E2E: Complete automation workflow achieves experiment-level effectiveness"""
    # Test validates: 120% development velocity, 95% contract accuracy, 4.8+ focus maintenance
    
def test_cross_chunk_integration_reliability():
    """E2E: Zero integration failures between automated chunk handoffs"""
    # Test validates: handoff compatibility, dependency satisfaction, error isolation
```

### **Phase 2B: Domain Validation Testing (2-3 weeks) - TDD Expansion**

#### **Validation Scenario 1: Greenfield React Application**
**Duration**: 3-4 days  
**Objective**: Test chunking automation on frontend component development

**Test Scope**:
- Component library development with complex state management
- API integration layers and data handling
- UI/UX implementation with design system constraints
- Testing framework integration and validation

**Success Metrics**:
- Maintain 90%+ contract accuracy across UI/API boundaries
- Achieve 4+ effectiveness rating for context management
- Generate quality handoffs for component integration
- Validate automation works for non-ML development domains

#### **Validation Scenario 2: Database Schema Migration**  
**Duration**: 3-4 days
**Objective**: Test chunking on data-intensive backend development

**Test Scope**:
- Complex schema changes with data migration requirements
- API endpoint modifications for new data structures
- Database performance optimization and indexing
- Data validation and integrity constraint implementation

**Success Metrics**:
- Maintain development velocity improvements vs traditional approach
- Validate contract accuracy for database interface changes
- Test error isolation effectiveness for data migration failures
- Confirm handoff quality for database-dependent chunks

#### **Validation Scenario 3: API Service Refactoring**
**Duration**: 3-4 days  
**Objective**: Test chunking on large-scale service decomposition

**Test Scope**:
- Microservice extraction from monolithic application  
- Inter-service communication protocol design
- Authentication and authorization boundary management
- Service deployment and configuration management

**Success Metrics**:
- Validate chunking effectiveness for service architecture changes
- Test dependency management across service boundaries  
- Confirm integration reliability for distributed system development
- Measure automation effectiveness for complex refactoring tasks

#### **Validation Scenario 4: Testing Infrastructure**
**Duration**: 2-3 days
**Objective**: Test chunking on testing and DevOps automation

**Test Scope**:
- Test automation framework development
- CI/CD pipeline configuration and optimization
- Monitoring and observability system integration
- Performance testing and load validation systems

**Success Metrics**:
- Validate automation effectiveness for infrastructure-as-code
- Test chunk boundary detection for DevOps workflow development  
- Confirm handoff quality for testing framework integration
- Measure development velocity for infrastructure automation

### **Phase 2C: System Refinement (1-2 weeks)**

#### **Cross-Domain Pattern Analysis**
**Duration**: 3-4 days
- Analyze patterns that work across all validation domains
- Identify domain-specific adaptations required for automation
- Refine handoff generation based on cross-domain learnings
- Update context isolation patterns for different development types

#### **Automation Optimization**  
**Duration**: 3-4 days
- Optimize systems based on validation feedback
- Implement domain-specific intelligence where proven necessary
- Refine contract prediction accuracy based on cross-domain results
- Update sequential orchestration for different development patterns

## Risk Management

### **Phase 2A Risks (Core Automation)**

**High Risk**:
- **Handoff Generation Quality**: Auto-generated handoffs don't match manual quality
  - **Mitigation**: Use proven HANDOFF examples as validation benchmarks, extensive testing against manual standards, automated quality scoring via pytest

**Medium Risk**:
- **Context Isolation Accuracy**: Automated context selection misses critical information
  - **Mitigation**: Conservative approach including more context initially, learn from successful patterns, comprehensive integration testing

- **Contract Prediction Complexity**: Interface prediction fails for complex integration scenarios
  - **Mitigation**: Start with simpler contract patterns, iterative improvement based on validation failures, AST-based validation

**DevOps Risk**:
- **Development Environment Complexity**: Multi-stage testing requirements create setup friction
  - **Mitigation**: Modern pyproject.toml configuration, automated environment setup scripts, pre-commit hooks for quality assurance

### **Phase 2B Risks (Domain Validation)**

**High Risk**:
- **Domain Transfer Failure**: Automation doesn't work outside ML integration context
  - **Mitigation**: Start with simpler scenarios, document domain-specific patterns systematically

**Medium Risk**:
- **Scalability Issues**: Automation breaks down with larger, more complex modules
  - **Mitigation**: Test with progressively larger modules, identify scalability limits early

### **Fallback Strategies**

**If Automation Quality < Manual Standards**:
- Hybrid approach: automated generation + human refinement
- Focus on highest-value automation (handoff generation) first
- Iterative improvement rather than complete automation

**If Domain Validation Fails**:
- Limit automation to proven domain (ML/data processing)
- Build domain-specific intelligence incrementally
- Maintain manual chunking as fallback for complex scenarios

### **Architecture Evolution Path**

**Repository Boundaries Decision Timeline**:
- **Immediate (Phase 2A)**: Develop integrated with current repository structure
- **Post-Validation (Phase 2B)**: Evaluate extraction to dedicated framework repository
- **Post-Refinement (Phase 2C)**: Implement chosen architecture with proven patterns

**System Boundary Considerations**:
- **Context Storage**: Active automation state in repository, framework logic potentially extractable
- **Claude Code Integration**: Hybrid model preserves interactive development effectiveness
- **Framework Portability**: Design enables future extraction without losing proven context patterns
- **MCP Conversion**: Successful automation scripts can evolve to MCP tools for enhanced integration

## Success Criteria

### **Phase 2A Success (Core Automation)**
- **Handoff Generation**: Match 90%+ quality of manual HANDOFF-2.md benchmark
- **Context Isolation**: Achieve 4.5+ sufficiency rating consistently
- **Contract Validation**: Maintain 95%+ accuracy from experiment baseline  
- **Sequential Orchestration**: Generate correct dependency ordering without manual intervention
- **System Integration**: All components work together seamlessly for complete automation

### **Phase 2B Success (Domain Validation)**
- **Cross-Domain Effectiveness**: Maintain 4+ rating across all chunking dimensions in each validation scenario
- **Development Velocity**: Achieve measurable improvement vs traditional development in 3/4 scenarios
- **Contract Accuracy**: Maintain 90%+ accuracy across different development domains
- **Automation Reliability**: System works without manual intervention in 75%+ of scenarios

### **Overall Project Success**
- **Automation Effectiveness**: Deliver chunking results matching manual experiment quality
- **Domain Coverage**: Validate effectiveness across 4 different development scenarios  
- **System Robustness**: Handle errors gracefully and provide clear guidance for resolution
- **Developer Experience**: Reduce cognitive load and context switching vs traditional development
- **Scalability Foundation**: System architecture ready for advanced features (parallel execution, etc.)

## Implementation Timeline - TDD Integrated

### **Week 1: E2E Test Definition & Setup (TDD Red Phase)**
- **Day 1**: Repository setup + Modern Python project initialization (pyproject.toml, dev environment)
- **Day 2**: Define all E2E tests for Stages 1-5 + complete workflow + test infrastructure setup
- **Day 3**: Set up validation frameworks, benchmarking system, quality assurance tools
- **Day 4**: Claude Code integration points, script orchestration testing
- **Day 5**: Complete TDD Red phase validation - all E2E tests fail appropriately
- **Deliverable**: Fully configured development environment with comprehensive failing test suite

### **Week 2: Core Handoff & Context Systems (TDD Green Phase)**  
- **Day 1-3**: Stage 1 Handoff Generation Engine - implement to pass E2E tests
- **Day 4-5**: Stage 2 Context Isolation Engine - implement to pass E2E tests
- **Focus**: Achieve 90% handoff quality, 4.5+ context sufficiency through lightweight validation

### **Week 3: Validation & Orchestration (TDD Green Phase)**
- **Day 1-3**: Stage 3 Contract Validation Framework - implement to pass E2E tests  
- **Day 4-5**: Stage 4 Sequential Orchestration System - implement to pass E2E tests
- **Focus**: Achieve 95% contract accuracy, reliable workflow automation

### **Week 4: Integration & Testing (TDD Refactor Phase)**
- **Day 1-2**: Stage 5 E2E Integration System - complete workflow integration
- **Day 3-4**: System optimization based on E2E test feedback and performance analysis
- **Day 5**: Complete workflow validation - all E2E tests passing consistently

### **Week 5-7: Domain Validation**
- Validation Scenario 1: Greenfield React (3-4 days)
- Validation Scenario 2: Database Migration (3-4 days)  
- Validation Scenario 3: API Refactoring (3-4 days)
- Validation Scenario 4: Testing Infrastructure (2-3 days)

### **Week 8: System Refinement**
- Cross-domain pattern analysis (3-4 days)
- Automation optimization (3-4 days)

## Next Actions

### **Development Environment Setup** (Immediate)

**Phase 1: Subfolder Repository Creation & Setup** (Day 1)
1. **Create Framework Subfolder with Independent Git**:
   ```bash
   # From pronunciation-clips root directory
   mkdir chunking-framework
   cd chunking-framework
   git init
   git checkout -b develop
   
   # Add to main project .gitignore
   cd ..
   echo "chunking-framework/" >> .gitignore
   ```

2. **Framework Project Structure Initialization**:
   ```bash
   cd chunking-framework
   
   # Create framework-specific structure
   mkdir -p src/chunking_framework/{analysis,generation,validation,orchestration}
   mkdir -p context/{reference,development}
   mkdir -p {templates,scripts,tests/{unit,integration,e2e}}
   
   # Initialize framework-specific CLAUDE.md
   touch CLAUDE.md
   
   # Initialize pyproject.toml with lightweight dependencies
   # (See Modern Python DevOps Configuration above)
   ```

3. **Selective Context Import**:
   ```bash
   # Import proven patterns (from pronunciation-clips root)
   mkdir -p context/reference/handoff-examples
   cp ../context/chunking/examples/HANDOFF-*.md context/reference/handoff-examples/
   cp ../context/domains/standards.md context/reference/
   
   # Create framework-specific context structure
   mkdir -p context/development/{architecture,validation,integration}
   
   # Initialize templates from imported examples
   cp context/reference/handoff-examples/HANDOFF-2.md templates/handoff_templates/base-template.md
   ```

4. **Modern Python Environment Setup**:
   ```bash
   # Set up independent development environment
   python -m venv venv
   source venv/bin/activate  # or venv/Scripts/activate on Windows
   pip install -e ".[dev,test]"
   
   # Install pre-commit hooks for framework
   pre-commit install
   ```

5. **Quality Assurance Validation**:
   ```bash
   # Validate framework environment (should pass with empty codebase)
   pytest tests/
   ruff check src/
   black --check src/
   mypy src/
   
   # Initial git commit for framework
   git add .
   git commit -m "feat: initial framework structure with selective context import"
   ```

6. **CI/CD Pipeline** (Optional for Phase 2A, recommended for Phase 2B):
   ```yaml
   # .github/workflows/ci.yml
   name: CI
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       strategy:
         matrix:
           python-version: ["3.9", "3.10", "3.11"]
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v4
           with:
             python-version: ${{ matrix.python-version }}
         - run: pip install -e ".[dev,test]"
         - run: pytest
         - run: ruff check
         - run: black --check .
         - run: mypy src/
   ```

**Development Workflow Validation**:
```bash
# Complete development setup validation
cd chunking-framework

# Run all quality checks
hatch run quality    # lint + typecheck + unit tests
hatch run validate   # quality + integration + e2e tests

# Test development scripts
hatch run test-unit
hatch run test-integration  
hatch run test-e2e

# Validate Claude Code integration points
./scripts/generate-handoff.py --help
./scripts/prepare-context.py --help
./scripts/validate-contracts.py --help
./scripts/orchestrate-chunks.py --help

# Test integration with parent audio project
cd ..
# Validate framework can analyze audio project structure
./chunking-framework/scripts/analyze-completion.py --project=src/audio_to_json --stage=foundation
```

### **Immediate Next Actions (TDD Implementation Start)**

**Week 1 Focus: E2E Test Definition First**
1. **Day 1**: Subfolder repository setup + Context import + E2E test structure
   ```bash
   # Subfolder initialization with selective context import
   # (see Development Environment Setup above)
   cd chunking-framework
   
   # Create E2E test structure
   hatch run test-e2e  # All tests should fail initially (TDD Red phase)
   ```

2. **Day 2**: Define validation benchmarks using HANDOFF-2.md as quality standard
   ```bash
   # Set up benchmark validation infrastructure
   pytest tests/e2e/test_stage1_handoff_generation_e2e.py -v --tb=short
   # Expected: All tests fail with clear baseline measurements
   ```

3. **Day 3**: Set up lightweight validation infrastructure (AST parsing, template matching)
   ```bash
   # Validate development environment supports all testing technologies
   python -c "import ast, yaml, markdown, psutil; print('All dependencies available')"
   hatch run quality  # Should pass with empty implementation
   ```

4. **Day 4**: Test Claude Code integration points with placeholder automation
   ```bash
   # Test script orchestration from Claude Code
   ./scripts/generate-handoff.py --stage=placeholder --target=test
   ./scripts/prepare-context.py --chunk=test --dependencies=none
   ```

5. **Day 5**: Validate all E2E tests fail appropriately - establish measurement baselines
   ```bash
   # Complete TDD Red phase validation
   hatch run test-e2e --tb=no  # Clean failure output
   # Document baseline metrics for Green phase implementation
   ```

**Key Success Criteria for Week 1**:
- All E2E tests exist and fail predictably with clear error messages
- Validation infrastructure measures what matters (structure, interfaces, tokens, effectiveness)
- Claude Code integration points tested with minimal dependencies
- Modern development environment configured with quality assurance automation
- Benchmarking system ready for quality comparison against proven examples
- Development workflow validated: `hatch run validate` executes complete test suite

**DevOps Foundation Established**:
- Framework as independent git subfolder with selective context import
- Lightweight dependency management (~20MB total) isolated from ML dependencies (~500MB+)
- Multi-layer testing strategy (unit/integration/e2e) with pytest configuration
- Code quality automation (ruff, black, mypy) with independent pre-commit hooks
- Proven context patterns imported (4.8/5 effectiveness) without domain bloat
- Audio project serves as primary real-world validation scenario
- Independent CI/CD pipeline for framework development lifecycle

This implementation plan preserves proven experiment success (4.8/5 context effectiveness, 95% contract accuracy) while enabling clean framework development through architectural separation and selective pattern import.