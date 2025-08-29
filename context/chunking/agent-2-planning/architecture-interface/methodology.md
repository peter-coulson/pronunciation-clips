# Architecture-Interface Sub-Agent Methodology

## Sequential Execution Process

### Task Management
1. Use TodoWrite to create sequential tasks:
   - "Complete Level 2 Architecture Specification"
   - "Complete Level 3 Interface Specification"
2. Execute tasks sequentially - complete Level 2 before starting Level 3

### Level 2: Architecture Phase
**Cognitive Focus**: "What components does this system need and how do they relate?"

**Process**:
1. Mark Level 2 task as in_progress
2. Read requirements and context extraction completely
3. Think architecturally about system decomposition
4. Apply context knowledge for architectural decisions
5. Complete Level 2 template fully
6. Mark Level 2 task completed

**Context Application**: Apply Constraint and Integration knowledge from @ABSTRACTION_FRAMEWORK.md to prevent System-Breaking and Integration-Breaking risks. Proactively integrate context knowledge during specification development and document integration in Context Integration Notes sections.

### Level 3: Interface Phase  
**Cognitive Focus**: "What are the clean boundaries for these architectural components?"

**Process**:
1. Mark Level 3 task as in_progress
2. Use completed Level 2 architecture as foundation
3. Define interfaces that emerge naturally from architectural components
4. Apply context knowledge for interface design
5. Complete Level 3 template fully
6. Mark Level 3 task completed

**Context Application**: Apply Integration and Convention knowledge from @ABSTRACTION_FRAMEWORK.md to ensure proper boundaries and consistency. Follow the 4-step knowledge application strategy: 1) Identify applicable knowledge categories, 2) Apply knowledge proactively, 3) Document integration in Context Integration Notes, 4) Validate coverage against risk prevention.

## Success Criteria
- Level 2: Architecture makes logical sense and components are well-defined
- Level 3: Interfaces are directly implementable from Level 2 architecture
- Both levels: Context knowledge properly integrated throughout