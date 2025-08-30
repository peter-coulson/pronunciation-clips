# Claude Code Subagent MVP Guide

## MVP Strategy: Start Simple, Specialize Later

### Phase 1: Use Built-in `general-purpose` for ALL Sub-Processes
**Why**: Zero setup, full tool access, collect real performance data before optimizing.

**Implementation**: Use `subagent_type: "general-purpose"` in all Task tool calls initially.

### Phase 2: Evidence-Based Custom Subagents (After 5-10 Successful Runs)
**Only specialize where you observe consistent issues:**
- Role confusion or scope drift
- Tool usage inefficiencies
- Context pollution problems

## Essential Subagent Basics

### What Subagents Are
- **Same Claude model** with isolated context window
- **Specialized via system prompts** and optional tool restrictions
- **Stateless execution** - report back and terminate
- **No further subagent spawning** capability

### File Structure (MVP)
**Location**: `.claude/agents/` (project-level)

**Format**:
```yaml
---
name: subagent-name
description: When this subagent should be invoked
---
System prompt content goes here
```

## Thinking Allowances Configuration

**Available thinking budgets:**
- `"think"` - 4,000 tokens (standard analysis)
- `"think hard"` - Enhanced thinking (complex decisions)
- `"think harder"` - Maximum thinking (critical analysis)
- `"ultrathink"` - ~32,000 tokens (extremely complex tasks)

**Usage in prompts**:
```
Think hard about architectural decisions before proceeding.
Use ultrathink for complex dependency analysis.
```

## MVP Instruction Guidelines

### Include (Minimal Essential)
- **Role definition**: "You are a [expertise] specialist"
- **Primary objective**: Single clear goal
- **Success criteria**: How to measure completion
- **Methodology reference**: `@methodology.md` pointer
- **Thinking guidance**: Which thinking level to use

### Exclude (For Later Phases)
- Detailed step-by-step processes
- Tool usage instructions  
- Implementation examples
- Excessive context

### Methodology Integration (MVP)
```
Read and follow @methodology.md for detailed process guidance.
Think hard about [specific complexity area].
```

## Deliberately Excluded from MVP

### Future Expansion Areas (Do NOT Implement Now)
- **Custom MCP tools** - External tool development
- **Model selection** - haiku/sonnet/opus per subagent  
- **Complex tool restrictions** - Granular permissions
- **User-level subagents** - Cross-project configurations
- **Advanced delegation logic** - Smart routing systems
- **Performance optimization** - Context size tuning

### Scope Boundary
**MVP Focus**: Basic custom subagents that reference existing methodology files with appropriate thinking budgets.

**Expansion Risk**: Avoid feature creep - stick to simple system prompts + methodology references.

## Template and Reference

**Template**: `SUBAGENT_TEMPLATE.md`  
**Documentation**: https://docs.anthropic.com/en/docs/claude-code/sub-agents  
**Management**: `/agents` command