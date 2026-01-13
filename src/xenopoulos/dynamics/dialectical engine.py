"""
Dialectical Engine
Layer 3: Core business logic for Hegelian dialectical processes using INRC operators
Pure dialectical dynamics without I/O or external dependencies
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import math
from core.core_foundations import (
    DialecticalStage, 
    DialecticalTransition,
    DimensionMismatchError
)
from operators.inrc_operators import INRCOperatorFactory

# ============================================================================
# 1. DATA STRUCTURES
# ============================================================================

@dataclass
class DialecticalState:
    """Complete state of dialectical process at a moment in time"""
    thesis: List[float]
    antithesis: List[float]
    synthesis: Optional[List[float]] = None
    stage: DialecticalStage = DialecticalStage.THESIS
    history: List[DialecticalTransition] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate state on creation"""
        if len(self.thesis) != len(self.antithesis):
            raise DimensionMismatchError(
                f"Thesis dimension {len(self.thesis)} != "
                f"Antithesis dimension {len(self.antithesis)}"
            )
    
    @property
    def dimensions(self) -> int:
        """Dimension of the state space"""
        return len(self.thesis)
    
    @property
    def has_synthesis(self) -> bool:
        """Check if synthesis has been computed"""
        return self.synthesis is not None
    
    def to_dict(self) -> Dict:
        """Convert to serializable dictionary"""
        return {
            'thesis': self.thesis,
            'antithesis': self.antithesis,
            'synthesis': self.synthesis,
            'stage': self.stage.value,
            'dimensions': self.dimensions,
            'history': [t.describe() for t in self.history],
            'metadata': self.metadata
        }


class SynthesisMethod(Enum):
    """Methods for computing synthesis from thesis and antithesis"""
    STANDARD = "standard"      # Linear combination
    GEOMETRIC = "geometric"    # Geometric mean
    DIALECTICAL = "dialectical" # Using INRC operators
    HARMONIC = "harmonic"      # Harmonic mean
    MAX_TENSION = "max_tension" # Emphasize differences
    MIN_TENSION = "min_tension" # Minimize differences


@dataclass  
class TensionMetrics:
    """Quantitative metrics of dialectical tension"""
    mean_difference: float      # Mean absolute difference
    max_difference: float       # Maximum absolute difference
    mean_similarity: float      # Mean absolute sum (common ground)
    tension_index: float        # Normalized tension [0, 1]
    correlation: float          # Correlation coefficient
    entropy: float              # Information-theoretic divergence
    
    def to_dict(self) -> Dict:
        return {k: v for k, v in self.__dict__.items()}


# ============================================================================
# 2. CORE DIALECTICAL ENGINE
# ============================================================================

