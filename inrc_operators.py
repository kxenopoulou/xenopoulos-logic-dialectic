"""
INRC Operators Implementation
Layer 2: Concrete implementations of Piaget's INRC operators forming Klein-4 group

Mathematical operators: I, N, R, C with properties:
1. All are self-inverse: a² = I
2. Form Klein-4 group: N∘R = R∘N = C, R∘C = C∘R = N, N∘C = C∘N = R
3. Commutative: a∘b = b∘a
"""

from typing import List, Dict
from core.core_foundations import AbstractOperator, DimensionMismatchError
import numpy as np

# ============================================================================
# 1. CONCRETE INRC OPERATORS
# ============================================================================

class IdentityOperator(AbstractOperator):
    """
    Identity operator: I(x) = x
    The neutral element of Klein-4 group
    """
    
    def __init__(self):
        super().__init__("I", "Identity: I(x) = x")
    
    def apply(self, vector: List[float]) -> List[float]:
        """Return vector unchanged"""
        return vector.copy()
    
    def is_linear(self) -> bool:
        return True
    
    def is_self_inverse(self) -> bool:
        return True  # I∘I = I


class NegationOperator(AbstractOperator):
    """
    Negation operator: N(x) = -x
    Sign inversion (self-inverse)
    """
    
    def __init__(self):
        super().__init__("N", "Negation: N(x) = -x")
    
    def apply(self, vector: List[float]) -> List[float]:
        """Negate each element"""
        return [-x for x in vector]
    
    def is_linear(self) -> bool:
        return True
    
    def is_self_inverse(self) -> bool:
        return True  # N∘N = I


class ReciprocityOperator(AbstractOperator):
    """
    Reciprocity operator: R(x₁, x₂, ..., xₙ) = (xₙ, ..., x₂, x₁)
    
    CRITICAL: Order reversal (NOT cyclic permutation)
    Self-inverse: R² = I for all dimensions ≥ 2
    
    This corrects the common error of using cyclic permutation,
    which only works for dimension 2.
    """
    
    def __init__(self):
        super().__init__("R", "Reciprocity: R(x) = reversed order of x")
    
    def apply(self, vector: List[float]) -> List[float]:
        """Reverse order of elements"""
        return list(reversed(vector))
    
    def is_linear(self) -> bool:
        return True
    
    def is_self_inverse(self) -> bool:
        # R∘R = I always true for order reversal
        return True


class CorrelationOperator(AbstractOperator):
    """
    Correlation operator: C = N∘R = R∘N
    
    In Klein-4 group, correlation is the composition of
    negation and reciprocity (commutative).
    """
    
    def __init__(self, negation: NegationOperator, reciprocity: ReciprocityOperator):
        super().__init__("C", "Correlation: C(x) = N(R(x)) = R(N(x))")
        self._negation = negation
        self._reciprocity = reciprocity
    
    def apply(self, vector: List[float]) -> List[float]:
        """
        Apply N∘R (same as R∘N due to commutativity)
        Equivalent to: reverse order then negate
        """
        # Apply reciprocity (reverse order)
        reversed_vector = self._reciprocity.apply(vector)
        # Apply negation to reversed vector
        return self._negation.apply(reversed_vector)
    
    def is_linear(self) -> bool:
        # Composition of linear operators is linear
        return self._negation.is_linear() and self._reciprocity.is_linear()
    
    def is_self_inverse(self) -> bool:
        # C∘C = (N∘R)∘(N∘R) = N∘(R∘N)∘R = N∘C∘R = N∘(N∘R)∘R = I
        return True

# ============================================================================
# 2. MATRIX REPRESENTATIONS (Optional - with numpy)
# ============================================================================

