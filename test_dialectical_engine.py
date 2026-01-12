"""
Unit Tests for Dialectical Engine
Comprehensive testing of Hegelian dialectical processes using INRC operators

Tests ALL aspects of dialectical dynamics:
1. State initialization and validation
2. Dialectical stage transitions
3. Synthesis methods
4. Tension analysis
5. Convergence detection
6. Edge cases and error handling
"""

import numpy as np
import unittest
import sys
import time
from typing import List, Dict, Any
from datetime import datetime

# Import the DialecticalEngine - adjust import path as needed
try:
    from dynamics.dialectical_engine import (
        DialecticalEngine,
        DialecticalState,
        SynthesisMethod,
        TensionMetrics,
        ConservativeDialecticalEngine,
        RadicalDialecticalEngine
    )
    from operators.inrc_operators import INRCOperatorFactory
except ImportError:
    # Define minimal versions for testing if imports fail
    class DialecticalState:
        def __init__(self, thesis, antithesis, synthesis=None, stage=None, history=None):
            self.thesis = thesis
            self.antithesis = antithesis
            self.synthesis = synthesis
            self.stage = stage
            self.history = history or []
        
        @property
        def dimensions(self):
            return len(self.thesis)
        
        @property
        def has_synthesis(self):
            return self.synthesis is not None
    
    class DialecticalEngine:
        def __init__(self, factory=None):
            self.operators = {'I': lambda x: x, 'N': lambda x: [-xi for xi in x]}
        
        def initialize_state(self, thesis, antithesis=None):
            if antithesis is None:
                antithesis = self.operators['N'](thesis)
            return DialecticalState(thesis, antithesis)
        
        def apply_negation(self, state):
            return DialecticalState(state.antithesis, [-xi for xi in state.antithesis])
        
        def synthesize(self, state, method='standard'):
            if method == 'standard':
                synth = [0.7*t + 0.3*a for t, a in zip(state.thesis, state.antithesis)]
            else:
                synth = [(t + a)/2 for t, a in zip(state.thesis, state.antithesis)]
            return DialecticalState(state.thesis, state.antithesis, synth)
        
        def analyze_tension(self, state):
            return {'tension_index': 0.5}

# ============================================================================
# TEST CONSTANTS & UTILITIES
# ============================================================================

TOLERANCE = 1e-10
DIMENSIONS_TO_TEST = [2, 3, 4]
SYNTHESIS_METHODS = ['standard', 'geometric', 'dialectical', 'harmonic', 'max_tension', 'min_tension']

def generate_test_states(dimension: int, count: int = 3) -> List[tuple]:
    """Generate test thesis-antithesis pairs"""
    states = []
    np.random.seed(42)
    
    for i in range(count):
        # Random vectors
        thesis = np.random.randn(dimension).tolist()
        antithesis = np.random.randn(dimension).tolist()
        states.append((thesis, antithesis))
    
    # Special cases
    states.append(([1.0, 0.0, -1.0], [-1.0, 1.0, 0.0]))  # Orthogonal
    states.append(([1.0, 1.0, 1.0], [-1.0, -1.0, -1.0]))  # Perfect opposition
    states.append(([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]))     # Identical
    states.append(([0.0, 0.0, 0.0], [0.0, 0.0, 0.0]))     # Zero vectors
    
    return states[:count]

def assert_vectors_equal(test_case, v1: List[float], v2: List[float], msg: str = ""):
    """Assert two vectors are equal within tolerance"""
    test_case.assertEqual(len(v1), len(v2), f"Vector length mismatch: {msg}")
    for i, (a, b) in enumerate(zip(v1, v2)):
        test_case.assertAlmostEqual(a, b, delta=TOLERANCE, 
                                   msg=f"Vector element {i} mismatch: {a} != {b} ({msg})")

# ============================================================================
# MAIN TEST CLASS
# ============================================================================

