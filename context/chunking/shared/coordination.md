# Main Agent Coordination Patterns

## Coordination Responsibilities

### Phase Orchestration
- **Phase Transition Management**: Validates completion of current phase before initiating next phase
- **Handoff Validation**: Ensures standardized formats are maintained between phases  
- **Context Preservation**: Maintains overall project context across phase boundaries
- **Progress Tracking**: Monitors overall system progress and completion status

### Delegation Patterns
- **Specialist Assignment**: Routes work to appropriate phase-specific agents
- **Interface Enforcement**: Ensures agents adhere to standardized communication formats
- **Quality Gates**: Validates outputs before approving phase transitions
- **Error Handling**: Manages failures and coordinates recovery procedures

## Coordination Principles

### Stateless Design
- Each phase operates independently with document-based handoffs
- No persistent state maintained between agent invocations
- All context passed through standardized formats

### Clean Separation
- Main agent focuses on orchestration, not implementation details
- Specialist agents handle phase-specific complexity
- Clear boundaries prevent responsibility overlap