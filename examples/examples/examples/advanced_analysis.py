"""
Advanced Dialectical Analysis
Sophisticated analytical tools for deep investigation of dialectical processes

Features:
1. Multi-dimensional tension analysis
2. Convergence diagnostics
3. Phase space visualization
4. Attractor identification
5. Stability analysis
6. Bifurcation detection
7. Information-theoretic metrics
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from scipy import stats, signal, optimize
import warnings
warnings.filterwarnings('ignore')

from xenopoulos import DialecticalFactory, SynthesisMethod

# ============================================================================
# 1. ADVANCED ANALYTICAL STRUCTURES
# ============================================================================

@dataclass
class PhasePoint:
    """Point in dialectical phase space"""
    coordinates: np.ndarray
    stage: str
    tension: float
    velocity: Optional[np.ndarray] = None  # Rate of change
    stability: Optional[float] = None  # Local stability measure

@dataclass
class AttractorBasin:
    """Region of phase space that converges to an attractor"""
    center: np.ndarray
    radius: float
    strength: float  # Attraction strength
    stability: float
    points: List[PhasePoint]

@dataclass
class BifurcationPoint:
    """Point where system behavior changes qualitatively"""
    parameter: float
    coordinates: np.ndarray
    type: str  # 'pitchfork', 'saddle-node', 'hopf', 'transcritical'
    stability_change: Tuple[bool, bool]  # (before, after)

class AdvancedDialecticalAnalyzer:
    """
    Advanced analytical tools for dialectical processes
    """
    
    def __init__(self, dimension: int = 3):
        self.dimension = dimension
        self.factory = DialecticalFactory()
        self.service = self.factory.create_default_service()
        
    # ------------------------------------------------------------------------
    # 1. MULTI-SCALE TENSION ANALYSIS
    # ------------------------------------------------------------------------
    
    def analyze_multi_scale_tension(self, 
                                   states: List[Any],
                                   scales: List[int] = None) -> Dict[str, Any]:
        """
        Analyze tension at multiple temporal scales
        
        Args:
            states: List of dialectical states
            scales: Window sizes for multi-scale analysis
        
        Returns:
            Multi-scale tension metrics
        """
        if scales is None:
            scales = [1, 3, 5, 10]
        
        # Extract tension history
        tensions = []
        for state in states:
            if hasattr(state, 'tension'):
                tensions.append(state.tension)
            elif hasattr(self.service.engine, 'analyze_tension'):
                analysis = self.service.engine.analyze_tension(state)
                tensions.append(analysis.tension_index)
            else:
                # Estimate tension from thesis-antithesis difference
                diff = np.linalg.norm(
                    np.array(state.thesis) - np.array(state.antithesis)
                )
                norm = np.linalg.norm(state.thesis) + np.linalg.norm(state.antithesis)
                tensions.append(diff / max(norm, 1e-10))
        
        results = {
            'raw_tensions': tensions,
            'scales': {}
        }
        
        # Multi-scale analysis
        for scale in scales:
            if scale >= len(tensions):
                continue
                
            # Moving average at this scale
            if scale == 1:
                smoothed = tensions
            else:
                kernel = np.ones(scale) / scale
                smoothed = np.convolve(tensions, kernel, mode='valid')
                # Pad to original length
                pad_left = scale // 2
                pad_right = scale - pad_left - 1
                smoothed = np.pad(smoothed, (pad_left, pad_right), mode='edge')
            
            # Calculate metrics at this scale
            results['scales'][scale] = {
                'mean': float(np.mean(smoothed)),
                'std': float(np.std(smoothed)),
                'min': float(np.min(smoothed)),
                'max': float(np.max(smoothed)),
                'trend': self._calculate_trend(smoothed),
                'volatility': self._calculate_volatility(smoothed),
                'autocorrelation': self._calculate_autocorrelation(smoothed),
                'fractal_dimension': self._estimate_fractal_dimension(smoothed)
            }
        
        # Cross-scale correlations
        scale_pairs = []
        correlations = []
        scales_list = list(results['scales'].keys())
        
        for i, scale1 in enumerate(scales_list):
            for scale2 in scales_list[i+1:]:
                data1 = results['scales'][scale1]['smoothed'] if 'smoothed' in locals() else tensions
                data2 = results['scales'][scale2]['smoothed'] if 'smoothed' in locals() else tensions
                
                # Ensure same length
                min_len = min(len(data1), len(data2))
                corr = np.corrcoef(data1[:min_len], data2[:min_len])[0, 1]
                
                scale_pairs.append((scale1, scale2))
                correlations.append(float(corr))
        
        results['cross_scale_correlations'] = {
            'pairs': scale_pairs,
            'correlations': correlations,
            'mean_correlation': float(np.mean(correlations)) if correlations else 0.0
        }
        
        # Detect regime changes
        results['regime_changes'] = self._detect_regime_changes(tensions)
        
        return results
    
    def _calculate_trend(self, data: np.ndarray) -> float:
        """Calculate linear trend coefficient"""
        if len(data) < 2:
            return 0.0
        x = np.arange(len(data))
        slope, _, _, _, _ = stats.linregress(x, data)
        return float(slope)
    
    def _calculate_volatility(self, data: np.ndarray) -> float:
        """Calculate volatility (GARCH-style)"""
        if len(data) < 3:
            return 0.0
        returns = np.diff(data) / (data[:-1] + 1e-10)
        return float(np.std(returns))
    
    def _calculate_autocorrelation(self, data: np.ndarray, lag: int = 1) -> float:
        """Calculate autocorrelation at given lag"""
        if len(data) < lag + 2:
            return 0.0
        return float(np.corrcoef(data[:-lag], data[lag:])[0, 1])
    
    def _estimate_fractal_dimension(self, data: np.ndarray) -> float:
        """
        Estimate fractal dimension using box-counting method
        Simple implementation for 1D series
        """
        if len(data) < 10:
            return 1.0
        
        # Normalize data
        data_norm = (data - np.min(data)) / (np.max(data) - np.min(data) + 1e-10)
        
        # Simple box-counting
        scales = np.logspace(0, np.log10(len(data)/2), 10)
        counts = []
        
        for scale in scales:
            scale_int = int(max(1, scale))
            boxes = len(data_norm) // scale_int
            if boxes < 2:
                continue
            
            # Count boxes needed
            box_count = 0
            for i in range(boxes):
                segment = data_norm[i*scale_int:(i+1)*scale_int]
                if len(segment) > 0:
                    box_count += (np.max(segment) - np.min(segment)) / scale * len(data)
            
            counts.append(box_count)
        
        if len(counts) < 3:
            return 1.0
        
        # Fit power law: N(ε) ∝ ε^{-D}
        scales = scales[:len(counts)]
        log_scales = np.log(scales)
        log_counts = np.log(np.array(counts) + 1e-10)
        
        try:
            slope, _, _, _, _ = stats.linregress(log_scales, log_counts)
            return float(-slope)
        except:
            return 1.0
    
    def _detect_regime_changes(self, data: np.ndarray, 
                              sensitivity: float = 2.0) -> List[Dict]:
        """Detect points where statistical properties change"""
        if len(data) < 20:
            return []
        
        regimes = []
        window_size = max(5, len(data) // 10)
        
        for i in range(window_size, len(data) - window_size):
            before = data[i-window_size:i]
            after = data[i:i+window_size]
            
            # Compare statistical properties
            mean_diff = abs(np.mean(before) - np.mean(after))
            std_diff = abs(np.std(before) - np.std(after))
            
            # Normalize by overall variability
            overall_std = np.std(data)
            if overall_std > 1e-10:
                mean_diff_norm = mean_diff / overall_std
                std_diff_norm = std_diff / overall_std
                
                # Detect change if both exceed threshold
                if mean_diff_norm > sensitivity or std_diff_norm > sensitivity:
                    regimes.append({
                        'index': i,
                        'mean_change': float(mean_diff),
                        'std_change': float(std_diff),
                        'before_mean': float(np.mean(before)),
                        'after_mean': float(np.mean(after)),
                        'confidence': min(mean_diff_norm, std_diff_norm) / sensitivity
                    })
        
        return regimes
    
    # ------------------------------------------------------------------------
    # 2. PHASE SPACE ANALYSIS
    # ------------------------------------------------------------------------
    
    def map_phase_space(self, 
                       initial_points: List[np.ndarray],
                       iterations: int = 100) -> Dict[str, Any]:
        """
        Map the dialectical phase space
        
        Args:
            initial_points: Starting points in phase space
            iterations: Number of dialectical cycles per point
        
        Returns:
            Phase space structure
        """
        phase_points = []
        attractors = []
        bifurcations = []
        
        for init_point in initial_points:
            # Create process from initial point
            process_id = self.service.create_dialectical_process(
                thesis=init_point.tolist(),
                name=f"PhaseSpace_{hash(tuple(init_point)) % 1000}"
            )
            
            # Run multiple cycles
            trajectory = []
            for cycle in range(iterations):
                # Advance process
                try:
                    self.service.advance_process(process_id, 'negate')
                    self.service.advance_process(process_id, 'synthesize')
                    self.service.advance_process(process_id, 'negate_negation')
                    
                    # Get current state
                    process = self.service.get_process(process_id)
                    state = process.current_state
                    
                    # Create phase point
                    coords = np.array(state.thesis)
                    tension = self.service.engine.analyze_tension(state).tension_index
                    
                    # Calculate velocity (change from previous)
                    velocity = None
                    if trajectory:
                        prev_coords = np.array(trajectory[-1].coordinates)
                        velocity = coords - prev_coords
                    
                    point = PhasePoint(
                        coordinates=coords,
                        stage=state.stage.value,
                        tension=tension,
                        velocity=velocity
                    )
                    
                    trajectory.append(point)
                    phase_points.append(point)
                    
                except Exception as e:
                    print(f"Warning: Error in phase space mapping: {e}")
                    break
            
            # Analyze trajectory
            if len(trajectory) > 10:
                # Check for attractors
                attractor = self._identify_attractor(trajectory)
                if attractor:
                    attractors.append(attractor)
                
                # Check for bifurcations
                traj_bifurcations = self._detect_bifurcations(trajectory)
                bifurcations.extend(traj_bifurcations)
        
        # Analyze overall phase space structure
        return {
            'phase_points': phase_points,
            'attractors': attractors,
            'bifurcations': bifurcations,
            'phase_space_metrics': self._analyze_phase_space_metrics(phase_points),
            'basins_of_attraction': self._identify_basins(phase_points, attractors)
        }
    
    def _identify_attractor(self, trajectory: List[PhasePoint]) -> Optional[Dict]:
        """Identify attractors in trajectory"""
        if len(trajectory) < 20:
            return None
        
        # Extract coordinates
        coords = np.array([p.coordinates for p in trajectory])
        
        # Check for convergence
        late_start = len(coords) // 2
        late_traj = coords[late_start:]
        
        # Calculate convergence
        centroid = np.mean(late_traj, axis=0)
        distances = np.linalg.norm(late_traj - centroid, axis=1)
        
        # Check if converging (decreasing distance to centroid)
        if len(distances) > 5:
            early_dist = np.mean(distances[:len(distances)//2])
            late_dist = np.mean(distances[len(distances)//2:])
            
            if late_dist < early_dist * 0.8:  # Convergence threshold
                # Estimate attraction strength
                attraction_strength = 1.0 - (late_dist / (early_dist + 1e-10))
                
                # Estimate stability (inverse of fluctuation)
                stability = 1.0 / (np.std(distances) + 1e-10)
                
                return {
                    'center': centroid.tolist(),
                    'radius': float(np.mean(distances)),
                    'strength': float(attraction_strength),
                    'stability': float(stability),
                    'type': self._classify_attractor(trajectory)
                }
        
        return None
    
    def _classify_attractor(self, trajectory: List[PhasePoint]) -> str:
        """Classify type of attractor"""
        if len(trajectory) < 10:
            return 'unknown'
        
        coords = np.array([p.coordinates for p in trajectory])
        
        # Calculate Lyapunov exponent estimate
        lyapunov = self._estimate_lyapunov(coords)
        
        # Check periodicity
        autocorr = self._calculate_autocorrelation_nd(coords)
        
        if lyapunov > 0.1:
            return 'chaotic'
        elif np.max(autocorr) > 0.7:
            return 'periodic'
        else:
            return 'fixed_point'
    
    def _estimate_lyapunov(self, trajectory: np.ndarray) -> float:
        """Estimate largest Lyapunov exponent"""
        if len(trajectory) < 20:
            return 0.0
        
        # Simple estimation using divergence of nearby trajectories
        n = len(trajectory)
        exponents = []
        
        for i in range(min(10, n-10)):
            # Find nearest neighbor
            distances = np.linalg.norm(trajectory - trajectory[i], axis=1)
            distances[i] = np.inf  # Exclude self
            nearest_idx = np.argmin(distances)
            
            # Track divergence
            initial_dist = distances[nearest_idx]
            if initial_dist < 1e-10:
                continue
                
            # Look ahead a few steps
            lookahead = min(5, n - max(i, nearest_idx) - 1)
            if lookahead > 0:
                final_dist = np.linalg.norm(
                    trajectory[i+lookahead] - trajectory[nearest_idx+lookahead]
                )
                exponent = np.log(final_dist / initial_dist) / lookahead
                exponents.append(exponent)
        
        return float(np.mean(exponents)) if exponents else 0.0
    
    def _calculate_autocorrelation_nd(self, data: np.ndarray, lag: int = 1) -> np.ndarray:
        """Calculate autocorrelation for multidimensional data"""
        if len(data) < lag + 2:
            return np.array([0.0])
        
        # For simplicity, use mean autocorrelation across dimensions
        autocorrs = []
        for dim in range(data.shape[1]):
            dim_data = data[:, dim]
            if np.std(dim_data) > 1e-10:
                corr = np.corrcoef(dim_data[:-lag], dim_data[lag:])[0, 1]
                autocorrs.append(corr)
        
        return np.array(autocorrs) if autocorrs else np.array([0.0])
    
    def _detect_bifurcations(self, trajectory: List[PhasePoint]) -> List[Dict]:
        """Detect bifurcation points in trajectory"""
        if len(trajectory) < 30:
            return []
        
        bifurcations = []
        coords = np.array([p.coordinates for p in trajectory])
        
        # Sliding window analysis
        window_size = len(coords) // 5
        for i in range(window_size, len(coords) - window_size):
            before = coords[i-window_size:i]
            after = coords[i:i+window_size]
            
            # Compare statistical properties
            before_cov = np.cov(before.T) if before.shape[0] > 1 else np.eye(self.dimension)
            after_cov = np.cov(after.T) if after.shape[0] > 1 else np.eye(self.dimension)
            
            # Detect significant change in covariance structure
            cov_change = np.linalg.norm(before_cov - after_cov) / np.linalg.norm(before_cov + 1e-10)
            
            if cov_change > 0.5:  # Threshold
                # Classify bifurcation type
                bif_type = self._classify_bifurcation(before, after)
                
                bifurcations.append({
                    'index': i,
                    'coordinates': coords[i].tolist(),
                    'type': bif_type,
                    'covariance_change': float(cov_change),
                    'stability_change': self._assess_stability_change(before, after)
                })
        
        return bifurcations
    
    def _classify_bifurcation(self, before: np.ndarray, after: np.ndarray) -> str:
        """Classify bifurcation type"""
        # Simple classification based on dimensionality changes
        before_pca = np.linalg.svd(before - np.mean(before, axis=0))[1]
        after_pca = np.linalg.svd(after - np.mean(after, axis=0))[1]
        
        before_rank = np.sum(before_pca > 1e-10)
        after_rank = np.sum(after_pca > 1e-10)
        
        if before_rank != after_rank:
            return 'dimensionality_change'
        
        # Check for oscillatory behavior
        before_acf = self._calculate_autocorrelation_nd(before)
        after_acf = self._calculate_autocorrelation_nd(after)
        
        if np.max(after_acf) > 0.8 and np.max(before_acf) < 0.5:
            return 'hopf'  # Emergence of oscillations
        
        return 'unknown'
    
    def _assess_stability_change(self, before: np.ndarray, after: np.ndarray) -> Tuple[bool, bool]:
        """Assess stability before and after potential bifurcation"""
        # Simple assessment based on variance
        before_var = np.mean(np.var(before, axis=0))
        after_var = np.mean(np.var(after, axis=0))
        
        before_stable = before_var < 0.1  # Threshold
        after_stable = after_var < 0.1
        
        return (before_stable, after_stable)
    
    def _analyze_phase_space_metrics(self, points: List[PhasePoint]) -> Dict:
        """Analyze overall phase space structure"""
        if not points:
            return {}
        
        coords = np.array([p.coordinates for p in points])
        
        return {
            'dimensionality': self._estimate_effective_dimensions(coords),
            'volume': float(np.prod(np.std(coords, axis=0))),
            'symmetry': self._assess_symmetry(coords),
            'complexity': self._calculate_phase_space_complexity(coords)
        }
    
    def _estimate_effective_dimensions(self, data: np.ndarray) -> int:
        """Estimate effective dimensionality using PCA"""
        if len(data) < 2:
            return 0
        
        # Center data
        centered = data - np.mean(data, axis=0)
        
        # SVD
        _, s, _ = np.linalg.svd(centered)
        
        # Count significant singular values
        total_variance = np.sum(s**2)
        cumulative = np.cumsum(s**2) / total_variance
        
        # Dimensions explaining 95% of variance
        effective_dims = np.sum(cumulative < 0.95) + 1
        
        return min(effective_dims, data.shape[1])
    
    def _assess_symmetry(self, data: np.ndarray) -> float:
        """Assess symmetry of phase space distribution"""
        if len(data) < 10:
            return 0.0
        
        # Check symmetry around mean
        centered = data - np.mean(data, axis=0)
        
        # For each dimension, compare positive and negative parts
        symmetries = []
        for dim in range(data.shape[1]):
            pos = centered[centered[:, dim] > 0, dim]
            neg = -centered[centered[:, dim] < 0, dim]
            
            if len(pos) > 0 and len(neg) > 0:
                # Compare distributions using Kolmogorov-Smirnov
                try:
                    stat, _ = stats.ks_2samp(pos, neg)
                    symmetry = 1.0 - stat  # 1.0 = perfect symmetry
                    symmetries.append(symmetry)
                except:
                    symmetries.append(0.0)
        
        return float(np.mean(symmetries)) if symmetries else 0.0
    
    def _calculate_phase_space_complexity(self, data: np.ndarray) -> float:
        """Calculate phase space complexity using information-theoretic measures"""
        if len(data) < 20:
            return 0.0
        
        # Simple complexity measure: product of dimension-wise entropies
        complexities = []
        for dim in range(data.shape[1]):
            dim_data = data[:, dim]
            
            # Discretize for entropy calculation
            hist, _ = np.histogram(dim_data, bins=min(10, len(dim_data)//5))
            hist = hist / np.sum(hist)
            
            # Calculate entropy
            entropy = -np.sum(hist * np.log(hist + 1e-10))
            complexities.append(entropy)
        
        return float(np.prod(complexities)) if complexities else 0.0
    
    def _identify_basins(self, points: List[PhasePoint], 
                        attractors: List[Dict]) -> List[AttractorBasin]:
        """Identify basins of attraction"""
        if not attractors or not points:
            return []
        
        basins = []
        coords = np.array([p.coordinates for p in points])
        
        for attractor in attractors:
            center = np.array(attractor['center'])
            
            # Find points attracted to this center
            distances = np.linalg.norm(coords - center, axis=1)
            radius = np.percentile(distances, 75)  # 75th percentile as basin radius
            
            # Select points within basin
            basin_points = [points[i] for i in range(len(points)) 
                          if distances[i] < radius]
            
            if basin_points:
                basin = AttractorBasin(
                    center=center,
                    radius=float(radius),
                    strength=attractor['strength'],
                    stability=attractor['stability'],
                    points=basin_points
                )
                basins.append(basin)
        
        return basins
    
    # ------------------------------------------------------------------------
    # 3. INFORMATION-THEORETIC ANALYSIS
    # ------------------------------------------------------------------------
    
    def information_theoretic_analysis(self, 
                                      states: List[Any]) -> Dict[str, Any]:
        """
        Perform information-theoretic analysis of dialectical process
        
        Args:
            states: List of dialectical states
        
        Returns:
            Information-theoretic metrics
        """
        # Extract time series of thesis vectors
        thesis_series = []
        for state in states:
            thesis_series.append(state.thesis)
        
        thesis_array = np.array(thesis_series)
        
        results = {
            'dimensional_information': {},
            'mutual_information': {},
            'predictability': {},
            'complexity_measures': {}
        }
        
        # Analyze each dimension
        for dim in range(self.dimension):
            dim_series = thesis_array[:, dim]
            
            # Entropy
            entropy = self._calculate_entropy(dim_series)
            
            # Predictive information
            predictive_info = self._calculate_predictive_information(dim_series)
            
            # Statistical complexity
            stat_complexity = self._calculate_statistical_complexity(dim_series)
            
            results['dimensional_information'][dim] = {
                'entropy': entropy,
                'predictive_information': predictive_info,
                'statistical_complexity': stat_complexity,
                'information_production': self._calculate_information_production(dim_series)
            }
        
        # Cross-dimensional mutual information
        for dim1 in range(self.dimension):
            for dim2 in range(dim1 + 1, self.dimension):
                series1 = thesis_array[:, dim1]
                series2 = thesis_array[:, dim2]
                
                mutual_info = self._calculate_mutual_information(series1, series2)
                transfer_entropy = self._calculate_transfer_entropy(series1, series2)
                
                results['mutual_information'][f"{dim1}_{dim2}"] = {
                    'mutual_information': mutual_info,
                    'transfer_entropy': transfer_entropy,
                    'causality_ratio': transfer_entropy / (mutual_info + 1e-10)
                }
        
        # Overall predictability
        results['predictability'] = {
            'mean_predictability': self._assess_predictability(thesis_array),
            'predictable_dimensions': self._identify_predictable_dimensions(thesis_array),
            'surprise_sequence': self._calculate_surprise_sequence(thesis_array)
        }
        
        # Complexity measures
        results['complexity_measures'] = {
            'integrated_information': self._calculate_integrated_information(thesis_array),
            'causal_density': self._calculate_causal_density(thesis_array),
            'temporal_complexity': self._calculate_temporal_complexity(thesis_array)
        }
        
        return results
    
    def _calculate_entropy(self, series: np.ndarray, bins: int = 10) -> float:
        """Calculate Shannon entropy of a time series"""
        hist, _ = np.histogram(series, bins=bins)
        hist = hist / np.sum(hist)
        return float(-np.sum(hist * np.log(hist + 1e-10)))
    
    def _calculate_predictive_information(self, series: np.ndarray, 
                                         max_lag: int = 5) -> float:
        """Calculate predictive information (I_pred)"""
        if len(series) < max_lag * 2:
            return 0.0
        
        predictive_info = []
        for lag in range(1, min(max_lag, len(series)//2)):
            # Mutual information between past and future
            past = series[:-lag]
            future = series[lag:]
            
            mi = self._calculate_mutual_information(past, future)
            predictive_info.append(mi)
        
        return float(np.mean(predictive_info)) if predictive_info else 0.0
    
    def _calculate_statistical_complexity(self, series: np.ndarray) -> float:
        """Calculate statistical complexity (Cμ)"""
        # Simple implementation: product of entropy and predictive information
        entropy = self._calculate_entropy(series)
        predictive = self._calculate_predictive_information(series)
        return float(entropy * predictive)
    
    def _calculate_information_production(self, series: np.ndarray) -> float:
        """Calculate rate of information production"""
        if len(series) < 10:
            return 0.0
        
        # Difference in entropy over time
        half = len(series) // 2
        entropy_first = self._calculate_entropy(series[:half])
        entropy_second = self._calculate_entropy(series[half:])
        
        return float(abs(entropy_second - entropy_first) / half)
    
    def _calculate_mutual_information(self, x: np.ndarray, y: np.ndarray, 
                                     bins: int = 10) -> float:
        """Calculate mutual information between two series"""
        # Joint histogram
        hist_2d, x_edges, y_edges = np.histogram2d(x, y, bins=bins)
        
        # Normalize
        hist_2d = hist_2d / np.sum(hist_2d)
        
        # Marginal distributions
        p_x = np.sum(hist_2d, axis=1)
        p_y = np.sum(hist_2d, axis=0)
        
        # Mutual information
        mi = 0.0
        for i in range(bins):
            for j in range(bins):
                if hist_2d[i, j] > 0:
                    mi += hist_2d[i, j] * np.log(hist_2d[i, j] / (p_x[i] * p_y[j] + 1e-10))
        
        return float(mi)
    
    def _calculate_transfer_entropy(self, x: np.ndarray, y: np.ndarray, 
                                   lag: int = 1, bins: int = 5) -> float:
        """Calculate transfer entropy from x to y"""
        if len(x) < lag + 10 or len(y) < lag + 10:
            return 0.0
        
        # Prepare time series
        y_future = y[lag:]
        y_past = y[:-lag]
        x_past = x[:-lag]
        
        # Calculate conditional entropies
        # H(Y_future | Y_past)
        hist_cond, _, _ = np.histogram2d(y_future, y_past, bins=bins)
        hist_cond = hist_cond / np.sum(hist_cond)
        p_y_past = np.sum(hist_cond, axis=0)
        
        h_yf_yp = 0.0
        for i in range(bins):
            for j in range(bins):
                if hist_cond[i, j] > 0:
                    h_yf_yp -= hist_cond[i, j] * np.log(hist_cond[i, j] / (p_y_past[j] + 1e-10))
        
        # H(Y_future | Y_past, X_past)
        hist_joint, _ = np.histogramdd(np.column_stack([y_future, y_past, x_past]), 
                                      bins=[bins, bins, bins])
        hist_joint = hist_joint / np.sum(hist_joint)
        p_yp_xp = np.sum(hist_joint, axis=0)
        
        h_yf_yp_xp = 0.0
        it = np.nditer(hist_joint, flags=['multi_index'])
        for val in it:
            if val > 0:
                i, j, k = it.multi_index
                h_yf_yp_xp -= val * np.log(val / (p_yp_xp[j, k] + 1e-10))
        
        # Transfer entropy: H(Y_future|Y_past) - H(Y_future|Y_past,X_past)
        return float(max(0, h_yf_yp - h_yf_yp_xp))
    
    def _assess_predictability(self, series_array: np.ndarray) -> float:
        """Assess overall predictability of the system"""
        # Use autocorrelation as proxy for predictability
        autocorrs = []
        for dim in range(series_array.shape[1]):
            dim_series = series_array[:, dim]
            if len(dim_series) > 10:
                autocorr = self._calculate_autocorrelation(dim_series, lag=1)
                autocorrs.append(abs(autocorr))
        
        return float(np.mean(autocorrs)) if autocorrs else 0.0
    
    def _identify_predictable_dimensions(self, series_array: np.ndarray, 
                                        threshold: float = 0.7) -> List[int]:
        """Identify which dimensions are most predictable"""
        predictable_dims = []
        for dim in range(series_array.shape[1]):
            dim_series = series_array[:, dim]
            if len(dim_series) > 10:
                autocorr = self._calculate_autocorrelation(dim_series, lag=1)
                if abs(autocorr) > threshold:
                    predictable_dims.append(dim)
        
        return predictable_dims
    
    def _calculate_surprise_sequence(self, series_array: np.ndarray) -> np.ndarray:
        """Calculate sequence of surprises (unexpected changes)"""
        if len(series_array) < 10:
            return np.array([])
        
        surprises = []
        for i in range(1, len(series_array)):
            # Surprise = unexpected change
            change = np.linalg.norm(series_array[i] - series_array[i-1])
            expected = np.mean([np.linalg.norm(series_array[j] - series_array[j-1]) 
                              for j in range(max(1, i-5), i)])
            
            surprise = max(0, change - expected)
            surprises.append(surprise)
        
        return np.array(surprises)
    
    def _calculate_integrated_information(self, series_array: np.ndarray) -> float:
        """Calculate integrated information (Φ) - simplified"""
        # Simplified Φ: mutual information minus sum of dimensional entropies
        total_mi = 0.0
        pair_count = 0
        
        for dim1 in range(series_array.shape[1]):
            for dim2 in range(dim1 + 1, series_array.shape[1]):
                mi = self._calculate_mutual_information(series_array[:, dim1], 
                                                       series_array[:, dim2])
                total_mi += mi
                pair_count += 1
        
        avg_mi = total_mi / max(pair_count, 1)
        
        # Sum of individual entropies
        sum_entropies = 0.0
        for dim in range(series_array.shape[1]):
            sum_entropies += self._calculate_entropy(series_array[:, dim])
        
        # Simplified Φ
        return float(max(0, avg_mi * series_array.shape[1] - sum_entropies))
    
    def _calculate_causal_density(self, series_array: np.ndarray) -> float:
        """Calculate causal density"""
        n_dims = series_array.shape[1]
        if n_dims < 2:
            return 0.0
        
        causal_links = []
        for i in range(n_dims):
            for j in range(n_dims):
                if i != j:
                    te = self._calculate_transfer_entropy(series_array[:, i], 
                                                         series_array[:, j])
                    causal_links.append(te)
        
        return float(np.mean(causal_links)) if causal_links else 0.0
    
    def _calculate_temporal_complexity(self, series_array: np.ndarray) -> float:
        """Calculate temporal complexity"""
        # Product of dimensionality and unpredictability
        effective_dims = self._estimate_effective_dimensions(series_array)
        unpredictability = 1.0 - self._assess_predictability(series_array)
        
        return float(effective_dims * unpredictability)

# ============================================================================
# 4. VISUALIZATION TOOLS
# ============================================================================

def visualize_advanced_analysis(results: Dict[str, Any], save_path: str = None):
    """
    Create comprehensive visualizations of advanced analysis
    
    Args:
        results: Analysis results from AdvancedDialecticalAnalyzer
        save_path: Optional path to save figures
    """
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        
        # Create figure with multiple subplots
        n_plots = min(6, len(results.keys()))
        fig = plt.figure(figsize=(15, 10))
        
        plot_idx = 1
        