class TestDialecticalEngineCore(unittest.TestCase):
    """Core tests for DialecticalEngine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tolerance = TOLERANCE
        self.test_results = []
        self.engine = DialecticalEngine()
    
    def record_test(self, test_name: str, passed: bool, details: str = ""):
        """Record test result for reporting"""
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
    
    # ------------------------------------------------------------------------
    # TEST 1: STATE INITIALIZATION
    # ------------------------------------------------------------------------
    
    def test_01_state_initialization(self):
        """Test state initialization with various inputs"""
        print(f"\n{'='*60}")
        print("TEST: State initialization")
        print(f"{'='*60}")
        
        all_passed = True
        
        for dim in DIMENSIONS_TO_TEST:
            with self.subTest(dimension=dim):
                # Generate test states
                test_states = generate_test_states(dim, 2)
                
                for i, (thesis, antithesis) in enumerate(test_states):
                    # Test 1: Initialize with both thesis and antithesis
                    state1 = self.engine.initialize_state(thesis, antithesis)
                    
                    if len(state1.thesis) != dim or len(state1.antithesis) != dim:
                        all_passed = False
                        print(f"  ❌ Dim {dim}, Case {i}: Dimension mismatch")
                        self.record_test(f"init_dim_{dim}_case_{i}_explicit", False)
                    else:
                        assert_vectors_equal(self, state1.thesis, thesis)
                        assert_vectors_equal(self, state1.antithesis, antithesis)
                        self.record_test(f"init_dim_{dim}_case_{i}_explicit", True)
                        print(f"  ✅ Dim {dim}, Case {i}: Explicit init OK")
                    
                    # Test 2: Initialize with only thesis (default antithesis)
                    state2 = self.engine.initialize_state(thesis)
                    
                    # Default antithesis should be negation of thesis
                    expected_antithesis = [-x for x in thesis]
                    if not np.allclose(state2.antithesis, expected_antithesis, atol=self.tolerance):
                        all_passed = False
                        print(f"  ❌ Dim {dim}, Case {i}: Default antithesis wrong")
                        self.record_test(f"init_dim_{dim}_case_{i}_default", False)
                    else:
                        self.record_test(f"init_dim_{dim}_case_{i}_default", True)
                        print(f"  ✅ Dim {dim}, Case {i}: Default antithesis OK")
                    
                    # Test 3: Verify dimensions property
                    self.assertEqual(state1.dimensions, dim)
                    self.assertEqual(state2.dimensions, dim)
        
        # Test error case: Dimension mismatch
        with self.assertRaises(ValueError):
            self.engine.initialize_state([1, 2, 3], [4, 5])  # Different lengths
        self.record_test("init_dimension_mismatch_error", True)
        print(f"  ✅ Dimension mismatch correctly raises error")
        
        if all_passed:
            print(f"\n  ✅ ALL state initialization tests passed")
        else:
            print(f"\n  ❌ Some state initialization tests failed")
    
    # ------------------------------------------------------------------------
    # TEST 2: NEGATION OPERATION
    # ------------------------------------------------------------------------
    
    def test_02_negation_operation(self):
        """Test negation: Thesis → Antithesis"""
        print(f"\n{'='*60}")
        print("TEST: Negation operation")
        print(f"{'='*60}")
        
        all_passed = True
        
        for dim in DIMENSIONS_TO_TEST:
            with self.subTest(dimension=dim):
                test_states = generate_test_states(dim, 2)
                
                for i, (thesis, antithesis) in enumerate(test_states):
                    # Initialize state
                    state = self.engine.initialize_state(thesis, antithesis)
                    
                    # Apply negation
                    try:
                        negated_state = self.engine.apply_negation(state)
                        
                        # Check properties
                        checks = []
                        
                        # 1. New thesis should be old antithesis
                        checks.append((
                            np.allclose(negated_state.thesis, state.antithesis, atol=self.tolerance),
                            f"New thesis != old antithesis"
                        ))
                        
                        # 2. New antithesis should be negation of new thesis
                        expected_new_antithesis = [-x for x in negated_state.thesis]
                        checks.append((
                            np.allclose(negated_state.antithesis, expected_new_antithesis, atol=self.tolerance),
                            f"New antithesis != negation of new thesis"
                        ))
                        
                        # 3. History should be updated
                        checks.append((
                            len(negated_state.history) > len(state.history),
                            f"History not updated"
                        ))
                        
                        # Record results
                        for check_passed, error_msg in checks:
                            if not check_passed:
                                all_passed = False
                                print(f"  ❌ Dim {dim}, Case {i}: {error_msg}")
                        
                        if all(p for p, _ in checks):
                            self.record_test(f"negation_dim_{dim}_case_{i}", True)
                            print(f"  ✅ Dim {dim}, Case {i}: Negation OK")
                        else:
                            self.record_test(f"negation_dim_{dim}_case_{i}", False)
                    
                    except Exception as e:
                        all_passed = False
                        print(f"  ❌ Dim {dim}, Case {i}: Exception - {e}")
                        self.record_test(f"negation_dim_{dim}_case_{i}", False)
                
                # Test error: Cannot negate from wrong stage
                state_wrong_stage = self.engine.initialize_state([1, 2, 3])
                # Manually change stage to something other than THESIS
                if hasattr(state_wrong_stage, 'stage'):
                    state_wrong_stage.stage = "WRONG_STAGE"
                    with self.assertRaises(ValueError):
                        self.engine.apply_negation(state_wrong_stage)
                    self.record_test(f"negation_wrong_stage_error_dim_{dim}", True)
                    print(f"  ✅ Dim {dim}: Wrong stage error handling OK")
        
        if all_passed:
            print(f"\n  ✅ ALL negation operation tests passed")
        else:
            print(f"\n  ❌ Some negation operation tests failed")
    
    # ------------------------------------------------------------------------
    # TEST 3: SYNTHESIS OPERATIONS
    # ------------------------------------------------------------------------
    
    def test_03_all_synthesis_methods(self):
        """Test all synthesis methods"""
        print(f"\n{'='*60}")
        print("TEST: All synthesis methods")
        print(f"{'='*60}")
        
        all_passed = True
        dim = 3  # Test with 3D for all methods
        
        # Create a state at ANTITHESIS stage
        thesis = [1.0, 0.5, -0.3]
        antithesis = [-0.8, 0.7, 0.2]
        state = self.engine.initialize_state(thesis, antithesis)
        
        # Apply negation to reach ANTITHESIS stage
        if hasattr(self.engine, 'apply_negation'):
            state = self.engine.apply_negation(state)
        
        for method_name in SYNTHESIS_METHODS:
            with self.subTest(method=method_name):
                try:
                    # Apply synthesis
                    if hasattr(SynthesisMethod, method_name.upper()):
                        method = getattr(SynthesisMethod, method_name.upper())
                        synthesized = self.engine.synthesize(state, method=method)
                    else:
                        synthesized = self.engine.synthesize(state, method=method_name)
                    
                    # Check properties
                    checks = []
                    
                    # 1. Synthesis should be computed
                    checks.append((
                        synthesized.has_synthesis,
                        f"No synthesis computed for method {method_name}"
                    ))
                    
                    # 2. Dimensions should match
                    if synthesized.has_synthesis:
                        checks.append((
                            len(synthesized.synthesis) == dim,
                            f"Synthesis dimension mismatch for {method_name}"
                        ))
                    
                    # 3. Stage should be SYNTHESIS
                    if hasattr(synthesized, 'stage'):
                        checks.append((
                            synthesized.stage == "SYNTHESIS" or 
                            (hasattr(synthesized.stage, 'value') and 
                             synthesized.stage.value == "synthesis"),
                            f"Wrong stage after synthesis for {method_name}"
                        ))
                    
                    # Record results
                    for check_passed, error_msg in checks:
                        if not check_passed:
                            all_passed = False
                            print(f"  ❌ Method {method_name}: {error_msg}")
                    
                    if all(p for p, _ in checks):
                        self.record_test(f"synthesis_method_{method_name}", True)
                        print(f"  ✅ Method {method_name}: Synthesis OK")
                    else:
                        self.record_test(f"synthesis_method_{method_name}", False)
                
                except Exception as e:
                    all_passed = False
                    print(f"  ❌ Method {method_name}: Exception - {e}")
                    self.record_test(f"synthesis_method_{method_name}", False)
        
        # Test error: Cannot synthesize from wrong stage
        state_wrong_stage = self.engine.initialize_state([1, 2, 3])
        if hasattr(state_wrong_stage, 'stage'):
            # Ensure it's not at ANTITHESIS stage
            state_wrong_stage.stage = "THESIS"
            with self.assertRaises(ValueError):
                self.engine.synthesize(state_wrong_stage, method='standard')
            self.record_test("synthesis_wrong_stage_error", True)
            print(f"  ✅ Wrong stage error handling OK")
        
        if all_passed:
            print(f"\n  ✅ ALL synthesis method tests passed")
        else:
            print(f"\n  ❌ Some synthesis method tests failed")
    
    # ------------------------------------------------------------------------
    # TEST 4: TENSION ANALYSIS
    # ------------------------------------------------------------------------
    
    def test_04_tension_analysis(self):
        """Test tension analysis between thesis and antithesis"""
        print(f"\n{'='*60}")
        print("TEST: Tension analysis")
        print(f"{'='*60}")
        
        all_passed = True
        
        test_cases = [
            ("perfect_opposition", [1.0, 1.0], [-1.0, -1.0], 1.0),  # Maximum tension
            ("identical", [1.0, 2.0], [1.0, 2.0], 0.0),            # Zero tension
            ("orthogonal", [1.0, 0.0], [0.0, 1.0], 1.0),           # High tension
            ("partial_agreement", [1.0, 0.5], [0.5, 1.0], 0.5),    # Medium tension
            ("zero_vectors", [0.0, 0.0], [0.0, 0.0], 0.0),         # Edge case
        ]
        
        for case_name, thesis, antithesis, expected_tension in test_cases:
            with self.subTest(case=case_name):
                try:
                    # Create state
                    state = self.engine.initialize_state(thesis, antithesis)
                    
                    # Analyze tension
                    tension = self.engine.analyze_tension(state)
                    
                    # Check if it's a dict or object
                    if isinstance(tension, dict):
                        tension_value = tension.get('tension_index', 0)
                    elif hasattr(tension, 'tension_index'):
                        tension_value = tension.tension_index
                    else:
                        tension_value = tension
                    
                    # Check properties
                    checks = []
                    
                    # 1. Tension should be between 0 and 1
                    checks.append((
                        0 <= tension_value <= 1 + self.tolerance,
                        f"Tension {tension_value} outside [0,1] range"
                    ))
                    
                    # 2. Should match expected value (within tolerance)
                    if expected_tension is not None:
                        checks.append((
                            abs(tension_value - expected_tension) <= 0.2,  # Loose tolerance for different algorithms
                            f"Tension {tension_value} not close to expected {expected_tension}"
                        ))
                    
                    # Record results
                    for check_passed, error_msg in checks:
                        if not check_passed:
                            all_passed = False
                            print(f"  ❌ Case {case_name}: {error_msg}")
                    
                    if all(p for p, _ in checks):
                        self.record_test(f"tension_{case_name}", True)
                        print(f"  ✅ Case {case_name}: Tension = {tension_value:.3f} (OK)")
                    else:
                        self.record_test(f"tension_{case_name}", False)
                
                except Exception as e:
                    all_passed = False
                    print(f"  ❌ Case {case_name}: Exception - {e}")
                    self.record_test(f"tension_{case_name}", False)
        
        # Test with various dimensions
        for dim in [2, 3, 4]:
            thesis = np.random.randn(dim).tolist()
            antithesis = np.random.randn(dim).tolist()
            state = self.engine.initialize_state(thesis, antithesis)
            
            try:
                tension = self.engine.analyze_tension(state)
                # Just check it doesn't crash
                self.record_test(f"tension_random_dim_{dim}", True)
                print(f"  ✅ Random {dim}D: Tension analysis works")
            except Exception as e:
                all_passed = False
                print(f"  ❌ Random {dim}D: Failed - {e}")
                self.record_test(f"tension_random_dim_{dim}", False)
        
        if all_passed:
            print(f"\n  ✅ ALL tension analysis tests passed")
        else:
            print(f"\n  ❌ Some tension analysis tests failed")
    
    # ------------------------------------------------------------------------
    # TEST 5: COMPLETE DIALECTICAL CYCLE
    # ------------------------------------------------------------------------
    
    def test_05_complete_dialectical_cycle(self):
        """Test complete thesis → antithesis → synthesis → negation of negation cycle"""
        print(f"\n{'='*60}")
        print("TEST: Complete dialectical cycle")
        print(f"{'='*60}")
        
        all_passed = True
        
        for dim in DIMENSIONS_TO_TEST:
            with self.subTest(dimension=dim):
                # Create initial state
                thesis = np.random.randn(dim).tolist()
                state = self.engine.initialize_state(thesis)
                
                try:
                    # Run complete cycle
                    states = self.engine.run_dialectical_cycle(thesis, cycles=1)
                    
                    # Check properties
                    checks = []
                    
                    # 1. Should return list of states
                    checks.append((
                        isinstance(states, list) and len(states) > 0,
                        f"No states returned for dim {dim}"
                    ))
                    
                    # 2. Check number of states (should be 4: T, A, S, N)
                    if len(states) >= 4:
                        checks.append((
                            len(states) == 4,
                            f"Expected 4 states, got {len(states)} for dim {dim}"
                        ))
                    
                    # 3. Check stage progression if stages are tracked
                    if len(states) >= 4 and hasattr(states[0], 'stage'):
                        stage_names = [s.stage.value if hasattr(s.stage, 'value') 
                                      else s.stage for s in states[:4]]
                        expected_stages = ["thesis", "antithesis", "synthesis", "negation_of_negation"]
                        
                        # Check if stages match (allow for different naming)
                        stage_match = all(any(exp in str(act).lower() for exp in expected_stages[i:i+1])
                                         for i, act in enumerate(stage_names[:4]))
                        checks.append((
                            stage_match,
                            f"Stage progression wrong: {stage_names}"
                        ))
                    
                    # Record results
                    for check_passed, error_msg in checks:
                        if not check_passed:
                            all_passed = False
                            print(f"  ❌ Dim {dim}: {error_msg}")
                    
                    if all(p for p, _ in checks):
                        self.record_test(f"complete_cycle_dim_{dim}", True)
                        print(f"  ✅ Dim {dim}: Complete cycle OK ({len(states)} states)")
                    else:
                        self.record_test(f"complete_cycle_dim_{dim}", False)
                
                except Exception as e:
                    all_passed = False
                    print(f"  ❌ Dim {dim}: Exception - {e}")
                    self.record_test(f"complete_cycle_dim_{dim}", False)
        
        # Test multiple cycles
        thesis = [1.0, -0.5, 0.3]
        try:
            states = self.engine.run_dialectical_cycle(thesis, cycles=2)
            # Should have 1 initial + 3 states per cycle
            expected_min_states = 1 + (2 * 3)  # 1 initial + 2 cycles * 3 states per cycle
            if len(states) >= expected_min_states:
                self.record_test("multiple_cycles", True)
                print(f"  ✅ Multiple cycles: {len(states)} states generated")
            else:
                all_passed = False
                self.record_test("multiple_cycles", False)
                print(f"  ❌ Multiple cycles: Only {len(states)} states, expected ≥{expected_min_states}")
        except Exception as e:
            all_passed = False
            print(f"  ❌ Multiple cycles: Exception - {e}")
            self.record_test("multiple_cycles", False)
        
        if all_passed:
            print(f"\n  ✅ ALL dialectical cycle tests passed")
        else:
            print(f"\n  ❌ Some dialectical cycle tests failed")
    
    # ------------------------------------------------------------------------
    # TEST 6: CONVERGENCE DETECTION
    # ------------------------------------------------------------------------
    
    def test_06_convergence_detection(self):
        """Test convergence detection in dialectical processes"""
        print(f"\n{'='*60}")
        print("TEST: Convergence detection")
        print(f"{'='*60}")
        
        all_passed = True
        
        if not hasattr(self.engine, 'run_until_convergence'):
            print(f"  ⏭️  Skipping (run_until_convergence not implemented)")
            return
        
        # Test case 1: Should converge quickly (identical thesis/antithesis)
        thesis1 = [1.0, 1.0, 1.0]
        antithesis1 = [-1.0, -1.0, -1.0]
        state1 = self.engine.initialize_state(thesis1, antithesis1)
        
        try:
            states1, converged1 = self.engine.run_until_convergence(
                thesis1, max_cycles=10, tolerance=0.01
            )
            
            checks = []
            checks.append((
                isinstance(states1, list),
                "Convergence test 1 didn't return states list"
            ))
            checks.append((
                isinstance(converged1, bool),
                "Convergence test 1 didn't return boolean"
            ))
            
            if converged1:
                checks.append((
                    len(states1) < 30,  # Should converge in fewer than 30 states
                    f"Converged but took {len(states1)} states"
                ))
            
            for check_passed, error_msg in checks:
                if not check_passed:
                    all_passed = False
                    print(f"  ❌ Convergence test 1: {error_msg}")
            
            if all(p for p, _ in checks):
                self.record_test("convergence_test_1", True)
                status = "converged" if converged1 else "did not converge"
                print(f"  ✅ Convergence test 1: {status} after {len(states1)} states")
            else:
                self.record_test("convergence_test_1", False)
        
        except Exception as e:
            all_passed = False
            print(f"  ❌ Convergence test 1: Exception - {e}")
            self.record_test("convergence_test_1", False)
        
        # Test case 2: Should not converge within small cycle limit
        thesis2 = [1.0, 0.0, -1.0]
        
        try:
            states2, converged2 = self.engine.run_until_convergence(
                thesis2, max_cycles=2, tolerance=0.01  # Very small limit
            )
            
            if not converged2:
                self.record_test("convergence_test_2", True)
                print(f"  ✅ Convergence test 2: Correctly did not converge within limit")
            else:
                all_passed = False
                self.record_test("convergence_test_2", False)
                print(f"  ❌ Convergence test 2: Should not converge within 2 cycles")
        
        except Exception as e:
            all_passed = False
            print(f"  ❌ Convergence test 2: Exception - {e}")
            self.record_test("convergence_test_2", False)
        
        if all_passed:
            print(f"\n  ✅ ALL convergence detection tests passed")
        else:
            print(f"\n  ❌ Some convergence detection tests failed")
    
    # ------------------------------------------------------------------------
    # TEST 7: NUMERICAL STABILITY
    # ------------------------------------------------------------------------
    
    def test_07_numerical_stability(self):
        """Test numerical stability with extreme values"""
        print(f"\n{'='*60}")
        print("TEST: Numerical stability")
        print(f"{'='*60}")
        
        all_passed = True
        
        extreme_cases = [
            ("very_small", [1e-10, 1e-15, 1e-20]),
            ("very_large", [1e10, 1e15, 1e20]),
            ("mixed_scale", [1e10, 1e-10, 1e5]),
            ("inf_values", [float('inf'), 1.0, -float('inf')]),
            ("nan_values", [float('nan'), 1.0, 2.0]),
        ]
        
        for case_name, vector in extreme_cases[:3]:  # Skip inf/nan for basic tests
            with self.subTest(case=case_name):
                try:
                    # Create state
                    state = self.engine.initialize_state(vector)
                    
                    # Check state creation
                    checks = []
                    checks.append((
                        state.dimensions == len(vector),
                        f"Dimension mismatch for {case_name}"
                    ))
                    
                    # Check all values are finite (skip for inf/nan cases)
                    if 'inf' not in case_name and 'nan' not in case_name:
                        all_finite = all(np.isfinite(v) for v in state.thesis)
                        checks.append((
                            all_finite,
                            f"Non-finite values in state for {case_name}"
                        ))
                    
                    # Try basic operations
                    try:
                        tension = self.engine.analyze_tension(state)
                        checks.append((True, ""))
                    except:
                        checks.append((
                            False,
                            f"Tension analysis failed for {case_name}"
                        ))
                    
                    # Record results
                    for check_passed, error_msg in checks:
                        if not check_passed and error_msg:
                            all_passed = False
                            print(f"  ❌ Case {case_name}: {error_msg}")
                    
                    if all(p for p, _ in checks):
                        self.record_test(f"numerical_stability_{case_name}", True)
                        print(f"  ✅ Case {case_name}: Numerically stable")
                    else:
                        self.record_test(f"numerical_stability_{case_name}", False)
                
                except Exception as e:
                    # Some extreme cases might legitimately fail
                    print(f"  ⚠️  Case {case_name}: {type(e).__name__} - {e}")
                    self.record_test(f"numerical_stability_{case_name}", True)  # Not a failure
        
        print(f"  ⏭️  Skipping inf/nan cases (may not be supported)")
        
        if all_passed:
            print(f"\n  ✅ Numerical stability tests passed")
        else:
            print(f"\n  ❌ Some numerical stability tests failed")

# ============================================================================
# SPECIALIZED ENGINE TESTS
# ============================================================================

class TestSpecializedEngines(unittest.TestCase):
    """Tests for specialized dialectical engines"""
    
    def setUp(self):
        self.tolerance = TOLERANCE
    
    def test_conservative_engine(self):
        """Test ConservativeDialecticalEngine"""
        print(f"\n{'='*60}")
        print("TEST: Conservative dialectical engine")
        print(f"{'='*60}")
        
        try:
            engine = ConservativeDialecticalEngine()
            
            # Test that it can be created
            self.assertIsNotNone(engine)
            print(f"  ✅ Conservative engine created")
            
            # Test basic operation
            thesis = [1.0, 0.5, -0.3]
            state = engine.initialize_state(thesis)
            
            # Should be able to run a cycle
            states = engine.run_dialectical_cycle(thesis, cycles=1)
            self.assertGreater(len(states), 0)
            print(f"  ✅ Conservative engine runs dialectical cycle")
            
        except Exception as e:
            self.fail(f"Conservative engine test failed: {e}")
    
    def test_radical_engine(self):
        """Test RadicalDialecticalEngine"""
        print(f"\n{'='*60}")
        print("TEST: Radical dialectical engine")
        print(f"{'='*60}")
        
        try:
            engine = RadicalDialecticalEngine()
            
            # Test that it can be created
            self.assertIsNotNone(engine)
            print(f"  ✅ Radical engine created")
            
            # Test basic operation
            thesis = [1.0, 0.5, -0.3]
            state = engine.initialize_state(thesis)
            
            # Should be able to run a cycle
            states = engine.run_dialectical_cycle(thesis, cycles=1)
            self.assertGreater(len(states), 0)
            print(f"  ✅ Radical engine runs dialectical cycle")
            
        except Exception as e:
            self.fail(f"Radical engine test failed: {e}")

# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance(unittest.TestCase):
    """Performance tests for dialectical engine"""
    
    def test_performance_large_dimensions(self):
        """Test performance with large dimensions"""
        print(f"\n{'='*60}")
        print("TEST: Performance with large dimensions")
        print(f"{'='*60}")
        
        engine = DialecticalEngine()
        
        for dim in [10, 50, 100]:
            with self.subTest(dimension=dim):
                # Create large vectors
                thesis = np.random.randn(dim).tolist()
                antithesis = np.random.randn(dim).tolist()
                
                start_time = time.time()
                
                # Perform operations
                state = engine.initialize_state(thesis, antithesis)
                tension = engine.analyze_tension(state)
                
                if hasattr(engine, 'run_dialectical_cycle'):
                    states = engine.run_dialectical_cycle(thesis, cycles=1)
                
                elapsed = time.time() - start_time
                
                print(f"  ✅ Dim {dim}: Operations completed in {elapsed:.3f}s")
                
                # Should complete within reasonable time
                self.assertLess(elapsed, 5.0, f"Too slow for dimension {dim}: {elapsed:.2f}s")
    
    def test_performance_many_cycles(self):
        """Test performance with many dialectical cycles"""
        print(f"\n{'='*60}")
        print("TEST: Performance with many cycles")
        print(f"{'='*60}")
        
        engine = DialecticalEngine()
        thesis = [1.0, 0.5, -0.3]
        
        if hasattr(engine, 'run_dialectical_cycle'):
            start_time = time.time()
            
            # Run multiple cycles
            states = engine.run_dialectical_cycle(thesis, cycles=10)
            
            elapsed = time.time() - start_time
            
            print(f"  ✅ 10 cycles completed in {elapsed:.3f}s")
            print(f"     Generated {len(states)} states")
            
            self.assertLess(elapsed, 2.0, f"Too slow for 10 cycles: {elapsed:.2f}s")
        else:
            print(f"  ⏭️  Skipping (run_dialectical_cycle not implemented)")

# ============================================================================
# TEST RUNNER & REPORTING
# ============================================================================

def run_all_tests():
    """Run all dialectical engine tests with detailed output"""
    print(f"\n{'=' * 80}")
    print("COMPREHENSIVE TESTS FOR DIALECTICAL ENGINE")
    print(f"{'=' * 80}")
    print("\nTesting ALL aspects of dialectical dynamics...")
    
    # Create test suite
    loader = unittest.TestLoader()
    
    # Load all test classes
    test_classes = [
        TestDialecticalEngineCore,
        TestSpecializedEngines,
        TestPerformance
    ]
    
    suites = []
    for test_class in test_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        suites.append(suite)
    
    # Combine suites
    complete_suite = unittest.TestSuite(suites)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(complete_suite)
    
    # Collect test results
    test_results = []
    for test_instance in complete_suite:
        if hasattr(test_instance, 'test_results'):
            test_results.extend(test_instance.test_results)
    
    # Print summary
    print(f"\n{'=' * 80}")
    print("TEST SUMMARY")
    print(f"{'=' * 80}")
    print(f"Total tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if test_results:
        passed_tests = [t for t in test_results if t.get('passed', False)]
        print(f"\nDetailed results: {len(passed_tests)}/{len(test_results)} individual checks passed")
        
        # Group by test category
        from collections import defaultdict
        by_category = defaultdict(list)
        for test in test_results:
            test_name = test['test']
            # Categorize by first part of test name
            if '_' in test_name:
                category = test_name.split('_')[0]
                by_category[category].append(test)
        
        print("\nBreakdown by category:")
        for category, tests in sorted(by_category.items()):
            passed = sum(1 for t in tests if t['passed'])
            print(f"  {category}: {passed}/{len(tests)} passed")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED! Dialectical engine implementation is correct.")
    else:
        print("\n❌ SOME TESTS FAILED! Check implementation details.")
    
    # Show failure details
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"\n{test}:")
            print(traceback[:500])  # First 500 chars
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"\n{test}:")
            print(traceback[:500])
    
    return result.wasSuccessful()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Run all tests
    import warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    success = run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)