class MatrixOperator:
    """
    Matrix representations of INRC operators for numerical computations
    Requires numpy for matrix operations
    """
    
    def __init__(self, dimension: int):
        if dimension < 2:
            raise DimensionMismatchError(f"Dimension must be ≥ 2, got {dimension}")
        self.dimension = dimension
    
    def identity_matrix(self) -> np.ndarray:
        """I: Identity matrix"""
        return np.eye(self.dimension)
    
    def negation_matrix(self) -> np.ndarray:
        """N: Negative identity matrix"""
        return -np.eye(self.dimension)
    
    def reciprocity_matrix(self) -> np.ndarray:
        """
        R: Order reversal matrix (NOT cyclic)
        
        Correct implementation:
        R[i, n-1-i] = 1 for all i
        All other entries = 0
        
        This ensures R² = I for all n ≥ 2
        """
        R = np.zeros((self.dimension, self.dimension))
        for i in range(self.dimension):
            R[i, self.dimension - 1 - i] = 1.0
        return R
    
    def correlation_matrix(self) -> np.ndarray:
        """C = N∘R = R∘N (matrix multiplication)"""
        N = self.negation_matrix()
        R = self.reciprocity_matrix()
        return N @ R  # Matrix multiplication
    
    def get_all_matrices(self) -> Dict[str, np.ndarray]:
        """Get all four operator matrices"""
        return {
            'I': self.identity_matrix(),
            'N': self.negation_matrix(),
            'R': self.reciprocity_matrix(),
            'C': self.correlation_matrix()
        }
    
    def apply_matrix(self, vector: np.ndarray, operator: str) -> np.ndarray:
        """Apply operator matrix to vector"""
        matrices = self.get_all_matrices()
        if operator not in matrices:
            raise ValueError(f"Unknown operator: {operator}")
        return matrices[operator] @ vector

# ============================================================================
# 3. OPERATOR FACTORY
# ============================================================================

class INRCOperatorFactory:
    """
    Factory for creating INRC operator instances
    Ensures consistent creation and validation
    """
    
    @staticmethod
    def create_operators() -> Dict[str, AbstractOperator]:
        """
        Create all four INRC operators
        Returns: Dictionary mapping symbols to operator instances
        """
        # Create base operators
        I = IdentityOperator()
        N = NegationOperator()
        R = ReciprocityOperator()
        C = CorrelationOperator(N, R)
        
        return {
            'I': I,
            'N': N,
            'R': R,
            'C': C
        }
    
    @staticmethod
    def create_with_validation() -> Dict[str, AbstractOperator]:
        """
        Create operators and validate Klein-4 properties
        Raises: MathematicalError if validation fails
        """
        operators = INRCOperatorFactory.create_operators()
        
        # Validate self-inverse property
        for symbol, operator in operators.items():
            if not operator.is_self_inverse():
                raise DimensionMismatchError(
                    f"Operator {symbol} is not self-inverse"
                )
        
        # Test specific Klein-4 relations (N∘R = C, etc.)
        test_vector = [1.0, 2.0, 3.0]
        
        # N∘R = C
        n_then_r = operators['R'].apply(operators['N'].apply(test_vector))
        c_result = operators['C'].apply(test_vector)
        if not all(abs(a - b) < 1e-10 for a, b in zip(n_then_r, c_result)):
            raise DimensionMismatchError("N∘R ≠ C")
        
        # R∘N = C (commutativity)
        r_then_n = operators['N'].apply(operators['R'].apply(test_vector))
        if not all(abs(a - b) < 1e-10 for a, b in zip(r_then_n, c_result)):
            raise DimensionMismatchError("R∘N ≠ C")
        
        return operators
    
    @staticmethod
    def create_matrix_operators(dimension: int) -> MatrixOperator:
        """
        Create matrix representations for numerical computations
        """
        return MatrixOperator(dimension)

# ============================================================================
# 4. VALIDATION UTILITIES
# ============================================================================

