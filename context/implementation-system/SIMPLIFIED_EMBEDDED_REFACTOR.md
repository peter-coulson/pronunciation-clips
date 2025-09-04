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
- `standards-session` - Session-scoped standards gathering

### Modified Agents
- All main agents now include embedded context gathering with validation

## New Workflow

**Session Setup**: Standards-session agent creates `sessions/{session-name}/1-standards/standards-session.md` combining context domains + repository patterns.

**Stage 1: Architecture Design**  
- Input: User requirements + standards-session.md
- Process: Requirements scan → context extraction + validation → architecture design
- Output: Architecture specification

**Stage 2: Interface Design**
- Input: Architecture specification + standards-session.md  
- Process: Requirements scan → context extraction + validation → interface design
- Output: Interface specification

**Stage 3: Behavior Specification**
- Input: Interface specification + standards-session.md
- Process: Requirements scan → context extraction + validation → behavior specification  
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

2. Context Extraction + Validation  
   - Scan codebase for specific requirements
   - Focus on architectural patterns only
   - Validate requirements coverage
   - Flag missing context explicitly

3. Architecture Design
   - Use extracted context + standards
   - Generate architecture specification
```

## Standards Implementation

**Session-Scoped**: Standards-session agent combines `/context/domains/` + repository scan into single `standards-session.md`
**Single Source**: All agents reference same session standards file - no duplication or conflicts
**DRY Compliant**: No duplicate context structures, leverages existing domain organization

## Quality Assurance

**Self-Validation**: Each agent validates its own context extraction against requirements
**Clear Failures**: Missing context is explicitly flagged, not silently ignored  
**Independent Testing**: Each agent can be tested in isolation with known inputs

## Universal Templates

**Requirements Scan Template**
```markdown
# {Agent Name} Requirements Scan

## Context Requirements Identified
### Level-Specific Needs
- **{requirement_type}**: {description}

### Cross-Cutting Concerns  
- **{concern_type}**: {description}

## Priority Assessment
### Critical Requirements
### Nice-to-Have Requirements
```

**Context Extraction + Validation Template**
```markdown
# {Agent Name} Context Extraction

## Files Read Into Context
- **{file_path}**: {size/lines} - {relevance_reason}

## Files Analyzed  
- **{file_path}**: {relevance_reason}

## Patterns Identified
- **{pattern_type}**: {description}

## Constraints Found
- **{constraint_type}**: {impact}

## Gap Validation
### Requirements Coverage
- ✅ **{requirement}**: Found in {source}
- ❌ **{requirement}**: Missing - {impact}

### Validation Status
- **Ready to Proceed**: {yes/no}
- **Blocking Issues**: {list}
```

This approach eliminates coordination complexity while preserving all quality and progressive discovery benefits.