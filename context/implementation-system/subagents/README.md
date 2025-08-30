# Subagents Directory

Claude Code subagent definitions for the 4-stage implementation system. Each subagent specializes in specific sub-processes within the sequential processing pipeline.

## Purpose

Subagents enable isolated, focused execution of implementation sub-processes while maintaining the system's core design principles:
- **Perfect Independence** - Each subagent operates with zero dependencies
- **Methodology Adherence** - References existing methodology files for process guidance
- **Stateless Execution** - Document-based handoffs with predictable file locations

## File Structure

**Standard Format**:
```yaml
---
name: subagent-name
description: When this subagent should be invoked
settings:
  permissions:
    deny: ["Edit(**)", "Write(**)"]  # Block all editing by default
    allow: ["Edit(./specific/path/**)", "Write(./specific/path/**)"]
---
System prompt defining role, objectives, and methodology references
```

## Deployment

Deploy subagents to `.claude/agents/` for use with Claude Code's Task tool:
```bash
cp subagents/*.md .claude/agents/
```

Invoke via Task tool:
```
subagent_type: "subagent-name"
```

## Thinking Allocation Strategy

### "think hard" - Critical Architecture Points
- **architecture-interface-design** - System decomposition cascades through pipeline
- **behavior-specification-design** - Creates immutable test contracts

### "think" - Framework Application Points  
- **knowledge-requirements** - Complex risk-knowledge mapping
- **implementation-segmentation** - Dependency optimization
- **scope-definition** - Multi-level knowledge filtering

### Default - Execution-Focused
- **knowledge-extraction** - Research patterns
- **execution-orchestration** - Template synthesis
- **test-implementation** - Specification → code generation
- **segmented-implementation** - TDD execution

## Permission Strategy

**Default Security**: Block all file modifications (`deny: ["Edit(**)", "Write(**)"]`)

**Selective Access**: Enable specific paths based on sub-process needs:
- Template creation: Allow template directories only
- Test generation: Allow test directories only  
- Implementation: Block critical system files only

## Current Subagents

| Subagent | Stage | Purpose |
|----------|--------|---------|
| knowledge-requirements | 1 | Generate knowledge requirements using risk-prevention framework |
| knowledge-extraction | 1 | Research and extract project knowledge from repositories |
| architecture-interface-design | 2 | Design system architecture and component interfaces |
| behavior-specification-design | 2 | Create behavior specifications and test contracts |
| implementation-segmentation | 3 | Break implementation into manageable execution units |
| scope-definition | 3 | Filter knowledge packages for implementation scope |
| execution-orchestration | 3 | Create coordination plans for implementation execution |
| test-implementation | 4 | Generate tests from behavior specifications |
| segmented-implementation | 4 | Execute test-driven implementation of code segments |

## Methodology Integration

All subagents reference their corresponding methodology files:
```
Read and follow context/implementation-system/[stage]/[sub-process]/methodology.md
```

Output follows standard handoff protocols to:
```
context/implementation-system/sessions/$SESSION_NAME/[stage]/[output-file]
```