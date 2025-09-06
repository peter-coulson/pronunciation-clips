# Simplified Embedded Refactor: Single Agent System

## Stage 1 Approach: Single Process Implementation

**First Stage Strategy**: We will implement a single process with no shared templates or subprocesses to test the core agent approach. This allows us to validate the single agent methodology before abstracting shared templates and processes.

**Implementation Plan**:
- Create one complete process implementation as a proof of concept
- Embed all templates and subprocesses directly within the single process
- Test the agent's ability to execute the full methodology end-to-end
- Once validated, abstract shared components to the planned shared structure

**Stage 1 Benefits**:
- Rapid prototyping and validation of the core concept
- No premature abstraction until patterns are proven
- Complete testing of the agent execution model
- Foundation for later refactoring to shared components

## Executive Summary

**Current Problem**: Multiple specialized agents create coordination complexity and duplicate core execution patterns.

**Solution**: Single universal agent with dynamic methodology loading for specialization without duplication.

**Core Benefits**:
- ✅ **Eliminates agent orchestration** - One agent handles all processes
- ✅ **DRY principle compliance** - Shared execution patterns, specialized instructions
- ✅ **Perfect context targeting** - Sequential subprocess execution with cumulative context
- ✅ **Simplified architecture** - Methodology files replace separate agent definitions

## System Architecture

### Single Agent + Dynamic Methodologies
- **One Agent**: Universal execution patterns in system prompt
- **Dynamic Specialization**: Process-specific instructions loaded from methodology files
- **Sequential Execution**: Subprocess-by-subprocess with validation gates
- **Context Building**: Each subprocess builds upon previous context

## Key Principles Preserved

- **Progressive Discovery**: Context needs emerge as previous levels complete
- **Quality Control**: Requirements validated against actual extraction to prevent assumptions
- **Standards Consistency**: Proven patterns leveraged instead of inferring from incomplete examples
- **Stage Independence**: Clean handoffs maintained with no orchestration complexity

## Process Workflow

### Single Agent Process Execution

The universal agent sequentially executes processes, loading methodology files as needed:

**Process 01: Architecture Design**  
- Methodology: `01-architecture-design/methodology.md`
- Input: User requirements → Output: Architecture specification

**Process 02: Interface Design**
- Methodology: `02-interface-design/methodology.md`
- Input: Architecture specification → Output: Interface specification

**Process 03: Behavior Specification**
- Methodology: `03-behavior-specification/methodology.md`
- Input: Interface specification → Output: Behavior specification + test contracts

**Process 04: Implementation Segmentation**
- Methodology: `04-implementation-segmentation/methodology.md`
- Input: Behavior specifications → Output: Implementation segments

**Process 05: Execution Orchestration**
- Methodology: `05-execution-orchestration/methodology.md`
- Input: Implementation segments → Output: Coordination plan

**Process 06: Test Implementation**
- Methodology: `06-test-implementation/methodology.md`
- Input: Behavior specifications + coordination plan → Output: Test code

**Process 07: Segmented Implementation**
- Methodology: `07-segmented-implementation/methodology.md`
- Input: Coordination plan → Output: Generated code

### System Prompt vs Methodology Separation

**System Prompt Contains**:
- Core execution patterns (todo management, validation gates)
- General behavioral instructions (thoroughness, error handling)
- Meta-instructions for loading and following methodology files

**Methodology Files Contain**:
- Process-specific steps and domain knowledge
- Context requirements and loading instructions
- Subprocess validation criteria

## Universal Agent Execution Pattern

### Process Execution Flow

```
1. Todo List Generation
   - Agent reads methodology.md for current process
   - Creates subprocess todo list via TodoWrite
   - Tracks validation gates and handoff requirements

2. Sequential Subprocess Execution
   - Load subprocess context as specified in methodology
   - Execute subprocess steps with validation
   - Build upon previous subprocess outputs
   - Complete validation gates before proceeding

3. Process Completion
   - Verify all validation criteria met
   - Generate required handoff artifacts
   - Proceed to next process or complete
```

### Context Strategy

- **Cumulative Context**: Each process builds upon previous context
- **Methodology-Driven Loading**: Context requirements specified in methodology files
- **Validation Gates**: Context completeness verified at each process boundary

## Repository Structure

### New Folder Structure
```
context/implementation-system/
├── processes/
│   ├── 01-architecture-design/
│   │   ├── methodology.md
│   │   ├── templates/
│   │   └── subprocesses/
│   ├── 02-interface-design/
│   │   ├── methodology.md  
│   │   ├── templates/
│   │   └── subprocesses/
│   ├── 03-behavior-specification/
│   │   ├── methodology.md
│   │   ├── templates/
│   │   └── subprocesses/
│   ├── 04-implementation-segmentation/
│   │   ├── methodology.md
│   │   ├── templates/
│   │   └── subprocesses/
│   ├── 05-execution-orchestration/
│   │   ├── methodology.md
│   │   ├── templates/
│   │   └── subprocesses/
│   ├── 06-test-implementation/
│   │   ├── methodology.md
│   │   ├── templates/
│   │   └── subprocesses/
│   └── 07-segmented-implementation/
│       ├── methodology.md
│       ├── templates/
│       └── subprocesses/
├── shared/
│   ├── subprocesses/
│   │   ├── context-loading.md        # Universal context loading patterns
│   │   ├── validation-gates.md       # Subprocess validation criteria  
│   │   └── template-completion.md    # Template filling workflows
│   └── templates/
│       ├── handoff-report.md         # Standard handoff documentation
│       └── validation-checklist.md   # Subprocess completion criteria
├── sessions/ (unchanged)
└── proof-of-concept/ (unchanged)
```

### Migration Strategy

1. **Phase 1**: Create new `processes/` folder structure alongside existing structure
2. **Phase 2**: Convert agent definitions to methodology files 
3. **Phase 3**: Create universal agent with system prompt execution patterns
4. **Phase 4**: Remove old stage-based folders and agent definitions
5. **Phase 5**: Update all tooling to reference single agent + methodology system

### Key Benefits

- **Eliminates agent coordination complexity** - Single agent execution path
- **Maintains specialization** - Process-specific methodology files  
- **Enables DRY compliance** - Shared execution patterns and subprocess workflows
- **Simplifies maintenance** - Update methodology files without touching agent definitions
- **Preserves quality control** - Validation gates and progressive context building