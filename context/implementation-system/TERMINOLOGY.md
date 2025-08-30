# System Terminology

## Process Structure

### **Stage**
One of 4 main processing units in sequential order:
1. **Requirements Analysis** (`1-requirement-analysis/`)
2. **Specification Design** (`2-specification-design/`) 
3. **Implementation Preparation** (`3-implementation-preparation/`)
4. **Code Generation** (`4-code-generation/`)

### **Phase** 
Major subdivisions within a stage (e.g., Knowledge Requirements Generation, Knowledge Extraction within Requirements Analysis stage)

### **Sub-Process**
Individual processing units that execute specific methodologies within phases/stages

### **Coordination**
Management of execution sequence and handoffs between stages, phases, and sub-processes

### **Session**
Single execution instance of the complete 4-stage system for one implementation request

### **Session Name**
Filesystem-safe directory identifier for session (kebab-case, no spaces/special chars)

### **Feature Name**
Human-readable display name for the implementation request (can contain spaces and special characters)

## Information Management

### **Knowledge Repository**
External storage of project information (e.g., Claude's project context folders, documentation systems)
*Source: ABSTRACTION_FRAMEWORK.md*

### **Knowledge** 
Information and data extracted from knowledge repositories
*Source: ABSTRACTION_FRAMEWORK.md*

### **Knowledge Package**
Organized collections of knowledge filtered and structured for specific implementation purposes

### **Knowledge Categories**
Universal categories for risk prevention
*Source: ABSTRACTION_FRAMEWORK.md, Universal Knowledge Categories section*

### **Scope**
Boundaries and filtering of information for specific purposes
*Source: ABSTRACTION_FRAMEWORK.md*

### **Context**
Execution environment only (e.g., testing context, runtime context)
*Source: ABSTRACTION_FRAMEWORK.md*

## Specification Framework

### **Specification Levels**
7-level progression from business intent to executable code: Requirements → Architecture → Interface → Behavior → Strategy → Signature → Implementation
*Source: ABSTRACTION_FRAMEWORK.md, Specification Levels section*

### **Universal Risk Types**
Risk patterns that knowledge categories prevent: System-Breaking, Integration-Breaking, Maintenance-Breaking, Quality-Breaking
*Source: ABSTRACTION_FRAMEWORK.md, Universal Risk Types section*

## Operations

### **Template**
Standardized file formats for inputs/outputs using naming convention: `{ROLE}_{TYPE}_TEMPLATE.md`

### **Handoff**
Transfer of completed templates between stages/phases via document-based interfaces

### **Validation**
Verification of completeness, correctness, and coherence of inputs/outputs

### **Extraction**
Research and retrieval of existing information from knowledge repositories

### **Generation**
Creation of new specifications, implementations, or derived content based on frameworks and methodologies

### **Segmentation**
Breaking down implementation into manageable, independent units for execution