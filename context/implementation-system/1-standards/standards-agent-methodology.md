# Standards-Session Agent Methodology

## Purpose
Create session-scoped standards document by combining domain standards with repository patterns into `sessions/{session}/1-standards/standards-session.md`.

## Process

### 1. Context Discovery (Authoritative)
- Read all files in `/context/domains/`
- Extract principles, patterns, and constraints per domain
- Document conflicts between domain standards

### 2. Infrastructure Discovery (Structural)
- Scan root-level configs (package.json, pyproject.toml, etc.)
- Extract build/test commands from scripts
- Identify framework/tooling choices

### 3. Src Discovery (Validation/Gap-Filling)
- Sample key source files for actual implementation patterns
- Validate context standards against reality
- Fill gaps where context documentation is silent
- Focus on error handling, logging, imports, test utilities

### 4. Conflict Resolution
- Context standards take precedence over discovered patterns
- Explicit resolution of conflicts between context and implementation
- Document any unresolvable conflicts for session awareness

### 5. Template Population
Fill `STANDARDS_SESSION_TEMPLATE.md`:
- **Session Scope**: From user requirements
- **Domain Standards**: Map domain principles to implementation guidance
- **Repository Patterns**: Concrete patterns discovered in codebase
- **Quality Gates**: Test requirements and validation approaches
- **Context Sources**: File references and conflict resolutions

### 6. Validation Criteria
- ✅ All domain files analyzed and principles extracted
- ✅ Technology stack and dependencies identified
- ✅ Error handling and logging patterns found
- ✅ Test utilities and conventions documented
- ✅ Conflicts between standards explicitly resolved
- ✅ Template fully populated (no placeholders)

### 7. Output Location
Save as `sessions/{session}/1-standards/standards-session.md`

## Template Structure Reference
```
- Session Scope Definition (scope, exclusions, success)
- Domain Standards Applied (principles + application guidance)
- Repository Patterns Discovered (tech stack, organization, infrastructure)
- Quality Gates (validation approach)
- Context Sources (files analyzed, conflicts resolved)
```

## Agent Intelligence Assumptions
- Can identify relevant patterns from partial examples
- Can resolve conflicts between competing standards
- Can translate abstract principles into concrete guidance
- Can distinguish critical patterns from noise