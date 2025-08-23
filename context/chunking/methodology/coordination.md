# Main Agent Coordination Architecture

## **Document-Based Coordination Model**
The system uses document-based coordination instead of programmatic dependency management:
- **Stateless Agent Design**: Each agent receives complete context via documents, no runtime state sharing
- **File System Handoffs**: All inter-agent communication through prepared documents and handoff files
- **No Runtime Coordination**: All dependency relationships resolved through upfront planning by Analysis Agent
- **Context Window Boundaries**: Child agents operate within 3-4K token contexts from prepared documents

**Why Document Coordination**: Aligns with Claude Code's Task tool constraints while ensuring reproducible, debuggable agent interactions

## **Main Agent Responsibilities** (to be fleshed out)
- **Process Orchestration**: Sequences all specialized agents based on dependency chart
- **Report Interpretation**: Analyzes sub-agent outputs for success/failure states and next actions
- **Final Validation**: Ensures all tests pass before completion, implements corrections as needed
- **Error Recovery**: Determines restart vs escalation procedures (protocols to be defined)

## **Progress Tracking Protocols**
- **Main Progress**: Chunking progress captured in CLAUDE.md
- **Minor Progress Tracking**: Still needs to be defined
- **State Management**: Tracks completion status of each agent across all phases