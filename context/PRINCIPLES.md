# Context System Principles

## Maintenance Discipline
- Update contexts **immediately** after stage completion
- Update **before** starting new development phases
- Remove contexts that are no longer relevant

## Loading Strategy
- **Research tasks**: Load relevant domain contexts
- **Implementation**: Load standards + testing + stage contexts  
- **Debugging**: Load debugging contexts
- **Architecture decisions**: Load architecture + reference contexts

## Portable Structure
- **domains/**: Core knowledge domains (architecture, standards, testing, data, deployment)
- **workflows/**: Task-oriented contexts (current-task, debugging, performance)
- **stages/**: Development stage contexts (stage1-foundation, stage2-audio, etc.)
- **reference/**: Quick lookup contexts (apis, configs)

Reusable across projects - structure stays constant, content adapts.