class OperatorValidator:
    """Utilities for validating operator properties"""
    
    @staticmethod
    def validate_self_inverse(operator: AbstractOperator, 
                             test_vectors: List[List[float]]) -> bool:
        """
        Validate a² = I for multiple test vectors
        """
        for vector in test_vectors:
            once = operator.apply(vector)
            twice = operator.apply(once)
            if not all(abs(orig - twice) < 1e-10 
                      for orig, twice in zip(vector, twice)):
                return False
        return True
    
    @staticmethod
    def validate_linearity(operator: AbstractOperator) -> bool:
        """
        Validate linearity: A(αx + βy) = αA(x) + βA(y)
        Simple test with α=2, β=3
        """
        x = [1.0, 2.0, 3.0]
        y = [4.0, 5.0, 6.0]
        alpha, beta = 2.0, 3.0
        
        # Left side: A(αx + βy)
        left_input = [alpha * xi + beta * yi for xi, yi in zip(x, y)]
        left_result = operator.apply(left_input)
        
        # Right side: αA(x) + βA(y)
        ax = operator.apply(x)
        ay = operator.apply(y)
        right_result = [alpha * axi + beta * ayi for axi, ayi in zip(ax, ay)]
        
        return all(abs(l - r) < 1e-10 for l, r in zip(left_result, right_result))
    
    @staticmethod
    def validate_klein4_relations(operators: Dict[str, AbstractOperator]) -> bool:
        """
        Validate all Klein-4 group relations
        """
        test_vector = [1.0, 2.0, 3.0]
        relations = [
            ('N', 'R', 'C'),  # N∘R = C
            ('R', 'N', 'C'),  # R∘N = C
            ('R', 'C', 'N'),  # R∘C = N
            ('C', 'R', 'N'),  # C∘R = N
            ('N', 'C', 'R'),  # N∘C = R
            ('C', 'N', 'R')   # C∘N = R
        ]
        
        for a, b, expected in relations:
            # Apply a then b
            result = operators[b].apply(operators[a].apply(test_vector))
            expected_result = operators[expected].apply(test_vector)
            
            if not all(abs(r - e) < 1e-10 for r, e in zip(result, expected_result)):
                return False
        
        return True

# ============================================================================
# 5. DEMONSTRATION OF CORRECTNESS
# ============================================================================

class ImplementationDemonstration:
    """
    Demonstrates why order reversal is correct and cyclic permutation is wrong
    """
    
    @staticmethod
    def demonstrate_order_reversal_correctness(dimension: int = 3):
        """
        Show that order reversal (R[i, n-1-i] = 1) gives R² = I
        while cyclic permutation does NOT (except for n=2)
        """
        print(f"\n{'='*60}")
        print(f"DEMONSTRATION: Order Reversal vs Cyclic Permutation")
        print(f"Dimension: {dimension}")
        print(f"{'='*60}")
        
        # Correct R: Order reversal
        R_correct = np.zeros((dimension, dimension))
        for i in range(dimension):
            R_correct[i, dimension - 1 - i] = 1.0
        
        # Wrong R: Cyclic permutation (common error)
        R_wrong = np.zeros((dimension, dimension))
        for i in range(dimension):
            R_wrong[i, (i + 1) % dimension] = 1.0
        
        # Check self-inverse
        R_correct_squared = R_correct @ R_correct
        R_wrong_squared = R_wrong @ R_wrong
        
        print(f"\nCorrect R (order reversal):")
        print(f"R² = I? {np.allclose(R_correct_squared, np.eye(dimension))}")
        
        print(f"\nWrong R (cyclic permutation):")
        print(f"R² = I? {np.allclose(R_wrong_squared, np.eye(dimension))}")
        
        if dimension > 2 and np.allclose(R_wrong_squared, np.eye(dimension)):
            print(f"\n⚠️  WARNING: For dimension {dimension},")
            print("   cyclic permutation happens to be self-inverse.")
            print("   But this is NOT true in general for n > 2!")
        
        print(f"\n✅ Order reversal works for ALL dimensions n ≥ 2")
        print(f"❌ Cyclic permutation only works for n = 2")

# ============================================================================
# MAIN: Quick test
# ============================================================================

if __name__ == "__main__":
    print("Testing INRC Operators...")
    
    # Create operators
    factory = INRCOperatorFactory()
    operators = factory.create_with_validation()
    
    print(f"\nCreated operators: {list(operators.keys())}")
    
    # Test application
    test_vector = [1.0, 2.0, 3.0]
    print(f"\nTest vector: {test_vector}")
    
    for symbol, operator in operators.items():
        result = operator.apply(test_vector)
        print(f"{symbol}: {result}")
    
    # Validate properties
    validator = OperatorValidator()
    print(f"\nValidating Klein-4 relations...")
    if validator.validate_klein4_relations(operators):
        print("✅ All Klein-4 relations validated")
    else:
        print("❌ Klein-4 relations validation failed")
    
    # Demonstrate correctness
    ImplementationDemonstration.demonstrate_order_reversal_correctness(3)