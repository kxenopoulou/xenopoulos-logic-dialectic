"""
Core Mathematical Foundations
Pure mathematical abstractions with NO external dependencies
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Dict, List, Tuple, Any
from enum import Enum
from dataclasses import dataclass
import math

# ============================================================================
# 1. ENUMS & CONSTANTS
# ============================================================================

class DialecticalStage(Enum):
    """Stages in Hegelian dialectical process"""
    THESIS = "thesis"
    ANTITHESIS = "antithesis" 
    SYNTHESIS = "synthesis"
    NEGATION_OF_NEGATION = "negation_of_negation"

class GroupProperty(Enum):
    """Mathematical group properties"""
    CLOSURE = "closure"
    ASSOCIATIVITY = "associativity"
    IDENTITY = "identity"
    INVERSES = "inverses"
    COMMUTATIVITY = "commutativity"
    SELF_INVERSE = "self_inverse"

# ============================================================================
# 2. PROTOCOLS (Interfaces)
# ============================================================================

@runtime_checkable
class MathematicalOperator(Protocol):
    """Protocol for mathematical operators"""
    @property
    def symbol(self) -> str: ...
    
    @property 
    def description(self) -> str: ...
    
    def apply(self, vector: List[float]) -> List[float]: ...
    
    def is_linear(self) -> bool: ...
    
    def is_self_inverse(self) -> bool: ...

@runtime_checkable
class MathematicalGroup(Protocol):
    """Protocol for mathematical groups"""
    def is_group(self) -> bool: ...
    
    def get_elements(self) -> List[str]: ...
    
    def compose(self, a: str, b: str) -> str: ...
    
    def inverse(self, element: str) -> str: ...
    
    def identity(self) -> str: ...

# ============================================================================
# 3. ABSTRACT BASE CLASSES
# ============================================================================

class AbstractGroup(ABC):
    """Abstract base class for mathematical groups"""
    
    @abstractmethod
    def is_group(self) -> bool:
        """Verify all group axioms"""
        pass
    
    @abstractmethod
    def get_elements(self) -> List[str]:
        """Get all group elements"""
        pass
    
    @abstractmethod
    def compose(self, a: str, b: str) -> str:
        """Compose two group elements: a ∘ b"""
        pass
    
    @abstractmethod
    def inverse(self, element: str) -> str:
        """Get inverse of element"""
        pass
    
    @abstractmethod
    def identity(self) -> str:
        """Get identity element"""
        pass

class AbstractOperator(ABC):
    """Abstract base class for mathematical operators"""
    
    def __init__(self, symbol: str, description: str):
        self._symbol = symbol
        self._description = description
    
    @property
    def symbol(self) -> str:
        return self._symbol
    
    @property
    def description(self) -> str:
        return self._description
    
    @abstractmethod
    def apply(self, vector: List[float]) -> List[float]:
        """Apply operator to vector"""
        pass
    
    @abstractmethod
    def is_linear(self) -> bool:
        """Check if operator is linear"""
        pass
    
    def is_self_inverse(self) -> bool:
        """Check if operator is self-inverse: A² = I"""
        # Default implementation can be overridden
        test_vector = [1.0, 2.0, 3.0]
        once = self.apply(test_vector)
        twice = self.apply(once)
        return all(abs(orig - twice) < 1e-10 
                  for orig, twice in zip(test_vector, twice))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AbstractOperator):
            return False
        return self.symbol == other.symbol
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.symbol})"

# ============================================================================
# 4. DATA CLASSES (Value Objects)
# ============================================================================

@dataclass
class DialecticalTransition:
    """Represents a transition in dialectical process"""
    from_stage: DialecticalStage
    to_stage: DialecticalStage
    transformation: str  # Which operator caused the transition
    parameters: Dict[str, float]
    
    def describe(self) -> str:
        return f"{self.from_stage.value} → {self.to_stage.value} via {self.transformation}"

@dataclass
class GroupValidationResult:
    """Result of group validation"""
    is_group: bool
    properties: Dict[GroupProperty, bool]
    errors: List[str]
    
    def all_valid(self) -> bool:
        return all(self.properties.values()) and len(self.errors) == 0
    
    def get_failed_properties(self) -> List[GroupProperty]:
        return [prop for prop, valid in self.properties.items() if not valid]

@dataclass
class VectorTransformation:
    """Result of vector transformation"""
    original: List[float]
    transformed: List[float]
    operator_symbol: str
    operator_description: str
    
    def difference_norm(self) -> float:
        """Calculate Euclidean distance between original and transformed"""
        if len(self.original) != len(self.transformed):
            return float('inf')
        return math.sqrt(sum((o - t) ** 2 for o, t in zip(self.original, self.transformed)))

# ============================================================================
# 5. MATHEMATICAL UTILITIES (Pure Functions)
# ============================================================================

class MathUtils:
    """Pure mathematical utility functions (no state)"""
    
    @staticmethod
    def vectors_equal(v1: List[float], v2: List[float], 
                     tolerance: float = 1e-10) -> bool:
        """Compare vectors with tolerance"""
        if len(v1) != len(v2):
            return False
        return all(abs(a - b) <= tolerance for a, b in zip(v1, v2))
    
    @staticmethod
    def is_identity_matrix(matrix: List[List[float]], 
                          tolerance: float = 1e-10) -> bool:
        """Check if matrix is identity within tolerance"""
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                expected = 1.0 if i == j else 0.0
                if abs(matrix[i][j] - expected) > tolerance:
                    return False
        return True
    
    @staticmethod
    def validate_closure(elements: List[str], 
                        compose_func: callable,
                        tolerance: float = 1e-10) -> bool:
        """Validate closure property for a group"""
        for a in elements:
            for b in elements:
                result = compose_func(a, b)
                if result not in elements:
                    return False
        return True
    
    @staticmethod
    def validate_associativity(elements: List[str],
                             apply_func: callable,
                             tolerance: float = 1e-10) -> bool:
        """Validate associativity: (a∘b)∘c = a∘(b∘c)"""
        test_vector = [1.0, 2.0, 3.0][:len(elements)]
        for a in elements:
            for b in elements:
                for c in elements:
                    left = apply_func(apply_func(test_vector, a), b)
                    left = apply_func(left, c)
                    right = apply_func(test_vector, a)
                    right = apply_func(right, b)
                    right = apply_func(right, c)
                    if not MathUtils.vectors_equal(left, right, tolerance):
                        return False
        return True

# ============================================================================
# 6. EXCEPTIONS (Domain-specific)
# ============================================================================

class MathematicalError(Exception):
    """Base exception for mathematical errors"""
    pass

class GroupAxiomViolation(MathematicalError):
    """Raised when group axiom is violated"""
    def __init__(self, axiom: str, details: str = ""):
        self.axiom = axiom
        self.details = details
        super().__init__(f"Group axiom violation: {axiom}. {details}")

class OperatorApplicationError(MathematicalError):
    """Raised when operator application fails"""
    pass

class DimensionMismatchError(MathematicalError):
    """Raised when dimensions don't match"""
    pass

# ============================================================================
# 7. CONSTANTS & CONFIGURATION
# ============================================================================

class MathematicalConstants:
    """Mathematical constants used throughout the system"""
    
    # Tolerances for numerical comparisons
    DEFAULT_TOLERANCE = 1e-10
    STRICT_TOLERANCE = 1e-14
    LOOSE_TOLERANCE = 1e-6
    
    # Standard test vectors (various dimensions)
    TEST_VECTORS = {
        2: [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]],
        3: [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        4: [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], 
            [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    }
    
    # Klein-4 group properties (mathematical truths)
    KLEIN4_RELATIONS = [
        ('N', 'R', 'C'),  # N∘R = C
        ('R', 'N', 'C'),  # R∘N = C
        ('R', 'C', 'N'),  # R∘C = N
        ('C', 'R', 'N'),  # C∘R = N
        ('N', 'C', 'R'),  # N∘C = R
        ('C', 'N', 'R')   # C∘N = R
    ]