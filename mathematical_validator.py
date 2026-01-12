"""
Mathematical Validation Layer
Layer 5: Rigorous verification of all mathematical properties and correctness
Comprehensive unit tests and mathematical proofs for the entire system
"""

import numpy as np
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import math
import sys
from pathlib import Path

# Import all layers for validation
from core.core_foundations import (
    AbstractGroup, AbstractOperator, DialecticalStage,
    GroupValidationResult, VectorTransformation, MathematicalError
)
from operators.inrc_operators import (
    IdentityOperator, NegationOperator, ReciprocityOperator, CorrelationOperator,
    INRCOperatorFactory, MatrixOperator, OperatorValidator
)
from dynamics.dialectical_engine import DialecticalEngine, SynthesisMethod
from services.dialectical_service import DialecticalService

# ============================================================================
# 1. VALIDATION RESULTS & METRICS
# ============================================================================

class ValidationStatus(Enum):
    """Status of validation test"""
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class ValidationTest:
    """Individual validation test"""
    name: str
    description: str
    status: ValidationStatus = ValidationStatus.SKIPPED
    details: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    execution_time: float = 0.0
    
    def passed(self) -> bool:
        return self.status == ValidationStatus.PASSED
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'status': self.status.value,
            'details': self.details,
            'error': self.error_message,
            'execution_time': self.execution_time
        }


@dataclass
class ValidationSuite:
    """Suite of validation tests"""
    name: str
    tests: List[ValidationTest] = field(default_factory=list)
    started_at: float = field(default_factory=lambda: time.time())
    completed_at: Optional[float] = None
    
    @property
    def passed_count(self) -> int:
        return sum(1 for t in self.tests if t.passed())
    
    @property
    def total_count(self) -> int:
        return len(self.tests)
    
    @property
    def success_rate(self) -> float:
        return self.passed_count / max(self.total_count, 1)
    
    def add_test(self, test: ValidationTest):
        self.tests.append(test)
    
    def complete(self):
        self.completed_at = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'test_count': self.total_count,
            'passed_count': self.passed_count,
            'success_rate': self.success_rate,
            'duration': (self.completed_at or time.time()) - self.started_at,
            'tests': [t.to_dict() for t in self.tests]
        }


class ValidationReporter:
    """Reports validation results in various formats"""
    
    @staticmethod
    def console_report(suite: ValidationSuite, verbose: bool = True):
        """Print validation results to console"""
        print(f"\n{'='*80}")
        print(f"VALIDATION SUITE: {suite.name}")
        print(f"{'='*80}")
        
        for test in suite.tests:
            status_symbol = {
                ValidationStatus.PASSED: "✅",
                ValidationStatus.FAILED: "❌",
                ValidationStatus.ERROR: "⚠️",
                ValidationStatus.SKIPPED: "⏭️"
            }[test.status]
            
            print(f"{status_symbol} {test.name}: {test.status.value}")
            
            if verbose and test.error_message:
                print(f"   Error: {test.error_message}")
            if verbose and test.details:
                for key, value in test.details.items():
                    print(f"   {key}: {value}")
        
        print(f"\n{'='*80}")
        print(f"SUMMARY: {suite.passed_count}/{suite.total_count} tests passed "
              f"({suite.success_rate*100:.1f}%)")
        
        if suite.success_rate == 1.0:
            print("✅ ALL TESTS PASSED - MATHEMATICAL VALIDATION COMPLETE")
        else:
            print("❌ VALIDATION FAILED - MATHEMATICAL ERRORS DETECTED")
        print(f"{'='*80}")
    
    @staticmethod
    def json_report(suite: ValidationSuite) -> str:
        """Generate JSON report"""
        import json
        return json.dumps(suite.to_dict(), indent=2, default=str)
    
    @staticmethod
    def markdown_report(suite: ValidationSuite, filepath: Optional[str] = None) -> str:
        """Generate Markdown report"""
        report = f"# Validation Report: {suite.name}\n\n"
        report += f"**Date:** {datetime.now().isoformat()}\n"
        report += f"**Results:** {suite.passed_count}/{suite.total_count} passed "
        report += f"({suite.success_rate*100:.1f}%)\n\n"
        
        report += "## Test Results\n\n"
        for test in suite.tests:
            status_emoji = {
                ValidationStatus.PASSED: "✅",
                ValidationStatus.FAILED: "❌",
                ValidationStatus.ERROR: "⚠️",
                ValidationStatus.SKIPPED: "⏭️"
            }[test.status]
            
            report += f"### {status_emoji} {test.name}\n"
            report += f"**Status:** {test.status.value}\n"
            report += f"**Description:** {test.description}\n"
            
            if test.error_message:
                report += f"**Error:** `{test.error_message}`\n"
            
            if test.details:
                report += "**Details:**\n"
                for key, value in test.details.items():
                    report += f"- {key}: {value}\n"
            
            report += "\n"
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(report)
        
        return report


