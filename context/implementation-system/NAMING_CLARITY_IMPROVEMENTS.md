# Naming Clarity Improvements - Context Overload Resolution

## Problem Analysis
The term "context" is overloaded across 5 different conceptual domains, creating significant clarity issues:

1. **External Knowledge Source** - "context system", "context extraction"
2. **Processed Information Packages** - "context requirements", "context templates" 
3. **Execution Environment** - "testing context", "implementation context"
4. **Processing Scope** - "context independence", "project contexts"
5. **Meta-Process Information** - File context, warnings, etc.

## Proposed Solution
Create clear conceptual separation using three distinct terms:
- **Knowledge** - Information and data
- **Scope** - Boundaries and filtering  
- **Context** - Execution environment only

## Specific Changes

### Folder Renames
- [ ] `context-aggregation/` → `knowledge-extraction/`
- [ ] `context-requirement-mapping/` → `knowledge-requirements/`
- [ ] `context-scoping/` → `scope-definition/`

### File Renames
- [ ] `CONTEXT_EXTRACTION_TEMPLATE.md` → `KNOWLEDGE_PACKAGE_TEMPLATE.md`

### Conceptual Term Changes (Future File Content Updates)
| Old Term | New Term | Rationale |
|----------|----------|-----------|
| "context system" | "knowledge repository" | More precise - it's a repository of project knowledge |
| "context extraction" | "knowledge extraction" | Extracting information, not execution environment |
| "context templates" | "knowledge packages" | Structured containers of organized knowledge |
| "context independence" | "knowledge independence" | About when knowledge becomes universally applicable |
| "context filtering" | "scope filtering" | About defining boundaries, not environment |

### Keep "Context" For (No Changes)
- ✓ "testing context" - Refers to test execution environment
- ✓ "implementation context" - Refers to runtime environment  
- ✓ "system context" - Refers to overall execution environment

## Implementation Checklist

### Phase 1: File and Folder Renames (Current)
- [ ] Rename folder: `1-requirement-analysis/context-aggregation/` → `knowledge-extraction/`
- [ ] Rename folder: `1-requirement-analysis/context-requirement-mapping/` → `knowledge-requirements/`  
- [ ] Rename folder: `3-implementation-preparation/context-scoping/` → `scope-definition/`
- [ ] Rename file: `knowledge-extraction/templates/CONTEXT_EXTRACTION_TEMPLATE.md` → `KNOWLEDGE_PACKAGE_TEMPLATE.md`

### Phase 2: File Content Updates (Future)
- [ ] Update all references to old folder names in methodology files
- [ ] Update template references in coordination files
- [ ] Update terminology in README files
- [ ] Update @ABSTRACTION_FRAMEWORK.md terminology
- [ ] Update CLAUDE.md references
- [ ] Update coordination.md files in each stage

## Expected Benefits
1. **Conceptual Clarity** - Each term has single, clear meaning
2. **Reduced Cognitive Load** - No mental disambiguation required
3. **Better Documentation** - Self-documenting folder/file names
4. **Easier Onboarding** - New contributors understand structure immediately
5. **Maintainability** - Changes become more predictable and traceable

## Migration Notes
- All existing functionality preserved
- Only naming changes, no logic modifications
- File content updates can be done incrementally
- Backwards compatibility maintained during transition