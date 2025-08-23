# Agent-Based Chunking System

A simple, prompt-based chunking system that leverages Claude's proven architectural decision-making capabilities while providing structure and coordination for complex implementation projects. The system uses a Control Agent to analyze specifications and coordinate Sub-Agents that implement individual chunks, enabling parallel execution where dependencies allow.

## Core Goals

1. **Preserve Claude's Judgment** - Control Agent makes all chunking decisions using proven patterns
2. **Enable Parallel Execution** - Sub-Agents implement independent chunks simultaneously 
3. **Maintain Integration Quality** - Interface specification-based handoffs ensure seamless chunk integration
4. **Repository Agnostic** - Works with any codebase without complex setup
5. **Leverage Proven Patterns** - Built on 5/5 effectiveness experiment results (4.8/5 context management, 95% interface specification accuracy, 120% velocity)

## System Architecture

### Repository Structure
```
repository/
├── .claude/agents/                 # Claude Code agent definitions
│   ├── chunking-control.md         # Control agent (coordinates chunking)
│   │   # Imports: @context/chunking/methodology/*, @context/chunking/instructions/control-agent.md
│   └── chunking-sub.md             # Sub-agent (implements chunks)
│       # Imports: @context/chunking/instructions/sub-agents.md, @context/chunking/standards.md
├── context/                        # Repository context system (ENHANCED)
│   ├── domains/                    # Domain-specific knowledge
│   ├── standards/                  # Development standards
│   ├── patterns/                   # Proven implementation patterns
│   ├── workflows/                  # Development processes
│   └── chunking/                   # Chunking subdomain (distributed for maintainability)
│       ├── methodology/            # Core workflow rules (referenceable by agents)
│       │   ├── workflow.md         # Core phase sequence and steps only
│       │   ├── architecture.md     # Agent specialization, scale limits, coordination model
│       │   ├── testing.md          # E2E immutability, contract fulfillment, test execution rules
│       │   ├── templates.md        # Template standards, format specifications, quality criteria
│       │   ├── coordination.md     # Main agent orchestration, document handoffs, progress tracking
│       │   ├── boundaries.md       # Chunking decision patterns from experiments
│       │   ├── validation.md       # Quality gates, success criteria, validation procedures
│       │   └── success-factors.md  # Critical elements, proven patterns, risk mitigation
│       ├── instructions/           # Agent behaviors and coordination
│       │   ├── planning-agents/    # Input validation, E2E setup, analysis agents
│       │   ├── implementation-agents/ # Sequential chunk implementation
│       │   └── coordination/       # Main agent orchestration patterns
│       ├── templates/              # Standardized formats (extensible)
│       │   ├── input-spec.md       # Input specification template
│       │   ├── handoff.md          # Chunk handoff template
│       │   ├── summary.md          # Session completion template
│       │   └── [additional templates as needed]
│       ├── standards.md            # Input format validation criteria
│       ├── sessions/               # Active/completed sessions
│       │   └── YYYY-MM-DD-feature-name/
│       │       # NOTE: Structure TBD after methodology complete
│       │       └── [structure-to-be-designed]
│       └── experiments/            # Proven results (existing)
└── src/                           # Implementation code
```

### Content Division Principles

**Single Responsibility**: Each methodology file covers exactly one domain to eliminate duplication:
- **validation.md** = Quality gates and success criteria (WHEN things are correct)
- **templates.md** = Format specifications only (HOW communication is structured)  
- **testing.md** = Test execution rules only (HOW tests run, not when they pass)
- **coordination.md** = Agent orchestration (HOW agents interact)
- **architecture.md** = Agent capabilities (WHO does what, including scale constraints)

**Key Overlaps Resolved**:
- Scale limits: architecture.md owns agent constraints, boundaries.md owns chunking decision patterns
- Validation: validation.md owns quality gates, templates.md owns format standards
- Agent behavior: architecture.md defines roles, coordination.md defines interactions

## Control Agent Commands
```
- "Start chunking session with specification: [spec-file.md]"
- "Resume chunking development"
- "Archive completed session and update main context"
```

## Reference Documents
- `/context/chunking/experiment/CHUNKING_LEARNINGS_LOG.md` - Proven effectiveness patterns
- `/context/chunking/examples/HANDOFF-*.md` - Quality handoff examples
- `/context/domains/standards.md` - Development standards
- `diarization_implementation.md` - Reference specification format