# Chunking System Workflow

## Input Structure
The input to this system will come from a combination of:
- Repository main context for generic project wide guidelines
- A highly detailed file containing all the necessary specifications for the chunking system to implement the changes

This should allow for very little decisions made by the chunking system as they should be predefined in this file or in the repository context.

## System Foundation
The foundation of the system is its test driven framework. This starts with the main predefined E2E testing scenarios in the input file. These E2E tests will be solely for the entire implementation and not at the chunk level.

## Workflow Steps

### 1. Input Validation
The system should start by validating this file with a specific agent, checking it has all the necessary details and that it is clear.

### 2. E2E Test Setup
The chunking system will first set-up the E2E tests in the main tests folder and validate they are running. This should be done by an agent with separate permissions. Then all further agents will not have permissions to edit these files. We may need to override these whilst running due to bugs in the tests, however, that will be something the user must decide so permission restrictions hold.

### 3. Chunking Analysis
The system will then run a chunking analysis that will likely require a specialized agent, to divide the full tasks into chunks. The chunking division agent should also probably define:
- The success criteria and the tests for each chunk
- Any E2E tests that would be valuable across a few chunks
- Integration tests
- The dependency tree of chunks to determine which can be ran in parallel
- Any contracts if we are using them

### 4. Implementation
The system then implements the main code of the project, as defined by the chunking agent. Running the tasks in parallel if possible, and using handoff markdown files built from templates between dependent agents. The agent cannot mark the task complete without all tests passing unless there is some catastrophic failure.

### 5. Final Validation
Once all coding has been completed, a specialized final agent will be called to run the E2E tests + all other tests. It will implement any bug fixes it finds from these E2E tests until everything is working. It will then generate the final report with the full details of the implementation.

### 6. Context System Update
Then the main agent will update the main context system with the results of the chunking procedure and all relevant files. This may or may not need a specialized agent to be decided later. It will then also update a file tracking the general system success and review future implementations / optimizations.

## System Orchestration
The entirety of this will be ran by the main agent through claude code. The main agent will be keeping the rest of the context system up to date with progress as we go along, including the main claude.md file in the case of a failure.

## Target Scope
The target change size of this system is at minimum a large single file implementation and at maximum a medium to medium/large sized module.