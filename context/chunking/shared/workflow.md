# System Workflow

## Execution Phase Workflow

*Starting from completed chunk specifications:*

1. **Specification Validation**
   - Receive standardized chunk specifications
   - Validate format and completeness
   - Confirm dependency ordering

2. **Sequential Implementation**
   - Execute chunks in dependency order
   - Provide complete context package for each chunk:
     * HANDOFF document from previous chunk (workflow + interfaces)
     * CONTEXT document for current chunk (focused requirements)
     * Targeted existing source files (integration points, patterns)
     * Related configuration and test files
   - Handle integration points

3. **Result Integration**
   - Combine chunk outputs
   - Validate complete implementation
   - Generate completion summary

4. **Quality Verification**
   - Run validation checks
   - Confirm specification fulfillment
   - Document completion status