# Context Extraction Methodology

## Single-Phase Approach
**Input**: Knowledge Requirements + Context System  
**Output**: Filled CONTEXT_EXTRACTION_OUTPUT.md template  
**Agent Role**: Specialized research agent focused purely on information gathering

## Extraction Process

### Primary Task
Extract all available information from context system to populate template sections organized by:
- Specification levels (Requirements through Implementation)  
- Knowledge categories (Constraint, Integration, Pattern, Convention)

### Research Workflow
- Search context system using semantic understanding
- Fill template sections with concrete information found
- Document information sources used
- Identify contradictory information discovered
- Generate structured list of missing information in summary section

### Agent Responsibilities
- **Pure research**: Find and document available information
- **Gap identification**: List what could not be located
- **Source tracking**: Document where information was found
- **No assessment**: Avoid making criticality or importance judgments

### Output Structure
- **Filled template**: All available context organized by framework
- **Missing summary**: Structured list of gaps for downstream assessment
- **Metadata**: Sources and contradictions for transparency

## Downstream Usage
- **Planning agents**: Consume filled template as project context
- **Validation agents**: Assess missing items against requirements for criticality
- **Human operators**: Scan missing summary to improve context system