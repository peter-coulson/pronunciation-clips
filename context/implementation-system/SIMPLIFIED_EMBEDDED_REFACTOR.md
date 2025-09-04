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

### Eliminated Agents
- `knowledge-requirements` - Embedded in main agents
- `knowledge-extraction` - Embedded in main agents

### New Agents  
- `architecture-design` - Split from combined architecture-interface agent
- `interface-design` - Split from combined architecture-interface agent

### Modified Agents
- All main agents now include embedded context gathering with validation

### One-Time Setup
- **Standards detection** creates `~/.claude/standards/` with lightweight pattern files

## New Workflow

**One-time Setup**: Standards detection scans project and creates `~/.claude/standards/` with lightweight pattern files.

**Stage 1: Architecture Design**  
- Input: User requirements + standards
- Process: Requirements scan → context extraction → gap validation → architecture design
- Output: Architecture specification

**Stage 2: Interface Design**
- Input: Architecture specification + standards  
- Process: Requirements scan → context extraction → gap validation → interface design
- Output: Interface specification

**Stage 3: Behavior Specification**
- Input: Interface specification + standards
- Process: Requirements scan → context extraction → gap validation → behavior specification  
- Output: Behavior specification + test contracts

**Stage 4: Implementation Preparation** (unchanged)
- Input: Behavior specifications
- Output: Coordination plan + implementation segments

**Stage 5: Code Generation** (unchanged)  
- Input: Coordination plan
- Output: Generated code

## Agent Structure (Example: Architecture Design)

```
1. Requirements Scan
   - Based on user requirements + standards
   - "What architectural context do I need?"

2. Targeted Extraction  
   - Scan codebase for specific requirements
   - Focus on architectural patterns only

3. Gap Validation
   - "Did I find everything I needed?"
   - Flag missing context explicitly

4. Architecture Design
   - Use extracted context + standards
   - Generate architecture specification
```

## Standards Implementation

**Detection**: Simple project scan creates lightweight standards files
**Loading**: Each agent receives relevant standards as reference context
**Structure**: Minimal - naming conventions, test patterns, error handling per stack

## Quality Assurance

**Self-Validation**: Each agent validates its own context extraction against requirements
**Clear Failures**: Missing context is explicitly flagged, not silently ignored  
**Independent Testing**: Each agent can be tested in isolation with known inputs

This approach eliminates coordination complexity while preserving all quality and progressive discovery benefits.