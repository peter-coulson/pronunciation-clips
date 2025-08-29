# MVP Implementation Plan

## Architecture: Human-Coordinated Subagent Pipeline

**Execution Model**: You orchestrate stages, Claude subagents execute sub-processes using methodology documentation.

## Phases

### Phase 1: Session Infrastructure (1 day)
- Session directory initialization 
- Basic validation helpers

### Phase 2: Core Subagents (3-4 days)
- 9 methodology-based subagents (one per sub-process)
- Individual testing with real inputs
- Prompt refinement

### Phase 3: End-to-End Flow (1-2 days)
- Complete pipeline test on Spanish learning requirement
- Handoff validation
- Integration debugging

## Execution Prompts

### Phase 1 Prompt
```
Create minimal session management for the 4-stage implementation system.

Essential Context:
- Read: README.md (understand session directory structure)
- Read: sessions/example-session/ structure 

Task: Build utilities to:
1. Initialize session directories with proper structure
2. Basic template validation (required sections present)
3. Session state tracking

Focus: Minimal infrastructure - subagents read templates from source locations and write outputs to session directories.
```

### Phase 2 Prompt
```
Implement focused subagent for [SUBAGENT_NAME] following its methodology.

Essential Context:
- Read: [STAGE]/[SUBAGENT]/methodology.md (execution logic)
- Read: [STAGE]/[SUBAGENT]/templates/ (input/output templates)
- Read: ABSTRACTION_FRAMEWORK.md (risk-knowledge mapping framework)
- Read: sessions/example-session/ (understand file locations)

Task: Create subagent that:
1. Reads methodology and applies it step-by-step
2. Takes specified input templates from session
3. Outputs completed templates to session directory
4. Returns clear success/failure status

Focus: Single-purpose agent executing one methodology with template I/O.
```

### Phase 3 Prompt
```
Test complete 4-stage pipeline using Spanish learning project requirement.

Essential Context:
- Read: README.md (understand complete flow)
- Read: all coordination.md files (stage handoff logic)
- Read: proof-of-concept/ (operational learnings)
- Access: actual Spanish learning codebase for real-world testing

Task: Execute end-to-end flow:
1. Create real USER_REQUIREMENTS_TEMPLATE.md for Spanish learning feature
2. Run all 9 subagents in sequence with human validation
3. Validate each handoff works correctly
4. Debug integration issues and template gaps
5. Document operational lessons learned

Focus: Prove system works on real requirements → working code output.
```