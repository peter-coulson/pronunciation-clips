# Knowledge Extraction Methodology

## Single-Phase Approach
**Input**: Knowledge Requirements + Knowledge Repository  
**Output**: Filled KNOWLEDGE_PACKAGE_TEMPLATE.md template  
**Sub-Process Role**: Specialized research sub-process focused purely on information gathering

## Access Permissions
**READ**: 
- ABSTRACTION_FRAMEWORK.md
- TERMINOLOGY.md  
- Own methodology (knowledge-extraction/methodology.md)
- Completed input templates (knowledge-requirements.md)
- **Main context system** (entire project knowledge repository)

**WRITE**:
- Own output templates (knowledge-extraction.md)

## Extraction Process

### Primary Task
Extract all available information from knowledge repository to populate template sections organized by:
- Specification levels (Requirements through Implementation)  
- Knowledge categories (Constraint, Integration, Pattern, Convention)

### Research Workflow
- Search knowledge repository using semantic understanding
- Fill template sections with concrete information found
- Document information sources used
- Identify contradictory information discovered
- Generate structured list of missing information in summary section

### Sub-Process Responsibilities
- **Pure research**: Find and document available information
- **Gap identification**: List what could not be located
- **Source tracking**: Document where information was found
- **No assessment**: Avoid making criticality or importance judgments

### Output Structure
- **Filled template**: All available knowledge organized by framework
- **Missing summary**: Structured list of gaps for downstream assessment
- **Metadata**: Sources and contradictions for transparency

## Downstream Usage
- **Planning stages**: Consume filled template as project knowledge
- **Validation stages**: Assess missing items against requirements for criticality
- **Human operators**: Scan missing summary to improve knowledge repository