class DialecticalEngine:
    """
    Core engine implementing Hegelian dialectics using Klein-4 group
    
    Business logic only - no I/O, no visualization, no persistence
    Pure functions operating on DialecticalState objects
    """
    
    def __init__(self, operators_factory: Optional[INRCOperatorFactory] = None):
        """
        Initialize engine with optional custom operators
        
        Args:
            operators_factory: Factory for INRC operators.
                              If None, uses default factory.
        """
        self.operators_factory = operators_factory or INRCOperatorFactory()
        self.operators = self.operators_factory.create_with_validation()
        self.state_history: List[DialecticalState] = []
    
    # ------------------------------------------------------------------------
    # STATE INITIALIZATION
    # ------------------------------------------------------------------------
    
    def initialize_state(self, 
                        thesis: List[float],
                        antithesis: Optional[List[float]] = None,
                        metadata: Optional[Dict] = None) -> DialecticalState:
        """
        Initialize new dialectical state
        
        Args:
            thesis: Initial thesis vector
            antithesis: Antithesis vector. If None, computes as N(thesis)
            metadata: Optional metadata for the state
            
        Returns:
            Initialized DialecticalState
        """
        if antithesis is None:
            # Default antithesis: negation of thesis
            antithesis = self.operators['N'].apply(thesis)
        
        state = DialecticalState(
            thesis=thesis,
            antithesis=antithesis,
            stage=DialecticalStage.THESIS,
            metadata=metadata or {}
        )
        
        self.state_history.append(state)
        return state
    
    # ------------------------------------------------------------------------
    # DIALECTICAL TRANSITIONS
    # ------------------------------------------------------------------------
    
    def apply_negation(self, 
                      state: DialecticalState,
                      intensity: float = 1.0) -> DialecticalState:
        """
        Apply negation: Thesis → Antithesis
        
        In dialectics, the antithesis emerges from negating the thesis.
        This creates the fundamental contradiction.
        
        Args:
            state: Current dialectical state (must be THESIS stage)
            intensity: Strength of negation [0, 1]
            
        Returns:
            New state at ANTITHESIS stage
        """
        if state.stage != DialecticalStage.THESIS:
            raise ValueError(
                f"Can only apply negation from THESIS stage, "
                f"current stage: {state.stage}"
            )
        
        # New thesis becomes old antithesis
        new_thesis = state.antithesis
        
        # New antithesis emerges from negating new thesis
        # With intensity modulation
        base_antithesis = self.operators['N'].apply(new_thesis)
        new_antithesis = self._apply_intensity(
            base_antithesis, new_thesis, intensity
        )
        
        new_state = DialecticalState(
            thesis=new_thesis,
            antithesis=new_antithesis,
            stage=DialecticalStage.ANTITHESIS,
            history=state.history.copy(),
            metadata=state.metadata.copy()
        )
        
        # Record transition
        transition = DialecticalTransition(
            from_stage=DialecticalStage.THESIS,
            to_stage=DialecticalStage.ANTITHESIS,
            transformation='negation',
            parameters={'intensity': intensity, 'operator': 'N'}
        )
        new_state.history.append(transition)
        
        self.state_history.append(new_state)
        return new_state
    
    def synthesize(self,
                  state: DialecticalState,
                  method: SynthesisMethod = SynthesisMethod.DIALECTICAL,
                  parameters: Optional[Dict] = None) -> DialecticalState:
        """
        Synthesize thesis and antithesis
        
        The synthesis preserves what is rational in both thesis and antithesis
        while transcending their contradiction.
        
        Args:
            state: Current state (must be ANTITHESIS stage)
            method: Synthesis method
            parameters: Method-specific parameters
            
        Returns:
            New state at SYNTHESIS stage
        """
        if state.stage != DialecticalStage.ANTITHESIS:
            raise ValueError(
                f"Can only synthesize from ANTITHESIS stage, "
                f"current stage: {state.stage}"
            )
        
        parameters = parameters or {}
        
        # Compute synthesis based on method
        if method == SynthesisMethod.STANDARD:
            synthesis = self._standard_synthesis(
                state.thesis, state.antithesis, parameters
            )
        elif method == SynthesisMethod.GEOMETRIC:
            synthesis = self._geometric_synthesis(
                state.thesis, state.antithesis, parameters
            )
        elif method == SynthesisMethod.DIALECTICAL:
            synthesis = self._dialectical_synthesis(
                state.thesis, state.antithesis, parameters
            )
        elif method == SynthesisMethod.HARMONIC:
            synthesis = self._harmonic_synthesis(
                state.thesis, state.antithesis, parameters
            )
        elif method == SynthesisMethod.MAX_TENSION:
            synthesis = self._max_tension_synthesis(
                state.thesis, state.antithesis, parameters
            )
        elif method == SynthesisMethod.MIN_TENSION:
            synthesis = self._min_tension_synthesis(
                state.thesis, state.antithesis, parameters
            )
        else:
            raise ValueError(f"Unknown synthesis method: {method}")
        
        new_state = DialecticalState(
            thesis=state.thesis,
            antithesis=state.antithesis,
            synthesis=synthesis,
            stage=DialecticalStage.SYNTHESIS,
            history=state.history.copy(),
            metadata=state.metadata.copy()
        )
        
        # Record transition
        transition = DialecticalTransition(
            from_stage=DialecticalStage.ANTITHESIS,
            to_stage=DialecticalStage.SYNTHESIS,
            transformation=f'synthesis_{method.value}',
            parameters={'method': method.value, **parameters}
        )
        new_state.history.append(transition)
        
        self.state_history.append(new_state)
        return new_state
    
    def negate_negation(self,
                       state: DialecticalState,
                       preserve_history: bool = True) -> DialecticalState:
        """
        Negation of negation: Synthesis → New Thesis
        
        The synthesis becomes the new thesis, beginning a new dialectical cycle
        at a higher level of development (Aufhebung).
        
        Args:
            state: Current state (must be SYNTHESIS stage)
            preserve_history: Whether to keep previous thesis/antithesis in metadata
            
        Returns:
            New state at NEGATION_OF_NEGATION stage
        """
        if state.stage != DialecticalStage.SYNTHESIS:
            raise ValueError(
                f"Can only negate negation from SYNTHESIS stage, "
                f"current stage: {state.stage}"
            )
        
        if not state.has_synthesis:
            raise ValueError("Cannot negate negation without synthesis")
        
        # New thesis emerges from synthesis
        new_thesis = state.synthesis
        
        # New antithesis: negation of new thesis
        new_antithesis = self.operators['N'].apply(new_thesis)
        
        # Prepare metadata
        metadata = state.metadata.copy()
        if preserve_history:
            metadata['previous_thesis'] = state.thesis
            metadata['previous_antithesis'] = state.antithesis
            metadata['previous_synthesis'] = state.synthesis
        
        new_state = DialecticalState(
            thesis=new_thesis,
            antithesis=new_antithesis,
            stage=DialecticalStage.NEGATION_OF_NEGATION,
            history=state.history.copy(),
            metadata=metadata
        )
        
        # Record transition
        transition = DialecticalTransition(
            from_stage=DialecticalStage.SYNTHESIS,
            to_stage=DialecticalStage.NEGATION_OF_NEGATION,
            transformation='negation_of_negation',
            parameters={'preserve_history': preserve_history}
        )
        new_state.history.append(transition)
        
        self.state_history.append(new_state)
        return new_state
    
    # ------------------------------------------------------------------------
    # SYNTHESIS METHODS (Implementation)
    # ------------------------------------------------------------------------
    
    def _standard_synthesis(self,
                          thesis: List[float],
                          antithesis: List[float],
                          parameters: Dict) -> List[float]:
        """
        Standard synthesis: Linear combination
        
        S = α·thesis + β·antithesis
        Default: α=0.7, β=0.3 (thesis-weighted)
        """
        alpha = parameters.get('alpha', 0.7)
        beta = parameters.get('beta', 0.3)
        
        # Normalize weights
        total = alpha + beta
        alpha, beta = alpha/total, beta/total
        
        return [
            alpha * t + beta * a
            for t, a in zip(thesis, antithesis)
        ]
    
    def _geometric_synthesis(self,
                           thesis: List[float],
                           antithesis: List[float],
                           parameters: Dict) -> List[float]:
        """
        Geometric synthesis: Geometric mean preserving sign
        
        S = sign(t·a) · sqrt(|t·a|)
        Emphasizes multiplicative relationships
        """
        epsilon = parameters.get('epsilon', 1e-10)  # Avoid division by zero
        
        synthesis = []
        for t, a in zip(thesis, antithesis):
            product = t * a
            if abs(product) < epsilon:
                synthesis.append(0.0)
            else:
                sign = 1 if product >= 0 else -1
                magnitude = math.sqrt(abs(product))
                synthesis.append(sign * magnitude)
        
        return synthesis
    
    def _dialectical_synthesis(self,
                             thesis: List[float],
                             antithesis: List[float],
                             parameters: Dict) -> List[float]:
        """
        Dialectical synthesis: Using INRC operators
        
        Applies correlation operator to thesis, then blends with antithesis
        Incorporates both transformation and preservation
        """
        # Apply correlation operator to thesis
        transformed_thesis = self.operators['C'].apply(thesis)
        
        # Blend transformed thesis with antithesis
        blend_weight = parameters.get('blend_weight', 0.5)
        
        return [
            blend_weight * tt + (1 - blend_weight) * a
            for tt, a in zip(transformed_thesis, antithesis)
        ]
    
    def _harmonic_synthesis(self,
                          thesis: List[float],
                          antithesis: List[float],
                          parameters: Dict) -> List[float]:
        """
        Harmonic synthesis: Harmonic mean
        
        S = 2·t·a / (t + a) for t + a ≠ 0
        Emphasizes balance and mutual adjustment
        """
        epsilon = parameters.get('epsilon', 1e-10)
        
        synthesis = []
        for t, a in zip(thesis, antithesis):
            denominator = t + a
            if abs(denominator) < epsilon:
                synthesis.append(0.0)
            else:
                synthesis.append(2 * t * a / denominator)
        
        return synthesis
    
    def _max_tension_synthesis(self,
                             thesis: List[float],
                             antithesis: List[float],
                             parameters: Dict) -> List[float]:
        """
        Maximum tension synthesis: Emphasizes differences
        
        S = sign(t - a) · max(|t|, |a|)
        Preserves maximum magnitude with sign of difference
        """
        synthesis = []
        for t, a in zip(thesis, antithesis):
            if abs(t) > abs(a):
                synthesis.append(t)
            else:
                synthesis.append(a)
        
        return synthesis
    
    def _min_tension_synthesis(self,
                             thesis: List[float],
                             antithesis: List[float],
                             parameters: Dict) -> List[float]:
        """
        Minimum tension synthesis: Compromise
        
        S = (t + a) / 2
        Simple average minimizing conflict
        """
        return [(t + a) / 2 for t, a in zip(thesis, antithesis)]
    
    # ------------------------------------------------------------------------
    # TENSION ANALYSIS
    # ------------------------------------------------------------------------
    
    def analyze_tension(self, state: DialecticalState) -> TensionMetrics:
        """
        Analyze dialectical tension between thesis and antithesis
        
        Provides quantitative metrics of conflict, similarity,
        and potential for synthesis.
        """
        n = state.dimensions
        if n == 0:
            return TensionMetrics(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        
        # Calculate differences and similarities
        differences = [abs(t - a) for t, a in zip(state.thesis, state.antithesis)]
        similarities = [abs(t + a) for t, a in zip(state.thesis, state.antithesis)]
        
        # Basic statistics
        mean_diff = sum(differences) / n
        max_diff = max(differences)
        mean_sim = sum(similarities) / n
        
        # Tension index: normalized mean difference
        max_possible_diff = sum(abs(t) + abs(a) 
                               for t, a in zip(state.thesis, state.antithesis))
        tension_index = (sum(differences) / max_possible_diff) if max_possible_diff > 0 else 0
        
        # Correlation
        if n > 1:
            mean_t = sum(state.thesis) / n
            mean_a = sum(state.antithesis) / n
            
            cov = sum((t - mean_t) * (a - mean_a) 
                     for t, a in zip(state.thesis, state.antithesis)) / n
            var_t = sum((t - mean_t) ** 2 for t in state.thesis) / n
            var_a = sum((a - mean_a) ** 2 for a in state.antithesis) / n
            
            if var_t > 0 and var_a > 0:
                correlation = cov / math.sqrt(var_t * var_a)
            else:
                correlation = 0.0
        else:
            correlation = 0.0
        
        # Entropy (information-theoretic divergence)
        # Simple approximation using normalized differences
        normalized_diffs = [d / (abs(t) + abs(a) + 1e-10) 
                          for d, t, a in zip(differences, state.thesis, state.antithesis)]
        entropy = -sum(p * math.log(p + 1e-10) for p in normalized_diffs if p > 0)
        
        return TensionMetrics(
            mean_difference=mean_diff,
            max_difference=max_diff,
            mean_similarity=mean_sim,
            tension_index=tension_index,
            correlation=correlation,
            entropy=entropy
        )
    
    # ------------------------------------------------------------------------
    # COMPLETE PROCESSES
    # ------------------------------------------------------------------------
    
    def run_dialectical_cycle(self,
                             initial_thesis: List[float],
                             cycles: int = 1,
                             synthesis_method: SynthesisMethod = SynthesisMethod.DIALECTICAL,
                             synthesis_params: Optional[Dict] = None) -> List[DialecticalState]:
        """
        Run complete dialectical cycle(s)
        
        Full cycle: Thesis → Antithesis → Synthesis → Negation of Negation
        Each cycle begins a new dialectical process at a higher level.
        
        Args:
            initial_thesis: Starting thesis vector
            cycles: Number of cycles to run
            synthesis_method: Method for synthesis step
            synthesis_params: Parameters for synthesis
            
        Returns:
            List of all states in the process
        """
        states = []
        synthesis_params = synthesis_params or {}
        
        # Initialize
        state = self.initialize_state(initial_thesis)
        states.append(state)
        
        for cycle in range(cycles):
            # Thesis → Antithesis
            state = self.apply_negation(state)
            states.append(state)
            
            # Antithesis → Synthesis
            state = self.synthesize(state, synthesis_method, synthesis_params)
            states.append(state)
            
            # Synthesis → Negation of Negation (new thesis)
            state = self.negate_negation(state)
            states.append(state)
        
        return states
    
    def run_until_convergence(self,
                             initial_thesis: List[float],
                             max_cycles: int = 100,
                             tolerance: float = 1e-6,
                             synthesis_method: SynthesisMethod = SynthesisMethod.DIALECTICAL) -> Tuple[List[DialecticalState], bool]:
        """
        Run dialectical cycles until convergence
        
        Convergence: When tension index falls below tolerance
        or thesis change between cycles is minimal.
        
        Returns:
            (states, converged) tuple
        """
        states = []
        converged = False
        
        state = self.initialize_state(initial_thesis)
        states.append(state)
        
        for cycle in range(max_cycles):
            previous_thesis = state.thesis.copy()
            
            # Run one cycle
            state = self.apply_negation(state)
            states.append(state)
            
            state = self.synthesize(state, synthesis_method)
            states.append(state)
            
            state = self.negate_negation(state)
            states.append(state)
            
            # Check convergence
            tension = self.analyze_tension(state)
            thesis_change = sum(abs(p - c) for p, c in zip(previous_thesis, state.thesis))
            
            if tension.tension_index < tolerance and thesis_change < tolerance:
                converged = True
                break
        
        return states, converged
    
    # ------------------------------------------------------------------------
    # UTILITY METHODS
    # ------------------------------------------------------------------------
    
    def _apply_intensity(self,
                        base_vector: List[float],
                        reference: List[float],
                        intensity: float) -> List[float]:
        """
        Apply intensity modulation to a vector
        
        intensity=1.0: Full base_vector
        intensity=0.0: No change (returns reference)
        """
        if not 0 <= intensity <= 1:
            raise ValueError(f"Intensity must be in [0, 1], got {intensity}")
        
        if intensity == 1.0:
            return base_vector
        elif intensity == 0.0:
            return reference
        
        # Linear interpolation
        return [
            intensity * b + (1 - intensity) * r
            for b, r in zip(base_vector, reference)
        ]
    
    def get_state_history(self) -> List[DialecticalState]:
        """Get complete history of all states processed by this engine"""
        return self.state_history.copy()
    
    def clear_history(self):
        """Clear engine's state history"""
        self.state_history.clear()
    
    # ------------------------------------------------------------------------
    # SERIALIZATION
    # ------------------------------------------------------------------------
    
    def export_process(self, states: List[DialecticalState]) -> Dict:
        """
        Export dialectical process as serializable dictionary
        
        Suitable for JSON serialization, persistence, or transmission
        """
        return {
            'states': [state.to_dict() for state in states],
            'total_cycles': len([s for s in states if s.stage == DialecticalStage.NEGATION_OF_NEGATION]),
            'dimensions': states[0].dimensions if states else 0,
            'tension_history': [self.analyze_tension(s).to_dict() for s in states]
        }


# ============================================================================
# 3. SPECIALIZED ENGINES
# ============================================================================

class ConservativeDialecticalEngine(DialecticalEngine):
    """
    Conservative dialectics: Emphasizes preservation over transformation
    
    Uses weighted synthesis that favors thesis preservation
    """
    
    def synthesize(self,
                  state: DialecticalState,
                  method: SynthesisMethod = SynthesisMethod.STANDARD,
                  parameters: Optional[Dict] = None) -> DialecticalState:
        """Override with conservative parameters"""
        params = parameters or {}
        params.setdefault('alpha', 0.8)  # Heavy thesis weighting
        params.setdefault('beta', 0.2)
        return super().synthesize(state, method, params)


class RadicalDialecticalEngine(DialecticalEngine):
    """
    Radical dialectics: Emphasizes transformation over preservation
    
    Uses synthesis methods that create more dramatic transformations
    """
    
    def synthesize(self,
                  state: DialecticalState,
                  method: SynthesisMethod = SynthesisMethod.DIALECTICAL,
                  parameters: Optional[Dict] = None) -> DialecticalState:
        """Override with radical parameters"""
        params = parameters or {}
        params.setdefault('blend_weight', 0.3)  # More antithesis influence
        return super().synthesize(state, method, params)


# ============================================================================
# MAIN: Example usage
# ============================================================================

if __name__ == "__main__":
    print("Testing Dialectical Engine...")
    
    # Create engine
    engine = DialecticalEngine()
    
    # Initialize with philosophical positions
    initial_thesis = [1.0, 0.5, -0.3]  # Some initial position
    print(f"Initial thesis: {initial_thesis}")
    
    # Run one complete cycle
    states = engine.run_dialectical_cycle(
        initial_thesis,
        cycles=1,
        synthesis_method=SynthesisMethod.DIALECTICAL
    )
    
    print(f"\nDialectical cycle completed ({len(states)} states):")
    for i, state in enumerate(states):
        tension = engine.analyze_tension(state)
        print(f"\nState {i+1} ({state.stage.value}):")
        print(f"  Thesis: {[round(v, 3) for v in state.thesis]}")
        print(f"  Antithesis: {[round(v, 3) for v in state.antithesis]}")
        if state.has_synthesis:
            print(f"  Synthesis: {[round(v, 3) for v in state.synthesis]}")
        print(f"  Tension index: {tension.tension_index:.3f}")
    
    # Analyze convergence
    print(f"\n{'='*60}")
    print("Convergence test:")
    convergence_states, converged = engine.run_until_convergence(
        initial_thesis,
        max_cycles=10,
        tolerance=0.01
    )
    print(f"Converged: {converged} after {len(convergence_states)} states")
    
    if converged:
        final_state = convergence_states[-1]
        final_tension = engine.analyze_tension(final_state)
        print(f"Final tension: {final_tension.tension_index:.4f}")
        print(f"Final thesis: {[round(v, 3) for v in final_state.thesis]}")