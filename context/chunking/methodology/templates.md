# Template Format Specifications

## Template Types

The system uses **7 template types** for document-based coordination:

### **Core Communication Templates**

#### **1. Input Specification Template**
**Output File**: `input-specification.md`
**Format Sections**:
```markdown
# [Project Name] Implementation Specification

## Requirements
[Detailed requirement specifications]

## E2E Test Definitions  
[Test scenarios and success criteria]

## Technical Constraints
[Dependencies and limitations]

## Success Criteria
[Acceptance conditions]
```

#### **2. Context Package Template**
**Output Files**: `chunks/chunk-[N]-[name]/CONTEXT.md`
**Format Sections**:
```markdown
# Chunk [N]: [Name] - Implementation Context

## Chunk Scope
[Specific implementation boundaries]

## Required Interfaces
[Dependencies from previous chunks]

## Output Interface Specifications
[What this chunk must provide]

## Implementation Requirements
[Technical specifications and patterns]

## Integration Context
[Codebase integration guidance]
```

#### **3. Handoff Document Template**
**Output Files**: `HANDOFF-[N].md`
**Format Sections**:
```markdown
# HANDOFF-[N]: [From Chunk] to [To Chunk] Handoff

## Implementation Summary
[What was completed with key classes/functions]

## Public API Interface
[Primary entry points for integration]

## Error Handling Patterns
[Established error recovery and fallback strategies]

## Data Models & Interface Specifications
[Complete interface specifications with examples]

## Integration Requirements
[Specific implementation patterns for dependent chunks]

## Configuration Patterns
[Settings and environment variable integration]

## Testing Requirements
[Expected test coverage and validation approaches]

## Performance Characteristics
[Benchmarks and quality metrics achieved]

## Critical Integration Points
[Specific methods and workflows for next chunks]
```

#### **4. Summary Report Template**
**Output File**: `SESSION-SUMMARY.md`
**Format Sections**:
```markdown
# Session Summary: [Project Name]

## Implementation Results
[What was completed and validated]

## Context System Updates
[Required updates to main context]

## Success Metrics
[Performance and quality data]

## System State
[Final state and handoff information]
```

### **Planning & Coordination Templates**

#### **5. Scale Validation Template**
**Output File**: `SCALE-VALIDATION.md`
**Format Sections**:
```markdown
# Scale Validation: [Project Name]

## Chunk Count Estimation
[Estimated number of chunks]

## Scale Appropriateness Assessment
[Analysis of chunking suitability]

## User Decision Documentation
[Edge case decisions and rationale]

## Complexity Analysis
[Chunking rationale and boundaries]
```

#### **6. Dependency Chart Template**
**Output File**: `DEPENDENCY-CHART.md`
**Format Sections**:
```markdown
# Dependency Chart: [Project Name]

## Execution Order
[Sequential chunk execution sequence]

## Dependency Relationships
[Inter-chunk dependencies]

## Critical Path
[Essential dependency chain]

## Timing Estimates
[Expected execution duration]
```

#### **7. Coordination Plan Template**
**Output File**: `COORDINATION-PLAN.md`
**Format Sections**:
```markdown
# Coordination Plan: [Project Name]

## Execution Phases
[Phase-by-phase implementation steps]

## Agent Coordination
[How agents interact and handoff]

## Progress Checkpoints
[Validation points and milestones]

## Error Recovery
[Failure handling procedures]
```


## Template Naming Conventions

- **Sequential numbering**: HANDOFF-0.md, HANDOFF-1.md, etc.
- **Chunk identification**: chunk-[N]-[descriptive-name]/
- **Consistent extensions**: .md for documents
- **Descriptive filenames**: Use clear, descriptive names for all outputs