# ============================================================================
# 2. CORE MATHEMATICAL VALIDATOR
# ============================================================================

class MathematicalValidator:
    """
    Main validator for all mathematical properties in the system
    
    Performs rigorous mathematical verification of:
    1. Klein-4 group properties
    2. INRC operator correctness
    3. Dialectical process consistency
    4. Numerical stability and precision
    5. Dimensional consistency
    """
    
    def __init__(self, tolerance: float = 1e-12):
        """
        Initialize validator
        
        Args:
            tolerance: Numerical tolerance for equality comparisons
        """
        self.tolerance = tolerance
        self.test_vectors = {
            2: [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [-1.0, 0.5]],
            3: [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],
                [1.0, 1.0, 1.0], [-1.0, 0.5, 0.3]],
            4: [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0],
                [1.0, -1.0, 1.0, -1.0]]
        }
    
    # ------------------------------------------------------------------------
    # VALIDATION DECORATORS & UTILITIES
    # ------------------------------------------------------------------------
    
    def validate_test(self, name: str, description: str):
        """Decorator for validation tests"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                test = ValidationTest(name=name, description=description)
                start_time = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    
                    if isinstance(result, tuple) and len(result) == 2:
                        passed, details = result
                        test.status = ValidationStatus.PASSED if passed else ValidationStatus.FAILED
                        test.details = details if details else {}
                    elif isinstance(result, bool):
                        test.status = ValidationStatus.PASSED if result else ValidationStatus.FAILED
                    else:
                        test.status = ValidationStatus.PASSED
                    
                except Exception as e:
                    test.status = ValidationStatus.ERROR
                    test.error_message = str(e)
                    test.details = {'exception_type': type(e).__name__}
                
                test.execution_time = time.time() - start_time
                return test
            
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = description
            return wrapper
        
        return decorator
    
    def _vectors_equal(self, v1: List[float], v2: List[float]) -> bool:
        """Compare vectors with tolerance"""
        if len(v1) != len(v2):
            return False
        return all(abs(a - b) <= self.tolerance for a, b in zip(v1, v2))
    
    def _matrices_equal(self, m1: np.ndarray, m2: np.ndarray) -> bool:
        """Compare matrices with tolerance"""
        return np.allclose(m1, m2, atol=self.tolerance)
    
    # ------------------------------------------------------------------------
    # KLEIN-4 GROUP VALIDATION
    # ------------------------------------------------------------------------
    
    @validate_test(
        name="klein4_group_axioms",
        description="Validate all group axioms for Klein-4 group"
    )
    def validate_klein4_group_axioms(self, dimension: int = 3) -> Tuple[bool, Dict]:
        """Validate all group axioms"""
        factory = INRCOperatorFactory()
        matrix_ops = factory.create_matrix_operators(dimension)
        matrices = matrix_ops.get_all_matrices()
        
        results = {}
        
        # 1. Closure: A@B should be one of {I, N, R, C}
        closure_valid = True
        for a_name, a in matrices.items():
            for b_name, b in matrices.items():
                product = a @ b
                matches = False
                for op_name, op in matrices.items():
                    if self._matrices_equal(product, op):
                        matches = True
                        break
                if not matches:
                    closure_valid = False
        results['closure'] = closure_valid
        
        # 2. Associativity: (A@B)@C = A@(B@C)
        associativity_valid = True
        test_vector = np.random.randn(dimension)
        for a_name, a in matrices.items():
            for b_name, b in matrices.items():
                for c_name, c in matrices.items():
                    left = (a @ b) @ c @ test_vector
                    right = a @ (b @ c) @ test_vector
                    if not np.allclose(left, right, atol=self.tolerance):
                        associativity_valid = False
        results['associativity'] = associativity_valid
        
        # 3. Identity: I@A = A@I = A
        identity_valid = True
        I = matrices['I']
        for a_name, a in matrices.items():
            if not (self._matrices_equal(I @ a, a) and self._matrices_equal(a @ I, a)):
                identity_valid = False
        results['identity'] = identity_valid
        
        # 4. Inverses: A@A = I for all A (self-inverse)
        inverses_valid = True
        for a_name, a in matrices.items():
            if not self._matrices_equal(a @ a, I):
                inverses_valid = False
        results['inverses'] = inverses_valid
        
        # 5. Commutativity: A@B = B@A
        commutativity_valid = True
        for a_name, a in matrices.items():
            for b_name, b in matrices.items():
                if not self._matrices_equal(a @ b, b @ a):
                    commutativity_valid = False
        results['commutativity'] = commutativity_valid
        
        all_valid = all(results.values())
        return all_valid, results
    
    @validate_test(
        name="klein4_specific_relations",
        description="Validate specific Klein-4 group relations (N∘R=C, etc.)"
    )
    def validate_klein4_relations(self, dimension: int = 3) -> Tuple[bool, Dict]:
        """Validate Klein-4 specific relations"""
        factory = INRCOperatorFactory()
        matrix_ops = factory.create_matrix_operators(dimension)
        matrices = matrix_ops.get_all_matrices()
        
        relations = [
            ('N', 'R', 'C'),  # N∘R = C
            ('R', 'N', 'C'),  # R∘N = C
            ('R', 'C', 'N'),  # R∘C = N
            ('C', 'R', 'N'),  # C∘R = N
            ('N', 'C', 'R'),  # N∘C = R
            ('C', 'N', 'R')   # C∘N = R
        ]
        
        results = {}
        all_valid = True
        
        for a, b, expected in relations:
            product = matrices[a] @ matrices[b]
            is_equal = self._matrices_equal(product, matrices[expected])
            results[f"{a}∘{b} = {expected}"] = is_equal
            if not is_equal:
                all_valid = False
        
        return all_valid, results
    
    @validate_test(
        name="reciprocity_order_reversal",
        description="Verify R is order reversal (R[i,n-1-i]=1), not cyclic permutation"
    )
    def validate_reciprocity_definition(self, dimensions: List[int] = [2, 3, 4, 5]) -> Tuple[bool, Dict]:
        """Validate R is correctly defined as order reversal"""
        results = {}
        
        for dim in dimensions:
            # Create correct R (order reversal)
            R_correct = np.zeros((dim, dim))
            for i in range(dim):
                R_correct[i, dim - 1 - i] = 1.0
            
            # Create wrong R (cyclic permutation - common error)
            R_wrong = np.zeros((dim, dim))
            for i in range(dim):
                R_wrong[i, (i + 1) % dim] = 1.0
            
            # Check self-inverse property
            correct_self_inverse = self._matrices_equal(R_correct @ R_correct, np.eye(dim))
            wrong_self_inverse = self._matrices_equal(R_wrong @ R_wrong, np.eye(dim))
            
            results[f"dim_{dim}_correct_self_inverse"] = correct_self_inverse
            results[f"dim_{dim}_wrong_self_inverse"] = wrong_self_inverse
            
            # For dim=2, both happen to work
            # For dim>2, only correct should work
            if dim == 2:
                if not (correct_self_inverse and wrong_self_inverse):
                    return False, results
            else:
                if not (correct_self_inverse and not wrong_self_inverse):
                    return False, results
        
        return True, results
    
    # ------------------------------------------------------------------------
    # INRC OPERATOR VALIDATION
    # ------------------------------------------------------------------------
    
    @validate_test(
        name="inrc_operator_properties",
        description="Validate properties of each INRC operator"
    )
    def validate_inrc_operators(self) -> Tuple[bool, Dict]:
        """Validate all INRC operator properties"""
        factory = INRCOperatorFactory()
        operators = factory.create_with_validation()
        
        results = {}
        
        # Test each operator
        for dim in [2, 3, 4]:
            test_vectors = self.test_vectors.get(dim, [])
            
            for op_name, operator in operators.items():
                # Self-inverse property
                self_inverse = True
                for vector in test_vectors:
                    once = operator.apply(vector)
                    twice = operator.apply(once)
                    if not self._vectors_equal(vector, twice):
                        self_inverse = False
                        break
                
                results[f"{op_name}_dim{dim}_self_inverse"] = self_inverse
                
                # Linearity (for linear operators)
                if operator.is_linear():
                    linearity = OperatorValidator.validate_linearity(operator)
                    results[f"{op_name}_dim{dim}_linear"] = linearity
        
        # Validate Klein-4 relations using operators
        test_vector = [1.0, 2.0, 3.0]
        relations_valid = OperatorValidator.validate_klein4_relations(operators)
        results['klein4_relations'] = relations_valid
        
        all_valid = all(results.values())
        return all_valid, results
    
    @validate_test(
        name="operator_matrix_consistency",
        description="Verify operator implementations match matrix representations"
    )
    def validate_operator_matrix_consistency(self, dimensions: List[int] = [2, 3, 4]) -> Tuple[bool, Dict]:
        """Validate that pure Python operators match numpy matrix implementations"""
        results = {}
        
        for dim in dimensions:
            # Create operators
            factory = INRCOperatorFactory()
            operators = factory.create_with_validation()
            matrix_ops = factory.create_matrix_operators(dim)
            matrices = matrix_ops.get_all_matrices()
            
            # Test vectors
            test_vectors = self.test_vectors.get(dim, [])
            
            for op_name in ['I', 'N', 'R', 'C']:
                consistent = True
                
                for vector in test_vectors:
                    # Pure Python operator
                    py_result = operators[op_name].apply(vector)
                    
                    # Matrix operator
                    np_vector = np.array(vector)
                    np_result = matrix_ops.apply_matrix(np_vector, op_name)
                    
                    # Compare
                    if not self._vectors_equal(py_result, np_result.tolist()):
                        consistent = False
                        break
                
                results[f"{op_name}_dim{dim}_consistent"] = consistent
        
        all_valid = all(results.values())
        return all_valid, results
    
    # ------------------------------------------------------------------------
    # DIALECTICAL ENGINE VALIDATION
    # ------------------------------------------------------------------------
    
    @validate_test(
        name="dialectical_stage_transitions",
        description="Validate correct stage transitions in dialectical process"
    )
    def validate_dialectical_transitions(self) -> Tuple[bool, Dict]:
        """Validate dialectical stage transitions"""
        engine = DialecticalEngine()
        
        # Test complete cycle
        initial_thesis = [1.0, 0.5, -0.3]
        states = engine.run_dialectical_cycle(initial_thesis, cycles=1)
        
        results = {}
        
        # Check stage sequence
        expected_stages = [
            DialecticalStage.THESIS,
            DialecticalStage.ANTITHESIS,
            DialecticalStage.SYNTHESIS,
            DialecticalStage.NEGATION_OF_NEGATION
        ]
        
        for i, (state, expected) in enumerate(zip(states, expected_stages)):
            correct = state.stage == expected
            results[f"state_{i+1}_stage_correct"] = correct
        
        # Check that synthesis is computed
        synthesis_state = states[2]
        results["synthesis_computed"] = synthesis_state.has_synthesis
        
        # Check tension analysis works
        try:
            for state in states:
                tension = engine.analyze_tension(state)
                results[f"state_{state.stage.value}_tension_valid"] = (
                    0 <= tension.tension_index <= 1
                )
        except Exception:
            results["tension_analysis_valid"] = False
        
        all_valid = all(results.values())
        return all_valid, results
    
    @validate_test(
        name="synthesis_methods_consistency",
        description="Validate all synthesis methods produce valid results"
    )
    def validate_synthesis_methods(self) -> Tuple[bool, Dict]:
        """Validate all synthesis methods"""
        engine = DialecticalEngine()
        
        # Create test state
        thesis = [1.0, 0.5, -0.3]
        antithesis = [-0.8, 0.7, 0.2]
        state = engine.initialize_state(thesis, antithesis)
        state = engine.apply_negation(state)  # Move to antithesis stage
        
        results = {}
        
        # Test each synthesis method
        for method in SynthesisMethod:
            try:
                # Apply synthesis
                synthesized = engine.synthesize(state, method=method)
                
                # Check results
                results[f"{method.value}_succeeds"] = synthesized.has_synthesis
                results[f"{method.value}_stage_correct"] = (
                    synthesized.stage == DialecticalStage.SYNTHESIS
                )
                
                if synthesized.has_synthesis:
                    synthesis = synthesized.synthesis
                    # Check dimensions match
                    results[f"{method.value}_dimensions_match"] = (
                        len(synthesis) == state.dimensions
                    )
                    # Check synthesis is different from both thesis and antithesis
                    results[f"{method.value}_different_from_thesis"] = (
                        not self._vectors_equal(synthesis, state.thesis)
                    )
                    results[f"{method.value}_different_from_antithesis"] = (
                        not self._vectors_equal(synthesis, state.antithesis)
                    )
            
            except Exception as e:
                results[f"{method.value}_succeeds"] = False
                results[f"{method.value}_error"] = str(e)[:50]
        
        all_valid = all(results.values())
        return all_valid, results
    
    @validate_test(
        name="dialectical_convergence",
        description="Validate convergence detection in dialectical processes"
    )
    def validate_convergence(self) -> Tuple[bool, Dict]:
        """Validate convergence detection"""
        engine = DialecticalEngine()
        
        # Test case that should converge (identical thesis/antithesis)
        thesis = [1.0, 1.0, 1.0]
        antithesis = [-1.0, -1.0, -1.0]
        state = engine.initialize_state(thesis, antithesis)
        
        results = {}
        
        # Run until convergence
        states, converged = engine.run_until_convergence(
            thesis,
            max_cycles=10,
            tolerance=0.01
        )
        
        results["convergence_detected"] = converged
        results["states_generated"] = len(states)
        
        if converged:
            final_state = states[-1]
            final_tension = engine.analyze_tension(final_state)
            results["final_tension_below_tolerance"] = final_tension.tension_index < 0.01
        
        # Test case that shouldn't converge quickly (high tension)
        thesis2 = [1.0, 0.0, -1.0]
        antithesis2 = [-1.0, 1.0, 0.0]
        state2 = engine.initialize_state(thesis2, antithesis2)
        
        states2, converged2 = engine.run_until_convergence(
            thesis2,
            max_cycles=3,  # Small limit
            tolerance=0.01
        )
        
        results["non_convergence_detected"] = not converged2
        results["max_cycles_respected"] = len(states2) <= 10  # 3 cycles * 3 states + 1 initial
        
        all_valid = all(results.values())
        return all_valid, results
    
    # ------------------------------------------------------------------------
    # SERVICE LAYER VALIDATION
    # ------------------------------------------------------------------------
    
    @validate_test(
        name="service_layer_functionality",
        description="Validate service layer operations and process management"
    )
    def validate_service_layer(self) -> Tuple[bool, Dict]:
        """Validate dialectical service functionality"""
        service = DialecticalService()
        
        results = {}
        
        # Create process
        process_id = service.create_process(
            thesis=[1.0, 0.5, -0.3],
            name="Test Process",
            tags=["validation"]
        )
        results["process_creation"] = True
        
        # Get process
        process = service.get_process(process_id)
        results["process_retrieval"] = process is not None
        results["initial_stage_correct"] = (
            process.current_state.stage == DialecticalStage.THESIS
        )
        
        # Run operations
        try:
            # Negate
            negated = service.advance_process(process_id, 'negate')
            results["negation_succeeds"] = (
                negated.stage == DialecticalStage.ANTITHESIS
            )
            
            # Synthesize
            synthesized = service.advance_process(
                process_id, 
                'synthesize',
                method='standard',
                parameters={'alpha': 0.6, 'beta': 0.4}
            )
            results["synthesis_succeeds"] = (
                synthesized.stage == DialecticalStage.SYNTHESIS and
                synthesized.has_synthesis
            )
            
            # Negate negation
            negated_negation = service.advance_process(
                process_id, 
                'negate_negation'
            )
            results["negation_of_negation_succeeds"] = (
                negated_negation.stage == DialecticalStage.NEGATION_OF_NEGATION
            )
        
        except Exception as e:
            results["operations_succeed"] = False
            results["operations_error"] = str(e)[:50]
        
        # List processes
        processes = service.list_processes(tags=["validation"])
        results["process_listing"] = len(processes) > 0
        
        # Analyze process
        analysis = service.analyze_process(process_id)
        results["process_analysis"] = 'current_tension' in analysis
        
        # Clean up
        deleted = service.delete_process(process_id)
        results["process_deletion"] = deleted
        
        # Verify deletion
        try:
            service.get_process(process_id)
            results["process_actually_deleted"] = False
        except ValueError:
            results["process_actually_deleted"] = True
        
        all_valid = all(results.values())
        return all_valid, results
    
    @validate_test(
        name="batch_operations",
        description="Validate batch operations in service layer"
    )
    def validate_batch_operations(self) -> Tuple[bool, Dict]:
        """Validate batch operations"""
        service = DialecticalService()
        
        results = {}
        
        # Batch create
        theses = [
            [1.0, 0.5],
            [0.3, -0.7, 0.2],
            [1.0, 0.0, -1.0, 0.5]
        ]
        
        process_ids = service.batch_create(
            theses=theses,
            names=["Process 1", "Process 2", "Process 3"],
            tags_list=[["batch"], ["batch"], ["batch"]]
        )
        
        results["batch_creation"] = len(process_ids) == 3
        
        # Batch advance
        batch_results = service.batch_advance(
            process_ids=process_ids[:2],  # Test with 2 processes
            operation='negate',
            intensity=0.8
        )
        
        results["batch_advance_succeeds"] = (
            len(batch_results['successful']) == 2 and
            len(batch_results['failed']) == 0
        )
        
        # Clean up
        for pid in process_ids:
            try:
                service.delete_process(pid)
            except:
                pass
        
        all_valid = all(results.values())
        return all_valid, results
    
    # ------------------------------------------------------------------------
    # NUMERICAL STABILITY & EDGE CASES
    # ------------------------------------------------------------------------
    
    @validate_test(
        name="numerical_stability",
        description="Validate numerical stability with extreme values"
    )
    def validate_numerical_stability(self) -> Tuple[bool, Dict]:
        """Validate numerical stability"""
        engine = DialecticalEngine()
        
        test_cases = [
            ("very_small", [1e-10, 1e-15, 1e-20]),
            ("very_large", [1e10, 1e15, 1e20]),
            ("mixed_signs", [1e10, -1e10, 1e-10, -1e-10]),
            ("zero_vector", [0.0, 0.0, 0.0]),
            ("unit_vector", [1.0, 1.0, 1.0]),
        ]
        
        results = {}
        
        for case_name, vector in test_cases:
            try:
                # Initialize and run cycle
                state = engine.initialize_state(vector)
                states = engine.run_dialectical_cycle(
                    vector,
                    cycles=1,
                    synthesis_method=SynthesisMethod.STANDARD
                )
                
                # Check all states are valid
                valid = all(
                    s.dimensions == len(vector)
                    for s in states
                )
                results[f"{case_name}_valid"] = valid
                
                # Check no NaN or Inf
                no_nan_inf = all(
                    all(math.isfinite(v) for v in s.thesis)
                    for s in states
                )
                results[f"{case_name}_finite"] = no_nan_inf
            
            except Exception as e:
                results[f"{case_name}_valid"] = False
                results[f"{case_name}_error"] = type(e).__name__
        
        all_valid = all(results.values())
        return all_valid, results
    
    @validate_test(
        name="dimensional_consistency",
        description="Validate consistency across different dimensions"
    )
    def validate_dimensional_consistency(self, max_dim: int = 10) -> Tuple[bool, Dict]:
        """Validate system works correctly for different dimensions"""
        results = {}
        
        for dim in range(2, max_dim + 1):
            # Create random vector
            vector = np.random.randn(dim).tolist()
            
            try:
                # Test operators
                factory = INRCOperatorFactory()
                operators = factory.create_with_validation()
                
                # Test each operator
                op_results = []
                for op_name, operator in operators.items():
                    result = operator.apply(vector)
                    op_results.append(len(result) == dim)
                
                results[f"dim_{dim}_operators_valid"] = all(op_results)
                
                # Test dialectical cycle
                engine = DialecticalEngine()
                states = engine.run_dialectical_cycle(vector, cycles=1)
                
                cycle_valid = all(
                    s.dimensions == dim for s in states
                )
                results[f"dim_{dim}_cycle_valid"] = cycle_valid
            
            except Exception as e:
                results[f"dim_{dim}_valid"] = False
                results[f"dim_{dim}_error"] = type(e).__name__
        
        all_valid = all(results.values())
        return all_valid, results
    
    # ------------------------------------------------------------------------
    # COMPREHENSIVE VALIDATION SUITE
    # ------------------------------------------------------------------------
    
    def run_comprehensive_validation(self) -> ValidationSuite:
        """
        Run comprehensive validation of entire system
        
        Returns complete validation suite with all tests
        """
        suite = ValidationSuite(name="Xenopoulos Dialectical Framework - Comprehensive Validation")
        
        # Group theory validation
        suite.add_test(self.validate_klein4_group_axioms(dimension=3))
        suite.add_test(self.validate_klein4_relations(dimension=3))
        suite.add_test(self.validate_reciprocity_definition())
        
        # Operator validation
        suite.add_test(self.validate_inrc_operators())
        suite.add_test(self.validate_operator_matrix_consistency())
        
        # Dialectical engine validation
        suite.add_test(self.validate_dialectical_transitions())
        suite.add_test(self.validate_synthesis_methods())
        suite.add_test(self.validate_convergence())
        
        # Service layer validation
        suite.add_test(self.validate_service_layer())
        suite.add_test(self.validate_batch_operations())
        
        # Numerical stability
        suite.add_test(self.validate_numerical_stability())
        suite.add_test(self.validate_dimensional_consistency(max_dim=8))
        
        suite.complete()
        return suite


# ============================================================================
# 3. PROOF SYSTEM (Formal mathematical proofs)
# ============================================================================

class MathematicalProofs:
    """
    Formal mathematical proofs of system properties
    
    Provides rigorous mathematical proofs (not just tests)
    """
    
    @staticmethod
    def prove_klein4_group() -> Dict[str, str]:
        """
        Formal proof that INRC operators form a Klein-4 group
        
        Returns step-by-step proof
        """
        proofs = {
            "theorem": "The set {I, N, R, C} with composition forms a Klein-4 group isomorphic to ℤ₂ × ℤ₂.",
            
            "proof_steps": [
                "1. Define operators:",
                "   I(x) = x (identity)",
                "   N(x) = -x (negation)",
                "   R(x₁,...,xₙ) = (xₙ,...,x₁) (order reversal)",
                "   C = N∘R = R∘N (correlation)",
                
                "2. Show all operators are self-inverse:",
                "   • I∘I(x) = I(x) = x ∴ I² = I",
                "   • N∘N(x) = N(-x) = -(-x) = x ∴ N² = I",
                "   • R∘R(x₁,...,xₙ) = R(xₙ,...,x₁) = (x₁,...,xₙ) ∴ R² = I",
                "   • C∘C = (N∘R)∘(N∘R) = N∘(R∘N)∘R = N∘C∘R = N∘(N∘R)∘R = I",
                
                "3. Verify group axioms:",
                "   • Closure: Composition of any two yields another in set",
                "   • Associativity: Matrix multiplication is associative",
                "   • Identity: I is identity element",
                "   • Inverses: Each element is its own inverse",
                
                "4. Verify Klein-4 specific relations:",
                "   • N∘R = R∘N = C (commutative)",
                "   • R∘C = C∘R = N",
                "   • N∘C = C∘N = R",
                
                "5. Show isomorphism to ℤ₂ × ℤ₂:",
                "   • Map: I → (0,0), N → (1,0), R → (0,1), C → (1,1)",
                "   • Operation corresponds to component-wise addition mod 2",
                
                "6. Prove order reversal (not cyclic) is necessary:",
                "   • Cyclic permutation R' with R'[i,(i+1)%n]=1",
                "   • For n>2: (R')² ≠ I (counterexample: n=3)",
                "   • Therefore only order reversal satisfies R²=I ∀n≥2"
            ],
            
            "conclusion": "The INRC operators with order reversal for R form a Klein-4 group. "
                         "The common implementation error of using cyclic permutation "
                         "breaks the group structure for dimensions > 2."
        }
        
        return proofs
    
    @staticmethod
    def prove_dialectical_properties() -> Dict[str, str]:
        """
        Prove properties of dialectical processes
        """
        proofs = {
            "theorem": "Dialectical processes using INRC operators preserve key mathematical properties.",
            
            "proofs": {
                "tension_bounds": 
                    "Tension index t ∈ [0,1]: "
                    "t = Σ|tᵢ - aᵢ| / Σ(|tᵢ| + |aᵢ|) "
                    "Since |tᵢ - aᵢ| ≤ |tᵢ| + |aᵢ| by triangle inequality, "
                    "each term ≤ 1, so t ≤ 1. Non-negativity is obvious.",
                
                "synthesis_linearity": 
                    "Standard synthesis S = αT + βA is linear: "
                    "S(λT₁ + μT₂, A) = λS(T₁, A) + μS(T₂, A) "
                    "and similarly for antithesis.",
                
                "cycle_convergence": 
                    "For identical thesis/antithesis (T = -A): "
                    "t = 1 initially. After negation: new T' = -A = T, "
                    "new A' = -T' = -T = A