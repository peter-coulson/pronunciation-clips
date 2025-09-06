# System Terminology

## Process Structure

### **Process**
One of 7 main implementation workflows executed sequentially:
1. **Architecture Design** (`01-architecture-design/`)
2. **Interface Design** (`02-interface-design/`)
3. **Behavior Specification** (`03-behavior-specification/`)
4. **Implementation Segmentation** (`04-implementation-segmentation/`)
5. **Execution Orchestration** (`05-execution-orchestration/`)
6. **Test Implementation** (`06-test-implementation/`)
7. **Segmented Implementation** (`07-segmented-implementation/`)

### **Subprocess**
Individual execution steps within a process that follow shared patterns (e.g., context loading, validation gates, template completion)

### **Universal Agent**
Single agent with core execution patterns in system prompt that dynamically loads methodology files for specialization

### **Methodology File**
Process-specific instructions (`methodology.md`) containing todo generation, subprocess steps, context requirements, and validation gates

### **Session**
Single execution instance of the complete 7-process system for one implementation request

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