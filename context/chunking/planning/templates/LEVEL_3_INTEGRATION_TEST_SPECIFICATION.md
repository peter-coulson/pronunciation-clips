# Level 3 Integration Test Specification Template

**Feature Name**: [FROM CONTEXT EXTRACTION]
**Target Specification Level**: Integration Testing Interface (Level 3)
**Detail Level**: Signature (Level 6) - Required for test immutability

---

## Integration Test Methods

### [INTEGRATION_TEST_1]
**Method Signature**: `test_[component_a]_[component_b]_integration()`
**Components Under Test**: 
- `[ComponentA]` 
- `[ComponentB]`

**Mock Signatures**:
- `mock_[external_dependency]()` returns `[return_schema]`

**Test Data**:
- `[input_data_var]`: `[data_type]` - [purpose]

**Integration Assertions**:
- `assert [component_a].[method]([params]) == [expected]`
- `assert [component_b].[state_field] == [expected_value]`

### [INTEGRATION_TEST_2]  
**Method Signature**: `test_[integration_scenario]()`
**Components Under Test**:
- `[ComponentA]`
- `[ComponentB]`

**Mock Signatures**:
- `mock_[dependency]()` returns `[schema]`

**Integration Assertions**:
- `assert [condition]` - [requirement]

---

## Mock Method Signatures

### [MOCK_SET_1]
**Mock Method**: `create_[component]_mock()`
**Return Interface**:
```
{
  "[method_name]": [return_type],
  "[method_name]": [return_type]  
}
```

**Configuration Parameters**:
- `[param_name]`: [type] - [mock_behavior]

---

## Data Flow Test Signatures

### [DATA_FLOW_TEST_1]
**Method Signature**: `test_[data_type]_flow_[source]_to_[destination]()`
**Input Schema**:
```
{
  "[field]": [type],
  "[field]": [type]
}
```

**Output Validation**:
- `assert [output].[field] == [transformed_value]`
- `assert [output_schema_validation]([result])`

---

## Error Integration Signatures

### [ERROR_TEST_1] 
**Method Signature**: `test_[component]_[error_type]_propagation()`
**Error Trigger**: `[component].[method]()` raises `[ExceptionType]`
**Propagation Assertion**: `assert [downstream_component].[state] == [error_state]`

### [ERROR_TEST_2]
**Method Signature**: `test_[recovery_scenario]()`
**Recovery Trigger**: `[recovery_method]([params])`
**Recovery Assertion**: `assert [system_state] == [recovered_state]`

---

## Contract Validation Signatures

### [CONTRACT_TEST_1]
**Method Signature**: `test_[interface]_contract_compliance()`
**Interface Schema**:
```
request: {
  "[field]": [type]
}
response: {  
  "[field]": [type]
}
```

**Contract Assertions**:
- `assert [response].[field] == [expected_type]`
- `assert [validation_method]([response])`

---

## State Consistency Signatures

### [STATE_TEST_1]
**Method Signature**: `test_[components]_state_consistency()`
**State Validation**:
- `assert [component_a].[state_field] == [component_b].[related_field]`

**Transaction Test**: `test_[operation]_transaction_consistency()`
**Rollback Assertion**: `assert [pre_state] == [post_rollback_state]`

---

## Test Setup Signatures

### Configuration Methods
**Setup Method**: `setup_[integration_scenario]()`
**Return Type**: `[test_context_type]`

**Teardown Method**: `teardown_[integration_scenario]([context])`

### Fixture Methods
**[FIXTURE_LOADER]**: `load_[integration_data]()`
**Return Schema**:
```
{
  "[component_data]": [schema],
  "[expected_results]": [schema]
}
```

---

## Context Integration Notes

### Applied Context Knowledge
**Constraint Knowledge Applied**: 
- 

**Integration Knowledge Applied**: 
- 

**Pattern Knowledge Applied**: 
- 

**Convention Knowledge Applied**: 
- 