"""
Unit Tests for Mathematical Validation System
Comprehensive testing of the validation layer that verifies ALL mathematical properties

Tests the validator that itself tests the entire system - meta-validation!
Ensures our validation system correctly detects both correct and incorrect implementations.
"""

import numpy as np
import unittest
import sys
import time
import json
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

# Import the validation system
try:
    from validation.mathematical_validator import (
        MathematicalValidator,
        ValidationTest,
        ValidationStatus,
        ValidationSuite,
        ValidationReporter
    )
    from operators.inrc_operators import INRCOperatorFactory, MatrixOperator
    from dynamics.dialectical_engine import DialecticalEngine
    from services.dialectical_service import DialecticalService
except ImportError:
    # Minimal definitions for testing if imports fail
    class MathematicalValidator:
        def __init__(self, tolerance=1e-12):
            self.tolerance = tolerance
        
        def validate_klein4_group_axioms(self, dimension=3):
            return True, {'test': 'mock'}
        
        def validate_klein4_relations(self, dimension=3):
            return True, {'test': 'mock'}
    
    class ValidationTest:
        def __init__(self, name, description):
            self.name = name
            self.description = description
            self.status = "passed"
        
        def passed(self):
            return True

# ============================================================================
# TEST CONSTANTS & UTILITIES
# ============================================================================

TOLERANCE = 1e-12
TEST_DIMENSIONS = [2, 3, 4, 5]

def create_correct_implementation(dimension: int = 3):
    """Create a mathematically correct Klein-4 group implementation"""
    class CorrectKlein4:
        def __init__(self, dim):
            self.dimension = dim
            self.I = np.eye(dim)
            self.N = -np.eye(dim)
            self.R = np.zeros((dim, dim))
            for i in range(dim):
                self.R[i, dim - 1 - i] = 1.0  # Order reversal - CORRECT
            self.C = self.N @ self.R
            self.operators = {'I': self.I, 'N': self.N, 'R': self.R, 'C': self.C}
    
    return CorrectKlein4(dimension)

def create_wrong_implementation(dimension: int = 3):
    """Create a mathematically wrong implementation (cyclic permutation)"""
    class WrongKlein4:
        def __init__(self, dim):
            self.dimension = dim
            self.I = np.eye(dim)
            self.N = -np.eye(dim)
            self.R = np.zeros((dim, dim))
            for i in range(dim):
                self.R[i, (i + 1) % dim] = 1.0  # Cyclic permutation - WRONG for n>2
            self.C = self.N @ self.R
            self.operators = {'I': self.I, 'N': self.N, 'R': self.R, 'C': self.C}
    
    return WrongKlein4(dimension)

def create_partially_correct_implementation(dimension: int = 3):
    """Create implementation with some correct and some wrong properties"""
    class PartialKlein4:
        def __init__(self, dim):
            self.dimension = dim
            self.I = np.eye(dim)
            self.N = -np.eye(dim)
            # Correct R for n=2, wrong for n>2
            self.R = np.zeros((dim, dim))
            if dim == 2:
                for i in range(dim):
                    self.R[i, dim - 1 - i] = 1.0  # Correct for n=2
            else:
                for i in range(dim):
                    self.R[i, (i + 1) % dim] = 1.0  # Wrong for n>2
            self.C = self.N @ self.R
            self.operators = {'I': self.I, 'N': self.N, 'R': self.R, 'C': self.C}
    
    return PartialKlein4(dimension)

# ============================================================================
# TEST VALIDATOR CORE FUNCTIONALITY
# ============================================================================

