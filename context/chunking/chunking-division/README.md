# Chunking Division Agent

## Problem Statement
Transform Level 4 behavior specifications into execution-ready chunk boundaries with filtered contexts, dependency sequences, and implementation handoffs across abstraction levels 2-6.

## Input Templates

### Abstraction Framework (Root Foundation)
Universal specification progression framework defining 7 abstraction levels (Requirements → Architecture → Interface → Behavior → Strategy → Signature → Implementation) with risk-knowledge mapping across 4 knowledge categories (Constraint, Integration, Pattern, Convention). Establishes the theoretical foundation for all template relationships.

### Context Extraction Output
Comprehensive context knowledge organized across all 7 abstraction levels and 4 knowledge categories, populated from project research. Includes gap analysis identifying missing information and source metadata. Provides the actual knowledge base for informed chunk division and context distribution.

### Level 2 Architecture Specification  
Component relationships, data flows, system structure with core components, dependencies, interactions, and architectural constraints. Builds system foundation from requirements using Infrastructure Knowledge.

### Level 3 Interface Specification
Module boundaries, data schemas, component contracts with interface definitions, input/output specifications, integration contracts, and service boundaries. Defines component interaction contracts using Domain Knowledge.

### Level 4 Behavior Specification
Complete behavioral requirements organized into functional areas with normal behaviors, edge cases, error handling, integration behaviors, and quality requirements. Includes testing strategy with E2E/integration requirements and behavioral dependencies. Primary specification for chunk division.

### Level 4 E2E Test Specification
End-to-end test method signatures with fixtures, assertions, performance thresholds, and validation patterns at Signature Level (Level 6) detail for test immutability. Defines system capability validation requirements.

### Level 4 Integration Test Specification  
Integration test method signatures with component boundaries, mock interfaces, data flow validations, and contract compliance tests at Signature Level (Level 6) detail. Defines component boundary validation requirements.

## Solution Approach

### Phase 1: Boundary Analysis
Determine optimal chunk divisions based on functional areas, integration complexity, and dependency analysis.

### Phase 2: Dependency Analysis  
Generate execution sequence, parallel execution groups, and critical path identification from chunk dependencies.

### Phase 3: Context Distribution
Filter behavioral requirements into focused chunk contexts while maintaining DRY principles and <3K token limits.

### Phase 4: Coordination Synthesis
Generate coordination plans, test contexts, and handoff templates for seamless chunk-to-chunk execution.

## Agent Flow
Level 4 Behavior Specification → Boundary Analysis → Dependency Analysis → Context Distribution → Coordination Synthesis → Execution-Ready Chunks