Xenopoulos Logic-Dialectic System - API Reference

## Table of Contents
1. [Overview](#overview)
2. [Core Module (`xenopoulos.core`)](#core-module-xenopouloscore)
3. [Operators Module (`xenopoulos.operators`)](#operators-module-xenopoulosoperators)
4. [Dynamics Module (`xenopoulos.dynamics`)](#dynamics-module-xenopoulosdynamics)
5. [Services Module (`xenopoulos.services`)](#services-module-xenopoulosservices)
6. [Validation Module (`xenopoulos.validation`)](#validation-module-xenopoulosvalidation)
7. [Factory Module (`xenopoulos.factory`)](#factory-module-xenopoulosfactory)
8. [Utility Functions](#utility-functions)
9. [Examples & Usage Patterns](#examples--usage-patterns)

## Overview

This API reference documents the complete implementation of Xenopoulos' Fourth Logical Structure, a mathematical formalization of dialectical logic through Piaget's INRC operators forming a Klein-4 group.

## Core Module (`xenopoulos.core`)

### AbstractGroup Class
Base class for mathematical groups.

```python
from xenopoulos.core import AbstractGroup

class MyGroup(AbstractGroup):
    def is_group(self) -> bool:
        """Verify all group axioms"""
    
    def get_elements(self) -> List[str]:
        """Get all group elements"""
    
    def compose(self, a: str, b: str) -> str:
        """Compose two group elements: a ∘ b"""
    
    def inverse(self, element: str) -> str:
        """Get inverse of element"""
    
    def identity(self) -> str:
        """Get identity element"""
AbstractOperator Class
Base class for mathematical operators.

python
from xenopoulos.core import AbstractOperator

class MyOperator(AbstractOperator):
    def __init__(self, symbol: str, description: str):
        super().__init__(symbol, description)
    
    def apply(self, vector: List[float]) -> List[float]:
        """Apply operator to vector"""
    
    def is_linear(self) -> bool:
        """Check if operator is linear"""
Data Classes
DialecticalTransition
python
from xenopoulos.core import DialecticalTransition

transition = DialecticalTransition(
    from_stage=DialecticalStage.THESIS,
    to_stage=DialecticalStage.ANTITHESIS,
    transformation="negation",
    parameters={"intensity": 0.8}
)
GroupValidationResult
python
from xenopoulos.core import GroupValidationResult

result = GroupValidationResult(
    is_group=True,
    properties={GroupProperty.CLOSURE: True, GroupProperty.ASSOCIATIVITY: True},
    errors=[]
)
VectorTransformation
python
from xenopoulos.core import VectorTransformation

transformation = VectorTransformation(
    original=[1.0, 2.0, 3.0],
    transformed=[-1.0, -2.0, -3.0],
    operator_symbol="N",
    operator_description="Negation Operator"
)
Operators Module (xenopoulos.operators)
Klein4Group Class
Complete implementation of Piaget's INRC operators forming a Klein-4 group.

python
from xenopoulos.operators import Klein4Group

# Initialize group
group = Klein4Group(dimension=3)

# Get all elements
elements = group.get_elements()  # ['I', 'N', 'R', 'C']

# Apply operator to vector
vector = [1.0, 2.0, 3.0]
negated = group.apply_operator(vector, 'N')  # [-1.0, -2.0, -3.0]
reversed = group.apply_operator(vector, 'R')  # [3.0, 2.0, 1.0]

# Compose operators
composition = group.compose('N', 'R')  # 'C'
inverse_n = group.inverse('N')  # 'N' (self-inverse)

# Get identity
identity = group.identity()  # 'I'

# Validate group
is_valid = group.is_group()  # True
validation_result = group.validate()  # GroupValidationResult
INRCOperators Class
Individual operator implementations.

python
from xenopoulos.operators import IdentityOperator, NegationOperator, ReciprocityOperator, CorrelationOperator

# Create operators
I_op = IdentityOperator()
N_op = NegationOperator()
R_op = ReciprocityOperator(dimension=3)
C_op = CorrelationOperator(dimension=3)

# Apply operators
result_i = I_op.apply([1, 2, 3])  # [1, 2, 3]
result_n = N_op.apply([1, 2, 3])  # [-1, -2, -3]
result_r = R_op.apply([1, 2, 3])  # [3, 2, 1]
result_c = C_op.apply([1, 2, 3])  # [-3, -2, -1]

# Check properties
print(I_op.is_linear())  # True
print(N_op.is_self_inverse())  # True
print(R_op.symbol)  # 'R'
Dynamics Module (xenopoulos.dynamics)
DialecticalEngine Class
Manages complete dialectical processes.

python
from xenopoulos.dynamics import DialecticalEngine

# Initialize with Klein-4 group
engine = DialecticalEngine(group)

# Run dialectical cycle
states = engine.run_dialectical_cycle(
    initial_thesis=[1.0, 0.5, -0.5],
    cycles=3,
    synthesis_method='geometric'
)

# Access states
for state in states:
    print(f"Stage: {state.stage}")
    print(f"Thesis: {state.thesis}")
    print(f"Antithesis: {state.antithesis}")
    print(f"Synthesis: {state.synthesis}")
    print(f"Tension: {state.tension_metrics['tension_index']}")

# Get current state
current = engine.get_current_state()

# Get history
history = engine.get_transition_history()
DialecticalState Class
python
from xenopoulos.dynamics import DialecticalState

state = DialecticalState(
    thesis=[1.0, 0.5, -0.3],
    antithesis=[-0.8, 0.3, 0.6],
    synthesis=[0.1, 0.4, 0.15],
    stage=DialecticalStage.SYNTHESIS,
    transition_history=[...],
    tension_metrics={'tension_index': 0.75}
)
Services Module (xenopoulos.services)
DialecticalService Class
High-level API for dialectical processes.

python
from xenopoulos.services import DialecticalService

# Initialize service
service = DialecticalService()

# Create dialectical process
process_id = service.create_dialectical_process(
    thesis=[1.0, 0.5, -0.3],
    antithesis=[-0.8, 0.4, 0.5],
    name="Philosophical Inquiry",
    parameters={"synthesis_method": "dialectical"}
)

# Run full cycle
states = service.run_full_cycle(process_id, cycles=2)

# Advance process step by step
service.advance_process(process_id, 'negate')
service.advance_process(process_id, 'synthesize')
service.advance_process(process_id, 'negate_negation')

# Analyze process
analysis = service.analyze_process(process_id)
print(f"Tension analysis: {analysis['tension_analysis']}")
print(f"Transition count: {analysis['transition_count']}")
print(f"Current stage: {analysis['current_stage']}")

# Get process info
info = service.get_process_info(process_id)

# List all processes
processes = service.list_processes()

# Export/import
exported = service.export_process(process_id)
new_id = service.import_process(exported)
Validation Module (xenopoulos.validation)
MathematicalValidator Class
Validates mathematical properties of the system.

python
from xenopoulos.validation import MathematicalValidator

validator = MathematicalValidator()

# Validate Klein-4 group
group_results = validator.validate_klein4_group(group)
print(f"Closure: {group_results['closure']}")
print(f"Associativity: {group_results['associativity']}")
print(f"Identity: {group_results['identity']}")
print(f"Inverses: {group_results['inverses']}")
print(f"Klein-4 relations: {group_results['klein4_relations']}")

# Validate dialectical process
process_results = validator.validate_dialectical_process(process_id)

# Check mathematical consistency
consistency = validator.check_mathematical_consistency()

# Run comprehensive validation suite
full_report = validator.run_comprehensive_validation()
Factory Module (xenopoulos.factory)
DialecticalFactory Class
Factory pattern for creating system components.

python
from xenopoulos.factory import DialecticalFactory

factory = DialecticalFactory()

# Create complete system
service = factory.create_dialectical_service()

# Create individual components
group = factory.create_klein4_group(dimension=3)
engine = factory.create_dialectical_engine(group)
validator = factory.create_mathematical_validator()

# Create with custom parameters
custom_service = factory.create_dialectical_service(
    group_dimension=4,
    synthesis_method='linear',
    include_validation=True
)

# Get factory configuration
config = factory.get_configuration()
available_components = factory.list_available_components()
Utility Functions
MathUtils
Pure mathematical utility functions.

python
from xenopoulos.core import MathUtils

# Vector comparison
v1 = [1.0, 2.0, 3.0]
v2 = [1.000000001, 2.000000001, 3.000000001]
are_equal = MathUtils.vectors_equal(v1, v2, tolerance=1e-6)  # True

# Identity matrix check
matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
is_identity = MathUtils.is_identity_matrix(matrix)  # True

# Group property validation
elements = ['I', 'N', 'R', 'C']
closure_valid = MathUtils.validate_closure(elements, compose_func)
associativity_valid = MathUtils.validate_associativity(elements, apply_func)
Examples & Usage Patterns
Basic Usage Pattern
python
# Quick start with factory
from xenopoulos.factory import DialecticalFactory

factory = DialecticalFactory()
service = factory.create_dialectical_service()

# Create and run process
process_id = service.create_dialectical_process(
    thesis=[1.0, 0.5, -0.3],
    name="Test Process"
)

states = service.run_full_cycle(process_id, cycles=2)
analysis = service.analyze_process(process_id)
Advanced Analysis Pattern
python
# Custom analysis with individual components
from xenopoulos.operators import Klein4Group
from xenopoulos.dynamics import DialecticalEngine
from xenopoulos.validation import MathematicalValidator

# Create components
group = Klein4Group(dimension=3)
engine = DialecticalEngine(group)
validator = MathematicalValidator()

# Run custom analysis
states = engine.run_dialectical_cycle(
    initial_thesis=[1.0, 0.0, -0.5],
    cycles=5,
    synthesis_method='dialectical'
)

# Validate results
validation = validator.validate_dialectical_states(states)
group_validation = validator.validate_klein4_group(group)
Testing Pattern
python
# Unit testing example
import pytest
from xenopoulos.operators import Klein4Group

def test_klein4_group_properties():
    """Test all Klein-4 group properties"""
    group = Klein4Group(dimension=3)
    
    # Test closure
    for a in group.get_elements():
        for b in group.get_elements():
            result = group.compose(a, b)
            assert result in group.get_elements()
    
    # Test self-inverse
    assert group.compose('N', 'N') == 'I'
    assert group.compose('R', 'R') == 'I'
    assert group.compose('C', 'C') == 'I'
    
    # Test Klein-4 relations
    assert group.compose('N', 'R') == 'C'
    assert group.compose('R', 'N') == 'C'
    assert group.compose('R', 'C') == 'N'
    
    print("All tests passed!")
Error Handling
python
try:
    group = Klein4Group(dimension=1)  # Requires dimension >= 2
except DimensionMismatchError as e:
    print(f"Error: {e}")
    group = Klein4Group(dimension=2)  # Fix dimension

try:
    result = group.apply_operator([1, 2], 'X')  # Invalid operator
except ValueError as e:
    print(f"Invalid operator: {e}")
    result = group.apply_operator([1, 2], 'I')  # Use valid operator
Performance Considerations
Matrix operations: Optimized with NumPy

Vector dimensions: Typically 2-50 dimensions

Memory usage: O(n²) for n-dimensional operators

Batch processing: Supported for multiple vectors

Version Compatibility
Python: 3.8+

NumPy: Required for matrix operations

No external dependencies in core module

Optional dependencies: NumPy for advanced features

Support & Contact
For API-related questions:

Check the examples in /examples/

Review test cases in /tests/

Open an issue on GitHub

Contact: katerinaxenopoulou@gmail.com

Last Updated: January 2026
Documentation Version: 1.0
API Version: 1.0.0
Repository: https://github.com/kxenopoulou/xenopoulos-logic-dialectic