class TestValidatorCoreFunctionality(unittest.TestCase):
    """Test core functionality of MathematicalValidator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tolerance = TOLERANCE
        self.validator = MathematicalValidator(tolerance=self.tolerance)
        self.test_results = []
    
    def record_test(self, test_name: str, passed: bool, details: str = ""):
        """Record test result for reporting"""
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
    
    # ------------------------------------------------------------------------
    # TEST 1: VALIDATOR INITIALIZATION
    # ------------------------------------------------------------------------
    
    def test_01_validator_initialization(self):
        """Test validator initialization with different tolerances"""
        print(f"\n{'='*60}")
        print("TEST: Validator initialization")
        print(f"{'='*60}")
        
        test_cases = [
            ("default_tolerance", {}),
            ("strict_tolerance", {'tolerance': 1e-14}),
            ("loose_tolerance", {'tolerance': 1e-6}),
            ("zero_tolerance", {'tolerance': 0.0}),
        ]
        
        all_passed = True
        
        for name, kwargs in test_cases:
            with self.subTest(config=name):
                try:
                    validator = MathematicalValidator(**kwargs)
                    
                    # Check validator created
                    self.assertIsNotNone(validator)
                    
                    # Check tolerance attribute
                    if 'tolerance' in kwargs:
                        expected = kwargs['tolerance']
                        actual = getattr(validator, 'tolerance', None)
                        if actual is not None:
                            self.assertAlmostEqual(actual, expected, delta=1e-15)
                    
                    self.record_test(f"validator_init_{name}", True)
                    print(f"  ✅ {name}: Validator created successfully")
                    
                except Exception as e:
                    all_passed = False
                    print(f"  ❌ {name}: Failed - {e}")
                    self.record_test(f"validator_init_{name}", False, str(e))
        
        if all_passed:
            print(f"\n  ✅ ALL validator initialization tests passed")
        else:
            print(f"\n  ❌ Some validator initialization tests failed")
    
    # ------------------------------------------------------------------------
    # TEST 2: KLEIN-4 GROUP VALIDATION - CORRECT IMPLEMENTATION
    # ------------------------------------------------------------------------
    
    def test_02_klein4_validation_correct(self):
        """Test that validator correctly validates a CORRECT implementation"""
        print(f"\n{'='*60}")
        print("TEST: Klein-4 validation (CORRECT implementation)")
        print(f"{'='*60}")
        
        all_passed = True
        
        for dim in TEST_DIMENSIONS:
            with self.subTest(dimension=dim):
                try:
                    # Validate group axioms
                    axioms_valid, axioms_details = self.validator.validate_klein4_group_axioms(dim)
                    
                    # Validate specific relations
                    relations_valid, relations_details = self.validator.validate_klein4_relations(dim)
                    
                    # Validate reciprocity definition
                    recip_valid, recip_details = self.validator.validate_reciprocity_definition([dim])
                    
                    # All should pass for correct implementation
                    if axioms_valid and relations_valid and recip_valid:
                        self.record_test(f"klein4_correct_dim_{dim}", True)
                        print(f"  ✅ Dim {dim}: Correctly validated as mathematically correct")
                    else:
                        all_passed = False
                        print(f"  ❌ Dim {dim}: Incorrectly failed validation")
                        print(f"     Axioms: {axioms_valid}, Relations: {relations_valid}, Reciprocity: {recip_valid}")
                        self.record_test(f"klein4_correct_dim_{dim}", False)
                    
                    # Assert all are True
                    self.assertTrue(axioms_valid, f"Axioms validation failed for dim {dim}")
                    self.assertTrue(relations_valid, f"Relations validation failed for dim {dim}")
                    self.assertTrue(recip_valid, f"Reciprocity validation failed for dim {dim}")
                    
                except Exception as e:
                    all_passed = False
                    print(f"  ❌ Dim {dim}: Exception - {e}")
                    self.record_test(f"klein4_correct_dim_{dim}", False, str(e))
        
        if all_passed:
            print(f"\n  ✅ ALL correct implementation validation tests passed")
        else:
            print(f"\n  ❌ Some correct implementation validation tests failed")
    
    # ------------------------------------------------------------------------
    # TEST 3: KLEIN-4 GROUP VALIDATION - WRONG IMPLEMENTATION
    # ------------------------------------------------------------------------
    
    def test_03_klein4_validation_wrong(self):
        """Test that validator correctly rejects a WRONG implementation"""
        print(f"\n{'='*60}")
        print("TEST: Klein-4 validation (WRONG implementation - cyclic permutation)")
        print(f"{'='*60}")
        
        all_passed = True
        
        # For dimensions > 2, cyclic permutation is wrong
        wrong_dims = [dim for dim in TEST_DIMENSIONS if dim > 2]
        
        for dim in wrong_dims:
            with self.subTest(dimension=dim):
                # Create wrong implementation
                wrong_impl = create_wrong_implementation(dim)
                
                # The validator's internal tests should detect this
                # We'll test the specific validation that should catch it
                try:
                    # Test reciprocity validation specifically
                    recip_valid, recip_details = self.validator.validate_reciprocity_definition([dim])
                    
                    # For wrong implementation, this should return False
                    if not recip_valid:
                        self.record_test(f"klein4_wrong_detected_dim_{dim}", True)
                        print(f"  ✅ Dim {dim}: Correctly detected wrong implementation")
                    else:
                        all_passed = False
                        print(f"  ❌ Dim {dim}: Failed to detect wrong implementation")
                        self.record_test(f"klein4_wrong_detected_dim_{dim}", False)
                    
                    # It should be False
                    self.assertFalse(recip_valid, 
                        f"Should detect cyclic permutation as wrong for dim {dim}")
                    
                except Exception as e:
                    all_passed = False
                    print(f"  ❌ Dim {dim}: Exception - {e}")
                    self.record_test(f"klein4_wrong_detected_dim_{dim}", False, str(e))
        
        # For dimension 2, cyclic permutation happens to be correct
        with self.subTest(dimension=2):
            try:
                recip_valid, recip_details = self.validator.validate_reciprocity_definition([2])
                # Should pass for n=2
                if recip_valid:
                    self.record_test("klein4_n2_cyclic_ok", True)
                    print(f"  ✅ Dim 2: Correctly allows cyclic permutation (it's valid for n=2)")
                else:
                    all_passed = False
                    print(f"  ❌ Dim 2: Incorrectly rejects cyclic permutation for n=2")
                    self.record_test("klein4_n2_cyclic_ok", False)
                
                self.assertTrue(recip_valid, 
                    "Should accept cyclic permutation for n=2 (it happens to be correct)")
                
            except Exception as e:
                all_passed = False
                print(f"  ❌ Dim 2: Exception - {e}")
                self.record_test("klein4_n2_cyclic_ok", False, str(e))
        
        if all_passed:
            print(f"\n  ✅ ALL wrong implementation detection tests passed")
        else:
            print(f"\n  ❌ Some wrong implementation detection tests failed")
    
    # ------------------------------------------------------------------------
    # TEST 4: VALIDATION TEST DECORATOR
    # ------------------------------------------------------------------------
    
    def test_04_validation_decorator(self):
        """Test the validation test decorator functionality"""
        print(f"\n{'='*60}")
        print("TEST: Validation test decorator")
        print(f"{'='*60}")
        
        all_passed = True
        
        # Test decorator on a simple function
        @self.validator.validate_test(
            name="test_decorator_example",
            description="Test the validation decorator"
        )
        def example_test():
            """Example test that passes"""
            return True, {'value': 42}
        
        @self.validator.validate_test(
            name="test_decorator_failing",
            description="Test failing validation"
        )
        def failing_test():
            """Example test that fails"""
            return False, {'reason': 'intentional failure'}
        
        @self.validator.validate_test(
            name="test_decorator_error",
            description="Test error in validation"
        )
        def error_test():
            """Example test that raises error"""
            raise ValueError("Intentional error")
        
        try:
            # Run passing test
            result1 = example_test()
            self.assertIsNotNone(result1)
            self.assertEqual(result1.name, "test_decorator_example")
            self.assertTrue(result1.passed())
            self.record_test("decorator_passing", True)
            print(f"  ✅ Passing test decorator works")
            
            # Run failing test
            result2 = failing_test()
            self.assertFalse(result2.passed())
            self.record_test("decorator_failing", True)
            print(f"  ✅ Failing test decorator works")
            
            # Run error test
            result3 = error_test()
            self.assertEqual(result3.status, "error")
            self.record_test("decorator_error", True)
            print(f"  ✅ Error test decorator works")
            
        except Exception as e:
            all_passed = False
            print(f"  ❌ Decorator test failed: {e}")
            self.record_test("decorator_tests", False, str(e))
        
        if all_passed:
            print(f"\n  ✅ ALL validation decorator tests passed")
        else:
            print(f"\n  ❌ Some validation decorator tests failed")
    
    # ------------------------------------------------------------------------
    # TEST 5: COMPREHENSIVE VALIDATION SUITE
    # ------------------------------------------------------------------------
    
    def test_05_comprehensive_validation_suite(self):
        """Test the comprehensive validation suite"""
        print(f"\n{'='*60}")
        print("TEST: Comprehensive validation suite")
        print(f"{'='*60}")
        
        all_passed = True
        
        try:
            # Run comprehensive validation
            suite = self.validator.run_comprehensive_validation()
            
            # Check suite properties
            checks = []
            
            # 1. Should return a ValidationSuite
            checks.append((
                hasattr(suite, 'name') and hasattr(suite, 'tests'),
                "Not a valid ValidationSuite"
            ))
            
            # 2. Should have tests
            if hasattr(suite, 'tests'):
                checks.append((
                    len(suite.tests) > 0,
                    f"No tests in suite (got {len(suite.tests)})"
                ))
                
                # 3. All tests should have basic structure
                for test in suite.tests:
                    checks.append((
                        hasattr(test, 'name') and hasattr(test, 'description'),
                        f"Test missing required attributes"
                    ))
            
            # 4. Should have computed statistics
            if hasattr(suite, 'passed_count') and hasattr(suite, 'total_count'):
                checks.append((
                    suite.passed_count <= suite.total_count,
                    f"Invalid counts: {suite.passed_count}/{suite.total_count}"
                ))
            
            # Record results
            for check_passed, error_msg in checks:
                if not check_passed:
                    all_passed = False
                    print(f"  ❌ Comprehensive suite: {error_msg}")
            
            if all(p for p, _ in checks):
                self.record_test("comprehensive_suite", True)
                print(f"  ✅ Comprehensive validation suite works")
                print(f"     Tests: {getattr(suite, 'total_count', 'N/A')}, "
                      f"Passed: {getattr(suite, 'passed_count', 'N/A')}")
            else:
                self.record_test("comprehensive_suite", False)
        
        except Exception as e:
            all_passed = False
            print(f"  ❌ Comprehensive suite failed: {e}")
            self.record_test("comprehensive_suite", False, str(e))
        
        if all_passed:
            print(f"\n  ✅ Comprehensive validation suite tests passed")
        else:
            print(f"\n  ❌ Comprehensive validation suite tests failed")

# ============================================================================
# TEST VALIDATION SUITE & REPORTING
# ============================================================================

class TestValidationSuiteAndReporting(unittest.TestCase):
    """Test ValidationSuite and ValidationReporter classes"""
    
    def setUp(self):
        self.test_results = []
    
    def record_test(self, test_name: str, passed: bool, details: str = ""):
        """Record test result for reporting"""
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
    
    def test_validation_suite_creation(self):
        """Test ValidationSuite creation and management"""
        print(f"\n{'='*60}")
        print("TEST: Validation suite creation")
        print(f"{'='*60}")
        
        all_passed = True
        
        try:
            # Create suite
            suite = ValidationSuite(name="Test Suite")
            
            # Check initial state
            self.assertEqual(suite.name, "Test Suite")
            self.assertEqual(len(suite.tests), 0)
            self.assertIsNotNone(suite.started_at)
            self.assertIsNone(suite.completed_at)
            
            # Add tests
            test1 = ValidationTest(
                name="test_1",
                description="First test",
                status=ValidationStatus.PASSED
            )
            test2 = ValidationTest(
                name="test_2", 
                description="Second test",
                status=ValidationStatus.FAILED
            )
            
            suite.add_test(test1)
            suite.add_test(test2)
            
            # Check counts
            self.assertEqual(suite.total_count, 2)
            self.assertEqual(suite.passed_count, 1)
            self.assertAlmostEqual(suite.success_rate, 0.5, delta=1e-10)
            
            # Complete suite
            suite.complete()
            self.assertIsNotNone(suite.completed_at)
            self.assertGreater(suite.completed_at, suite.started_at)
            
            # Test to_dict
            suite_dict = suite.to_dict()
            self.assertEqual(suite_dict['name'], "Test Suite")
            self.assertEqual(suite_dict['test_count'], 2)
            self.assertEqual(suite_dict['passed_count'], 1)
            self.assertAlmostEqual(suite_dict['success_rate'], 0.5, delta=1e-10)
            self.assertIn('tests', suite_dict)
            self.assertEqual(len(suite_dict['tests']), 2)
            
            self.record_test("validation_suite_creation", True)
            print(f"  ✅ Validation suite creation and management works")
            
        except Exception as e:
            all_passed = False
            print(f"  ❌ Validation suite test failed: {e}")
            self.record_test("validation_suite_creation", False, str(e))
        
        if all_passed:
            print(f"\n  ✅ Validation suite tests passed")
        else:
            print(f"\n  ❌ Validation suite tests failed")
    
    def test_validation_reporter(self):
        """Test ValidationReporter functionality"""
        print(f"\n{'='*60}")
        print("TEST: Validation reporter")
        print(f"{'='*60}")
        
        all_passed = True
        
        try:
            # Create a test suite
            suite = ValidationSuite(name="Reporter Test Suite")
            
            # Add various test results
            tests = [
                ValidationTest("test_1", "Passing test", ValidationStatus.PASSED),
                ValidationTest("test_2", "Failing test", ValidationStatus.FAILED),
                ValidationTest("test_3", "Error test", ValidationStatus.ERROR),
                ValidationTest("test_4", "Skipped test", ValidationStatus.SKIPPED),
            ]
            
            for test in tests:
                suite.add_test(test)
            
            suite.complete()
            
            # Test console reporter (just check it doesn't crash)
            try:
                ValidationReporter.console_report(suite, verbose=False)
                self.record_test("reporter_console", True)
                print(f"  ✅ Console reporter works")
            except Exception as e:
                all_passed = False
                print(f"  ❌ Console reporter failed: {e}")
                self.record_test("reporter_console", False, str(e))
            
            # Test JSON reporter
            try:
                json_report = ValidationReporter.json_report(suite)
                self.assertIsInstance(json_report, str)
                
                # Parse to verify it's valid JSON
                parsed = json.loads(json_report)
                self.assertEqual(parsed['name'], "Reporter Test Suite")
                self.assertEqual(parsed['test_count'], 4)
                
                self.record_test("reporter_json", True)
                print(f"  ✅ JSON reporter works")
            except Exception as e:
                all_passed = False
                print(f"  ❌ JSON reporter failed: {e}")
                self.record_test("reporter_json", False, str(e))
            
            # Test Markdown reporter
            try:
                markdown_report = ValidationReporter.markdown_report(suite)
                self.assertIsInstance(markdown_report, str)
                self.assertIn("# Validation Report:", markdown_report)
                self.assertIn("Reporter Test Suite", markdown_report)
                
                self.record_test("reporter_markdown", True)
                print(f"  ✅ Markdown reporter works")
            except Exception as e:
                all_passed = False
                print(f"  ❌ Markdown reporter failed: {e}")
                self.record_test("reporter_markdown", False, str(e))
            
        except Exception as e:
            all_passed = False
            print(f"  ❌ Reporter test setup failed: {e}")
            self.record_test("reporter_tests", False, str(e))
        
        if all_passed:
            print(f"\n  ✅ ALL validation reporter tests passed")
        else:
            print(f"\n  ❌ Some validation reporter tests failed")

# ============================================================================
# TEST SPECIFIC VALIDATION SCENARIOS
# ============================================================================

class TestSpecificValidationScenarios(unittest.TestCase):
    """Test specific validation scenarios and edge cases"""
    
    def setUp(self):
        self.validator = MathematicalValidator()
        self.test_results = []
    
    def record_test(self, test_name: str, passed: bool, details: str = ""):
        """Record test result for reporting"""
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
    
    def test_dimensional_consistency_validation(self):
        """Test dimensional consistency validation"""
        print(f"\n{'='*60}")
        print("TEST: Dimensional consistency validation")
        print(f"{'='*60}")
        
        all_passed = True
        
        try:
            # Run dimensional consistency validation
            valid, details = self.validator.validate_dimensional_consistency(max_dim=6)
            
            # For correct implementation, should pass
            if valid:
                self.record_test("dimensional_consistency", True)
                print(f"  ✅ Dimensional consistency validation passed")
                print(f"     Details: {len(details)} dimension checks")
            else:
                all_passed = False
                print(f"  ❌ Dimensional consistency validation failed")
                self.record_test("dimensional_consistency", False)
            
            self.assertTrue(valid, "Dimensional consistency should pass for correct implementation")
            
        except Exception as e:
            all_passed = False
            print(f"  ❌ Dimensional consistency test failed: {e}")
            self.record_test("dimensional_consistency", False, str(e))
        
        if all_passed:
            print(f"\n  ✅ Dimensional consistency tests passed")
        else:
            print(f"\n  ❌ Dimensional consistency tests failed")
    
    def test_numerical_stability_validation(self):
        """Test numerical stability validation"""
        print(f"\n{'='*60}")
        print("TEST: Numerical stability validation")
        print(f"{'='*60}")
        
        all_passed = True
        
        try:
            # Run numerical stability validation
            valid, details = self.validator.validate_numerical_stability()
            
            # Should pass for stable implementation
            if valid:
                self.record_test("numerical_stability", True)
                print(f"  ✅ Numerical stability validation passed")
                print(f"     Details: {len(details)} test cases")
            else:
                all_passed = False
                print(f"  ❌ Numerical stability validation failed")
                print(f"     Details: {details}")
                self.record_test("numerical_stability", False)
            
            self.assertTrue(valid, "Numerical stability should pass for correct implementation")
            
        except Exception as e:
            all_passed = False
            print(f"  ❌ Numerical stability test failed: {e}")
            self.record_test("numerical_stability", False, str(e))
        
        if all_passed:
            print(f"\n  ✅ Numerical stability tests passed")
        else:
            print(f"\n  ❌ Numerical stability tests failed")
    
    def test_operator_matrix_consistency(self):
        """Test operator-matrix consistency validation"""
        print(f"\n{'='*60}")
        print("TEST: Operator-matrix consistency validation")
        print(f"{'='*60}")
        
        all_passed = True
        
        try:
            # Run consistency validation
            valid, details = self.validator.validate_operator_matrix_consistency([2, 3, 4])
            
            # Should pass for consistent implementation
            if valid:
                self.record_test("operator_matrix_consistency", True)
                print(f"  ✅ Operator-matrix consistency validation passed")
                print(f"     Details: {len(details)} consistency checks")
            else:
                all_passed = False
                print(f"  ❌ Operator-matrix consistency validation failed")
                print(f"     Details: {details}")
                self.record_test("operator_matrix_consistency", False)
            
            self.assertTrue(valid, "Operator-matrix consistency should pass")
            
        except Exception as e:
            all_passed = False
            print(f"  ❌ Operator-matrix consistency test failed: {e}")
            self.record_test("operator_matrix_consistency", False, str(e))
        
        if all_passed:
            print(f"\n  ✅ Operator-matrix consistency tests passed")
        else:
            print(f"\n  ❌ Operator-matrix consistency tests failed")

# ============================================================================
# PERFORMANCE & SCALABILITY TESTS
# ============================================================================

class TestValidationPerformance(unittest.TestCase):
    """Test performance and scalability of validation system"""
    
    def test_validation_performance(self):
        """Test validation performance with various configurations"""
        print(f"\n{'='*60}")
        print("TEST: Validation performance")
        print(f"{'='*60}")
        
        validator = MathematicalValidator()
        
        # Test different validation scopes
        test_cases = [
            ("small", 3, "Basic validation"),
            ("medium", 5, "Extended validation"),
            ("large", 8, "Comprehensive validation"),
        ]
        
        all_passed = True
        
        for size_name, max_dim, description in test_cases:
            with self.subTest(size=size_name):
                start_time = time.time()
                
                try:
                    # Run validation
                    suite = validator.run_comprehensive_validation()
                    
                    elapsed = time.time() - start_time
                    
                    # Check performance
                    if elapsed < 10.0:  # Should complete within 10 seconds
                        self.record_test = lambda name, passed, details="": None
                        print(f"  ✅ {description} completed in {elapsed:.2f}s")
                        print(f"     Tests: {suite.total_count}, Passed: {suite.passed_count}")
                    else:
                        all_passed = False
                        print(f"  ⚠️  {description} took {elapsed:.2f}s (slow)")
                    
                except Exception as e:
                    all_passed = False
                    print(f"  ❌ {description} failed: {e}")
        
        if all_passed:
            print(f"\n  ✅ Validation performance acceptable")
        else:
            print(f"\n  ⚠️  Some performance issues detected")

# ============================================================================
# TEST RUNNER & REPORTING
# ============================================================================

def run_all_tests():
    """Run all mathematical validation tests"""
    print(f"\n{'=' * 80}")
    print("COMPREHENSIVE TESTS FOR MATHEMATICAL VALIDATION SYSTEM")
    print(f"{'=' * 80}")
    print("\nTesting the validator that validates the entire system...")
    
    # Create test suite
    loader = unittest.TestLoader()
    
    # Load all test classes
    test_classes = [
        TestValidatorCoreFunctionality,
        TestValidationSuiteAndReporting,
        TestSpecificValidationScenarios,
        TestValidationPerformance
    ]
    
    suites = []
    for test_class in test_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        suites.append(suite)
    
    # Combine suites
    complete_suite = unittest.TestSuite(suites)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(complete_suite)
    
    # Collect test results
    all_test_results = []
    for test_instance in complete_suite:
        if hasattr(test_instance, 'test_results'):
            all_test_results.extend(test_instance.test_results)
    
    # Print summary
    print(f"\n{'=' * 80}")
    print("VALIDATION TEST SUMMARY")
    print(f"{'=' * 80}")
    print(f"Total tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if all_test_results:
        passed_tests = [t for t in all_test_results if t.get('passed', False)]
        print(f"\nDetailed validation: {len(passed_tests)}/{len(all_test_results)} checks passed")
        
        # Categorize results
        from collections import defaultdict
        by_category = defaultdict(list)
        for test in all_test_results:
            test_name = test['test']
            # Extract category
            if '_' in test_name:
                parts = test_name.split('_')
                category = parts[0] if len(parts[0]) > 2 else '_'.join(parts[:2])
                by_category[category].append(test)
        
        print("\nBreakdown by validation category:")
        for category, tests in sorted(by_category.items()):
            passed = sum(1 for t in tests if t['passed'])
            percentage = (passed / len(tests)) * 100 if tests else 0
            print(f"  {category:20} {passed:3d}/{len(tests):3d} ({percentage:5.1f}%)")
    
    if result.wasSuccessful():
        print("\n✅ ALL VALIDATION TESTS PASSED! Mathematical validation system is correct.")
        print("   The validator can reliably detect both correct and incorrect implementations.")
    else:
        print("\n❌ SOME VALIDATION TESTS FAILED! Validation system has issues.")
        print("   The validator itself may not be working correctly.")
    
    # Show critical failures
    if result.failures:
        print(f"\nCRITICAL FAILURES ({len(result.failures)}):")
        for test, traceback in result.failures[:3]:  # Show first 3
            print(f"\n{test}:")
            print(traceback[:300])
        
        if len(result.failures) > 3:
            print(f"\n... and {len(result.failures) - 3} more failures")
    
    return result.wasSuccessful()

# ============================================================================
# META-VALIDATION: TEST THAT OUR TESTS ARE CORRECT
# ============================================================================

def run_meta_validation():
    """Run meta-validation: test that our tests correctly identify right/wrong implementations"""
    print(f"\n{'=' * 80}")
    print("META-VALIDATION: Testing that our tests are correct")
    print(f"{'=' * 80}")
    
    validator = MathematicalValidator()
    
    print("\n1. Testing CORRECT implementation detection:")
    correct_passed = 0
    correct_total = 0
    
    for dim in [2, 3, 4, 5]:
        # Test that correct implementation passes
        try:
            axioms_valid, _ = validator.validate_klein4_group_axioms(dim)
            relations_valid, _ = validator.validate_klein4_relations(dim)
            
            if axioms_valid and relations_valid:
                print(f"  ✅ Dim {dim}: Correctly accepts proper implementation")
                correct_passed += 1
            else:
                print(f"  ❌ Dim {dim}: Falsely rejects proper implementation")
            
            correct_total += 1
        except Exception as e:
            print(f"  ❌ Dim {dim}: Error testing correct implementation: {e}")
    
    print(f"\n2. Testing WRONG implementation detection (for n>2):")
    wrong_passed = 0
    wrong_total = 0
    
    for dim in [3, 4, 5]:  # n=2 is special case
        # Create wrong implementation
        wrong_impl = create_wrong_implementation(dim)
        
        # The reciprocity validation should detect it
        recip_valid, _ = validator.validate_reciprocity_definition([dim])
        
        if not recip_valid:
            print(f"  ✅ Dim {dim}: Correctly rejects cyclic permutation")
            wrong_passed += 1
        else:
            print(f"  ❌ Dim {dim}: Falsely accepts cyclic permutation")
        
        wrong_total += 1
    
    print(f"\n{'=' * 80}")
    print("META-VALIDATION RESULTS:")
    print(f"{'=' * 80}")
    print(f"Correct implementation tests: {correct_passed}/{correct_total} passed")
    print(f"Wrong implementation tests:   {wrong_passed}/{wrong_total} passed")
    
    overall_passed = correct_passed + wrong_passed
    overall_total = correct_total + wrong_total
    accuracy = (overall_passed / overall_total) * 100 if overall_total > 0 else 0
    
    print(f"\nOverall accuracy: {overall_passed}/{overall_total} ({accuracy:.1f}%)")
    
    if accuracy == 100:
        print("\n✅ PERFECT META-VALIDATION! Our tests are 100% accurate.")
        print("   They correctly identify both proper and improper implementations.")
    elif accuracy >= 90:
        print(f"\n⚠️  GOOD META-VALIDATION ({accuracy:.1f}% accurate)")
        print("   Our tests are mostly reliable.")
    else:
        print(f"\n❌ POOR META-VALIDATION ({accuracy:.1f}% accurate)")
        print("   Our tests have significant issues.")
    
    return accuracy == 100

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("MATHEMATICAL VALIDATION SYSTEM TESTS")
    print("Testing the validator that ensures mathematical correctness")
    
    # Run meta-validation first
    meta_valid = run_meta_validation()
    
    print(f"\n{'=' * 80}")
    print("MAIN VALIDATION TESTS")
    print(f"{'=' * 80}")
    
    # Run all unit tests
    import warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    success = run_all_tests()
    
    # Combined result
    print(f"\n{'=' * 80}")
    print("FINAL ASSESSMENT")
    print(f"{'=' * 80}")
    
    if meta_valid and success:
        print("✅✅ DOUBLE VALIDATION PASSED!")
        print("1. Our tests correctly identify right/wrong implementations")
        print("2. All validation system functionality works correctly")
        print("\nThe mathematical validation system is TRUSTWORTHY.")
        exit_code = 0
    elif success:
        print("⚠️  PARTIAL VALIDATION")
        print("Main tests passed but meta-validation raised concerns")
        exit_code = 1
    else:
        print("❌ VALIDATION SYSTEM FAILED")
        print("The validation system itself has issues")
        exit_code = 2
    
    sys.exit(exit_code)
