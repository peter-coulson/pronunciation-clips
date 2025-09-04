# Simplified Embedded Refactor: Self-Contained Progressive Agents

## Fundamental Principles Preserved

- **Progressive Discovery**: Don't know what context is needed until previous level completes
- **Quality Control**: Validate requirements against actual extraction to prevent assumptions
- **Standards Consistency**: Leverage proven patterns instead of inferring from incomplete examples
- **Stage Independence**: Clean handoffs with no orchestration complexity

## Core Problem Solved

**Current**: Separate knowledge-requirements and knowledge-extraction agents create coordination complexity and front-load all context discovery.

**Solution**: Embed context gathering directly into main agents with validation steps.

## Key Benefits

- ✅ **Eliminates orchestration complexity** - No separate knowledge agents to coordinate
- ✅ **Perfect context targeting** - Each agent gets exactly what it needs when it needs it  
- ✅ **Maintains quality control** - Built-in requirement validation prevents missing context
- ✅ **Self-contained agents** - Each agent is independently testable and debuggable
- ✅ **Standards efficiency** - Agents scan for "how to apply patterns" not "what are patterns"

## Refactor Changes

### Removed Agents
- `knowledge-requirements` - Embedded in main agents
- `knowledge-extraction` - Embedded in main agents

### New Agents  
- `architecture-design` - Split from combined architecture-interface agent
- `interface-design` - Split from combined architecture-interface agent

### Modified Agents
- All main agents now include embedded context gathering with validation

## New Workflow

**Stage 1: Architecture Design**  
- Input: User requirements
- Process: Context requirements identification → context loading → architecture design
- Output: Architecture specification

**Stage 2: Interface Design**
- Input: Architecture specification
- Process: Context requirements identification → context loading → interface design
- Output: Interface specification

**Stage 3: Behavior Specification**
- Input: Interface specification
- Process: Context requirements identification → context loading → behavior specification  
- Output: Behavior specification + test contracts

**Stage 4: Implementation Preparation** (unchanged)
- Input: Behavior specifications
- Output: Coordination plan + implementation segments

**Stage 5: Code Generation** (unchanged)  
- Input: Coordination plan
- Output: Generated code

## Agent Structure (Example: Architecture Design)

```
1. Context Requirements Identification
   - Based on user requirements
   - "What architectural context do I need?"
   - Identify specific files/patterns needed

2. Context Loading 
   - Read identified context files (/context/domains/, existing code)
   - Load relevant repository patterns
   - Validate coverage of requirements

3. Architecture Design
   - Use loaded context
   - Generate architecture specification
```

## Context Loading Strategy

**Direct Access**: Agents read `/context/domains/` files directly when needed
**No Duplication**: No session standards files - use source context directly
**On-Demand**: Load only the specific context needed for each agent's task

## Quality Assurance

**Self-Validation**: Each agent validates its own context loading against requirements
**Clear Failures**: Missing context is explicitly flagged, not silently ignored  
**Independent Testing**: Each agent can be tested in isolation with known inputs

## Universal Templates

**Context Requirements Template**
```markdown
# {Agent Name} Context Requirements

## Required Context
### Domain Files Needed
- **{domain_file}**: {reason}

### Repository Files Needed
- **{file_path}**: {reason}

## Context Loading Plan
### Priority 1 (Critical)
- {files_needed}

### Priority 2 (Nice-to-Have)  
- {files_needed}
```

**Context Loading Validation Template**
```markdown
# {Agent Name} Context Loading

## Context Loaded
- **{file_path}**: {size/lines} - {relevance_reason}

## Patterns Identified
- **{pattern_type}**: {description}

## Requirements Coverage
- ✅ **{requirement}**: Found in {source}
- ❌ **{requirement}**: Missing - {impact}

## Ready to Proceed
- **Status**: {yes/no}
- **Blocking Issues**: {list}
```

This approach eliminates coordination complexity while preserving all quality and progressive discovery benefits.

## New Repository Structure

### Proposed Agents Folder Structure
```
context/implementation-system/
├── agents/
│   ├── 01-architecture-design/
│   │   ├── methodology.md
│   │   └── templates/
│   ├── 02-interface-design/
│   │   ├── methodology.md  
│   │   └── templates/
│   ├── 03-behavior-specification/
│   │   ├── methodology.md
│   │   └── templates/
│   ├── 04-implementation-segmentation/
│   │   ├── methodology.md
│   │   └── templates/
│   ├── 05-execution-orchestration/
│   │   ├── methodology.md
│   │   └── templates/
│   ├── 06-test-implementation/
│   │   ├── methodology.md
│   │   └── templates/
│   └── 07-segmented-implementation/
│       ├── methodology.md
│       └── templates/
├── sessions/ (unchanged)
└── proof-of-concept/ (unchanged)
```

### Structure Benefits

- **Flat Organization**: Eliminates stage hierarchy complexity since agents are now self-contained
- **Clear Sequencing**: Numbered agents (01, 02, etc.) show execution order without folder nesting
- **Independent Agents**: Each agent folder is complete and self-contained with methodology and templates
- **Easy Reordering**: Simple to add, remove, or resequence agents without restructuring
- **Terminology Alignment**: "Agents" terminology matches the self-contained nature (no more "subagents")

### Migration Strategy

1. **Phase 1**: Create new `agents/` folder structure alongside existing structure
2. **Phase 2**: Migrate each agent individually as refactor is implemented
3. **Phase 3**: Remove old stage-based folders once migration is complete
4. **Phase 4**: Update all documentation and tooling to reference new structure

This structure directly supports the embedded context gathering approach while providing a cleaner, more intuitive organization model.