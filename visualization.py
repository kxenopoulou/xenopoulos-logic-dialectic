"""
Visualization Layer for Klein-4 Dialectical System
Layer 6: Comprehensive visualization of mathematical and dialectical properties

Provides interactive plots, 3D visualizations, and analytical diagrams for:
1. Klein-4 group structure visualization
2. Dialectical process evolution
3. Vector transformations
4. Mathematical property demonstrations
5. Comparison and analysis tools
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
from typing import List, Dict, Tuple, Optional, Any, Union
import seaborn as sns
import pandas as pd
from dataclasses import dataclass, field
import time
import json
import base64
from io import BytesIO
import warnings
from enum import Enum
import os

# ============================================================================
# MINIMAL IMPLEMENTATIONS FOR MISSING IMPORTS
# ============================================================================

# Define minimal versions of missing classes
class DialecticalStage(Enum):
    """Minimal implementation of DialecticalStage"""
    THESIS = "THESIS"
    ANTITHESIS = "ANTITHESIS"
    SYNTHESIS = "SYNTHESIS"
    NEGATION_OF_NEGATION = "NEGATION_OF_NEGATION"


class SynthesisMethod(Enum):
    """Minimal implementation of SynthesisMethod"""
    DIALECTICAL = "DIALECTICAL"
    LINEAR = "LINEAR"
    GEOMETRIC = "GEOMETRIC"
    HARMONIC = "HARMONIC"


class DialecticalState:
    """Minimal implementation of DialecticalState"""
    def __init__(self, thesis: List[float], stage: DialecticalStage = DialecticalStage.THESIS):
        self.thesis = thesis
        self.stage = stage
        self.dimensions = len(thesis)
        self.has_synthesis = False
        self.synthesis = None
        self.antithesis = [-x for x in thesis]  # Simple negation as antithesis
    
    def __repr__(self):
        return f"DialecticalState(thesis={self.thesis[:3]}..., stage={self.stage.value})"


class TensionAnalysis:
    """Minimal implementation of TensionAnalysis"""
    def __init__(self, state: Optional[DialecticalState] = None):
        if state is None:
            self.mean_difference = np.random.random()
            self.max_difference = np.random.random()
            self.mean_similarity = np.random.random()
            self.tension_index = np.random.random()
            self.correlation = np.random.uniform(-1, 1)
            self.entropy = np.random.random()
        else:
            # Calculate actual tension
            diff = np.abs(np.array(state.thesis) - np.array(state.antithesis))
            self.mean_difference = np.mean(diff)
            self.max_difference = np.max(diff)
            self.mean_similarity = np.mean(np.abs(np.array(state.thesis) + np.array(state.antithesis)))
            self.tension_index = self.mean_difference / (self.mean_difference + self.mean_similarity + 1e-10)
            self.correlation = np.corrcoef(state.thesis, state.antithesis)[0, 1] if len(state.thesis) > 1 else 0
            self.entropy = -np.sum(p * np.log(p + 1e-10) for p in np.abs(state.thesis)/np.sum(np.abs(state.thesis)))


class DialecticalEngine:
    """Minimal implementation of DialecticalEngine"""
    def __init__(self):
        pass
    
    def run_dialectical_cycle(self, initial_thesis: List[float], cycles: int = 1,
                            synthesis_method: SynthesisMethod = SynthesisMethod.DIALECTICAL):
        """Minimal implementation - generates dummy states"""
        states = []
        current_thesis = initial_thesis
        
        for cycle in range(cycles):
            # Create states for each stage in a cycle
            stages = [
                (DialecticalStage.THESIS, current_thesis),
                (DialecticalStage.ANTITHESIS, [-x for x in current_thesis]),
                (DialecticalStage.SYNTHESIS, [0.5 * (current_thesis[i] + (-current_thesis[i])) 
                                            for i in range(len(current_thesis))]),
                (DialecticalStage.NEGATION_OF_NEGATION, current_thesis)  # Returns to thesis
            ]
            
            for stage, values in stages:
                state = DialecticalState(values, stage)
                if stage == DialecticalStage.SYNTHESIS:
                    state.has_synthesis = True
                    state.synthesis = values
                states.append(state)
            
            # Update for next cycle
            current_thesis = [x * 0.8 for x in current_thesis]  # Dampening
        
        return states
    
    def initialize_state(self, thesis: List[float]):
        """Minimal implementation"""
        return DialecticalState(thesis)
    
    def analyze_tension(self, state: DialecticalState):
        """Minimal implementation"""
        return TensionAnalysis(state)


class INRCOperator:
    """Minimal implementation of INRCOperator"""
    def __init__(self, symbol: str, description: str):
        self.symbol = symbol
        self.description = description


class MatrixOperator:
    """Minimal implementation of MatrixOperator"""
    def __init__(self, dimension: int = 3):
        self.dimension = dimension
        
        # Create simple matrices for I, N, R, C
        if dimension == 3:
            self.matrices = {
                'I': np.eye(dimension),
                'N': -np.eye(dimension),
                'R': np.array([[0, -1, 0], 
                              [1, 0, 0], 
                              [0, 0, -1]]),
                'C': np.array([[0, 1, 0], 
                              [1, 0, 0], 
                              [0, 0, -1]])
            }
        else:
            # For other dimensions, create simple patterns
            self.matrices = {
                'I': np.eye(dimension),
                'N': -np.eye(dimension),
                'R': self._create_r_matrix(dimension),
                'C': self._create_c_matrix(dimension)
            }
    
    def _create_r_matrix(self, dim: int):
        """Create R matrix for arbitrary dimension"""
        matrix = np.eye(dim)
        # Swap first two dimensions and apply negation pattern
        matrix[0, 0] = 0
        matrix[0, 1] = -1
        matrix[1, 0] = 1
        matrix[1, 1] = 0
        return matrix
    
    def _create_c_matrix(self, dim: int):
        """Create C matrix for arbitrary dimension"""
        matrix = np.eye(dim)
        # Create correlation pattern
        for i in range(dim):
            for j in range(dim):
                if i == j:
                    matrix[i, j] = -1 if i % 2 == 0 else 1
                elif i + j == dim - 1:
                    matrix[i, j] = 1
        return matrix
    
    def get_all_matrices(self):
        return self.matrices
    
    def apply_matrix(self, vector: np.ndarray, operator: str):
        if len(vector) != self.dimension:
            # Pad or truncate vector if needed
            if len(vector) > self.dimension:
                vector = vector[:self.dimension]
            else:
                vector = np.pad(vector, (0, self.dimension - len(vector)))
        return self.matrices[operator] @ vector


class INRCOperatorFactory:
    """Minimal implementation of INRCOperatorFactory"""
    def __init__(self):
        pass
    
    def create_with_validation(self):
        """Create dummy operators"""
        return {
            'I': INRCOperator('I', 'Identity: Leaves vector unchanged'),
            'N': INRCOperator('N', 'Negation: Reverses all signs'),
            'R': INRCOperator('R', 'Reciprocity: Swaps and negates components'),
            'C': INRCOperator('C', 'Correlation: Combines N and R operations')
        }
    
    def create_matrix_operators(self, dimension: int = 3):
        return MatrixOperator(dimension)


# ============================================================================
# 1. VISUALIZATION CONFIGURATION
# ============================================================================

class VisualizationStyle(Enum):
    """Visualization style presets"""
    CLASSIC = "classic"          # Matplotlib classic style
    MODERN = "modern"            # Seaborn modern style
    DARK = "dark"                # Dark theme for presentations
    PUBLICATION = "publication"  # Publication quality
    INTERACTIVE = "interactive"  # Plotly interactive
    MINIMAL = "minimal"          # Minimal clean style


@dataclass
class VisualConfig:
    """Configuration for visualizations"""
    
    # General settings
    style: VisualizationStyle = VisualizationStyle.MODERN
    dpi: int = 150
    figsize: Tuple[int, int] = (12, 8)
    color_palette: str = "viridis"
    dark_mode: bool = False
    
    # Klein-4 specific
    operator_colors: Dict[str, str] = field(default_factory=lambda: {
        'I': '#2E86AB',    # Blue
        'N': '#A23B72',    # Purple
        'R': '#F18F01',    # Orange
        'C': '#C73E1D'     # Red
    })
    
    # Dialectical stages colors
    stage_colors: Dict[DialecticalStage, str] = field(default_factory=lambda: {
        DialecticalStage.THESIS: '#2E86AB',          # Blue
        DialecticalStage.ANTITHESIS: '#A23B72',      # Purple
        DialecticalStage.SYNTHESIS: '#F18F01',       # Orange
        DialecticalStage.NEGATION_OF_NEGATION: '#C73E1D'  # Red
    })
    
    # Animation settings
    animation_fps: int = 30
    animation_duration: int = 5  # seconds
    
    def apply_style(self):
        """Apply the selected style to matplotlib"""
        if self.style == VisualizationStyle.CLASSIC:
            plt.style.use('classic')
        elif self.style == VisualizationStyle.MODERN:
            plt.style.use('seaborn-v0_8-darkgrid')
            sns.set_palette(self.color_palette)
        elif self.style == VisualizationStyle.DARK:
            plt.style.use('dark_background')
        elif self.style == VisualizationStyle.PUBLICATION:
            plt.style.use('seaborn-paper')
            plt.rcParams.update({
                'font.size': 11,
                'axes.labelsize': 12,
                'axes.titlesize': 14,
                'xtick.labelsize': 10,
                'ytick.labelsize': 10,
                'legend.fontsize': 10,
                'figure.titlesize': 16
            })
        elif self.style == VisualizationStyle.MINIMAL:
            plt.style.use('default')
            plt.rcParams.update({
                'axes.spines.top': False,
                'axes.spines.right': False,
                'axes.grid': True,
                'grid.alpha': 0.3
            })


# ============================================================================
# 2. KLEIN-4 GROUP VISUALIZATIONS
# ============================================================================

class Klein4Visualizer:
    """Visualizations specifically for Klein-4 group properties"""
    
    def __init__(self, dimension: int = 3, config: Optional[VisualConfig] = None):
        """
        Initialize Klein-4 visualizer
        
        Args:
            dimension: Dimension for operators
            config: Visualization configuration
        """
        self.dimension = dimension
        self.config = config or VisualConfig()
        self.operator_factory = INRCOperatorFactory()
        self.operators = self.operator_factory.create_with_validation()
        self.matrix_ops = self.operator_factory.create_matrix_operators(dimension)
        self.matrices = self.matrix_ops.get_all_matrices()
        
        # Apply style
        self.config.apply_style()
    
    # ------------------------------------------------------------------------
    # 2.1 GROUP STRUCTURE VISUALIZATIONS
    # ------------------------------------------------------------------------
    
    def plot_cayley_table(self, save_path: Optional[str] = None) -> Figure:
        """
        Plot Cayley table for Klein-4 group
        
        Shows the complete multiplication table with colors
        """
        fig, ax = plt.subplots(figsize=self.config.figsize)
        
        # Cayley table data
        operators = ['I', 'N', 'R', 'C']
        cayley_table = [
            ['I', 'N', 'R', 'C'],
            ['N', 'I', 'C', 'R'],
            ['R', 'C', 'I', 'N'],
            ['C', 'R', 'N', 'I']
        ]
        
        # Create table - FIXED: Use proper cellText and cellLoc
        cell_text = []
        cell_colors = []
        
        # Add header row
        header_row = [''] + operators
        cell_text.append(header_row)
        cell_colors.append(['#f0f0f0'] * 5)  # Gray for header
        
        # Add data rows
        for i, row in enumerate(cayley_table):
            row_text = [operators[i]] + row
            cell_text.append(row_text)
            
            # Color cells
            row_colors = ['#f0f0f0']  # First cell is row header
            for cell in row:
                row_colors.append(self.config.operator_colors.get(cell, '#ffffff'))
            cell_colors.append(row_colors)
        
        # Create table with explicit cell data
        table = ax.table(cellText=cell_text,
                        cellLoc='center',
                        loc='center',
                        cellColours=cell_colors)
        
        # Style table
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 2)
        
        # Style all cells
        for i in range(len(cell_text)):  # rows
            for j in range(len(cell_text[0])):  # columns
                cell = table[(i, j)]
                cell.set_text_props(weight='bold' if i == 0 or j == 0 else 'normal')
                if i == 0 or j == 0:  # Headers
                    cell.set_text_props(color='black')
                else:
                    cell.set_text_props(color='white' if self.config.dark_mode else 'black')
        
        ax.axis('off')
        ax.set_title('Klein-4 Group Cayley Table', fontsize=16, pad=20)
        
        # Add legend
        legend_elements = []
        for op, color in self.config.operator_colors.items():
            legend_elements.append(plt.Rectangle((0, 0), 1, 1, facecolor=color, 
                                               label=f'{op}: {self.operators[op].description}'))
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        
        return fig
    
    def plot_group_structure_diagram(self, save_path: Optional[str] = None) -> Figure:
        """
        Plot group structure as a directed graph
        
        Shows relationships between operators
        """
        fig, ax = plt.subplots(figsize=self.config.figsize)
        
        # Create directed graph
        G = nx.DiGraph()
        
        # Add nodes
        for op in ['I', 'N', 'R', 'C']:
            G.add_node(op, color=self.config.operator_colors[op])
        
        # Add edges for composition
        edges = [
            ('N', 'C', 'R'), ('R', 'C', 'N'), ('C', 'N', 'R'),
            ('N', 'R', 'C'), ('R', 'N', 'C'), ('C', 'R', 'N'),
            ('I', 'N', 'N'), ('I', 'R', 'R'), ('I', 'C', 'C'),
            ('N', 'N', 'I'), ('R', 'R', 'I'), ('C', 'C', 'I')
        ]
        
        for a, b, result in edges:
            G.add_edge(a, result, label=b, composition=f"{a}∘{b} = {result}")
        
        # Position nodes in a square
        pos = {
            'I': (0, 0),
            'N': (1, 0),
            'R': (0, 1),
            'C': (1, 1)
        }
        
        # Draw nodes
        node_colors = [self.config.operator_colors[node] for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=2000, alpha=0.8, ax=ax)
        
        # Draw edges with labels
        edge_labels = nx.get_edge_attributes(G, 'composition')
        nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, 
                              edge_color='gray', width=2, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
                                    font_size=10, ax=ax)
        
        # Draw node labels
        nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', 
                               font_color='white' if self.config.dark_mode else 'black', ax=ax)
        
        ax.set_title('Klein-4 Group Structure Diagram', fontsize=16)
        ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        
        return fig
    
    # ------------------------------------------------------------------------
    # 2.2 MATRIX VISUALIZATIONS
    # ------------------------------------------------------------------------
    
    def plot_operator_matrices(self, save_path: Optional[str] = None) -> Figure:
        """
        Visualize all operator matrices as heatmaps
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()
        
        operators = ['I', 'N', 'R', 'C']
        
        for idx, op in enumerate(operators):
            ax = axes[idx]
            matrix = self.matrices[op]
            
            # Create heatmap
            im = ax.imshow(matrix, cmap='RdBu_r', vmin=-1, vmax=1, 
                          interpolation='nearest')
            
            # Add text annotations
            for i in range(self.dimension):
                for j in range(self.dimension):
                    value = matrix[i, j]
                    if abs(value) > 0.5:  # Significant values
                        color = 'white'
                    else:
                        color = 'black'
                    ax.text(j, i, f'{value:.1f}', ha='center', va='center', 
                           color=color, fontsize=10)
            
            ax.set_title(f'Operator {op}', fontsize=14, 
                        color=self.config.operator_colors[op])
            ax.set_xlabel('Column')
            ax.set_ylabel('Row')
            ax.set_xticks(range(self.dimension))
            ax.set_yticks(range(self.dimension))
            
            # Add grid
            ax.set_xticks(np.arange(-0.5, self.dimension, 1), minor=True)
            ax.set_yticks(np.arange(-0.5, self.dimension, 1), minor=True)
            ax.grid(which='minor', color='gray', linestyle='-', linewidth=1)
        
        fig.suptitle(f'Klein-4 Operator Matrices (Dimension {self.dimension})', 
                    fontsize=18, y=1.02)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        
        return fig
    
    def plot_matrix_eigenvalues(self, save_path: Optional[str] = None) -> Figure:
        """
        Plot eigenvalues of all operators on complex plane
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()
        
        operators = ['I', 'N', 'R', 'C']
        
        for idx, op in enumerate(operators):
            ax = axes[idx]
            matrix = self.matrices[op]
            
            # Calculate eigenvalues
            eigenvalues = np.linalg.eigvals(matrix)
            
            # Plot on complex plane
            real_parts = np.real(eigenvalues)
            imag_parts = np.imag(eigenvalues)
            
            # Unit circle
            theta = np.linspace(0, 2*np.pi, 100)
            ax.plot(np.cos(theta), np.sin(theta), '--', color='gray', alpha=0.5, linewidth=1)
            
            # Plot eigenvalues
            colors = self.config.operator_colors[op]
            ax.scatter(real_parts, imag_parts, color=colors, s=100, alpha=0.8, 
                      edgecolors='black', linewidth=1.5, zorder=5)
            
            # Mark ±1 points
            ax.scatter([1, -1], [0, 0], color='red', s=50, marker='x', 
                      linewidth=2, zorder=6, label='±1')
            
            # Set limits
            max_val = max(1.2, np.max(np.abs(eigenvalues)) * 1.2)
            ax.set_xlim(-max_val, max_val)
            ax.set_ylim(-max_val, max_val)
            
            ax.set_xlabel('Real')
            ax.set_ylabel('Imaginary')
            ax.set_title(f'Eigenvalues of {op}', fontsize=14, 
                        color=self.config.operator_colors[op])
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='k', linestyle='-', alpha=0.2)
            ax.axvline(x=0, color='k', linestyle='-', alpha=0.2)
            ax.set_aspect('equal')
            
            # Add eigenvalue values as text
            for i, (real, imag) in enumerate(zip(real_parts, imag_parts)):
                ax.text(real, imag + 0.1, f'{real:.2f}{imag:+.2f}i', 
                       fontsize=8, ha='center')
        
        fig.suptitle('Eigenvalues on Complex Plane (Should be ±1)', fontsize=18, y=1.02)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        
        return fig
    
    # ------------------------------------------------------------------------
    # 2.3 VECTOR TRANSFORMATION VISUALIZATIONS
    # ------------------------------------------------------------------------
    
    def plot_vector_transformations_2d(self, vector: Optional[np.ndarray] = None,
                                      save_path: Optional[str] = None) -> Figure:
        """
        Plot 2D vector transformations (for dimension 2)
        
        Only works for 2D vectors
        """
        if self.dimension != 2:
            print("Warning: 2D visualization only works for dimension 2")
            print(f"Creating 2D visualization with first 2 dimensions of {self.dimension}D data")
            # Create a 2D subvector if dimension > 2
            if vector is None:
                vector = np.random.randn(self.dimension)
            vector = vector[:2]
            # Create temporary 2D matrices
            temp_matrices = {}
            for op in ['I', 'N', 'R', 'C']:
                matrix = self.matrices[op][:2, :2]
                temp_matrices[op] = matrix
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()
        
        # Generate test vector if not provided
        if vector is None:
            vector = np.array([1.0, 0.5])
        
        operators = ['I', 'N', 'R', 'C']
        
        for idx, op in enumerate(operators):
            ax = axes[idx]
            
            # Apply operator
            if self.dimension == 2:
                transformed = self.matrix_ops.apply_matrix(vector, op)
            else:
                # Use 2D version
                transformed = temp_matrices[op] @ vector
            
            # Create quiver plot
            ax.quiver(0, 0, vector[0], vector[1], 
                     angles='xy', scale_units='xy', scale=1,
                     color='blue', alpha=0.7, width=0.01, 
                     label='Original')
            
            ax.quiver(0, 0, transformed[0], transformed[1],
                     angles='xy', scale_units='xy', scale=1,
                     color=self.config.operator_colors[op], alpha=0.7, 
                     width=0.01, label=f'{op} applied')
            
            # Set limits
            max_val = max(np.max(np.abs(vector)), np.max(np.abs(transformed))) * 1.5
            ax.set_xlim(-max_val, max_val)
            ax.set_ylim(-max_val, max_val)
            
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title(f'Operator {op}: {self.operators[op].description}', 
                        fontsize=14, color=self.config.operator_colors[op])
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='k', linestyle='-', alpha=0.2)
            ax.axvline(x=0, color='k', linestyle='-', alpha=0.2)
            ax.set_aspect('equal')
            ax.legend()
            
            # Add angle and magnitude info
            orig_angle = np.degrees(np.arctan2(vector[1], vector[0]))
            trans_angle = np.degrees(np.arctan2(transformed[1], transformed[0]))
            orig_mag = np.linalg.norm(vector)
            trans_mag = np.linalg.norm(transformed)
            
            info_text = (f'Original: ({vector[0]:.2f}, {vector[1]:.2f})\n'
                        f'Transformed: ({transformed[0]:.2f}, {transformed[1]:.2f})\n'
                        f'Angle change: {abs(trans_angle - orig_angle):.1f}°\n'
                        f'Magnitude: {orig_mag:.2f} → {trans_mag:.2f}')
            
            ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
                   verticalalignment='top', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        fig.suptitle(f'2D Vector Transformations by Klein-4 Operators\n'
                    f'Original vector: {vector}', fontsize=18, y=1.02)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        
        return fig
    
    def plot_vector_transformations_3d(self, vector: Optional[np.ndarray] = None,
                                      save_path: Optional[str] = None) -> Figure:
        """
        Plot 3D vector transformations (for dimension 3 or higher)
        """
        if self.dimension < 3:
            print(f"Warning: 3D visualization requires dimension ≥ 3, current is {self.dimension}")
            print("Creating simulated 3D visualization")
            plot_dim = 3
            # Create simulated 3D vector
            if vector is None:
                vector = np.random.randn(self.dimension)
            # Pad vector to 3D
            vector_3d = np.zeros(3)
            vector_3d[:min(3, self.dimension)] = vector[:min(3, self.dimension)]
            if self.dimension < 3:
                vector_3d[self.dimension:] = np.random.randn(3 - self.dimension) * 0.1
            vector = vector_3d
        else:
            plot_dim = min(3, self.dimension)
        
        fig = plt.figure(figsize=(15, 10))
        
        # Generate test vector if not provided
        if vector is None:
            vector = np.random.randn(self.dimension)
        
        # Use first 3 dimensions for visualization
        plot_vector = vector[:plot_dim]
        
        operators = ['I', 'N', 'R', 'C']
        
        for idx, op in enumerate(operators):
            ax = fig.add_subplot(2, 2, idx + 1, projection='3d')
            
            # Apply operator to full vector
            try:
                transformed_full = self.matrix_ops.apply_matrix(vector, op)
            except:
                # If dimension mismatch, pad vector
                if len(vector) != self.dimension:
                    if len(vector) > self.dimension:
                        vector = vector[:self.dimension]
                    else:
                        padded = np.zeros(self.dimension)
                        padded[:len(vector)] = vector
                        vector = padded
                transformed_full = self.matrix_ops.apply_matrix(vector, op)
            
            # Take first 3 dimensions for visualization
            transformed = transformed_full[:plot_dim]
            
            # Plot original vector
            ax.quiver(0, 0, 0, 
                     plot_vector[0], plot_vector[1], plot_vector[2],
                     color='blue', alpha=0.7, arrow_length_ratio=0.1,
                     label='Original', linewidth=2)
            
            # Plot transformed vector
            ax.quiver(0, 0, 0,
                     transformed[0], transformed[1], transformed[2],
                     color=self.config.operator_colors[op], alpha=0.7, 
                     arrow_length_ratio=0.1, label=f'{op} applied', linewidth=2)
            
            # Set limits
            max_val = max(np.max(np.abs(plot_vector)), np.max(np.abs(transformed))) * 1.5
            ax.set_xlim([-max_val, max_val])
            ax.set_ylim([-max_val, max_val])
            ax.set_zlim([-max_val, max_val])
            
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title(f'Operator {op}', fontsize=14, 
                        color=self.config.operator_colors[op])
            
            # Add legend
            ax.legend()
            
            # Add coordinate planes
            xx, yy = np.meshgrid([-max_val, max_val], [-max_val, max_val])
            zz = np.zeros_like(xx)
            ax.plot_surface(xx, yy, zz, alpha=0.1, color='gray')
            ax.plot_surface(xx, zz, yy, alpha=0.1, color='gray')
            ax.plot_surface(zz, xx, yy, alpha=0.1, color='gray')
        
        fig.suptitle(f'3D Vector Transformations by Klein-4 Operators\n'
                    f'Original vector (first {plot_dim} dimensions): {plot_vector}', 
                    fontsize=18, y=1.02)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        
        return fig
    
    # ------------------------------------------------------------------------
    # 2.4 PROPERTY VERIFICATION VISUALIZATIONS
    # ------------------------------------------------------------------------
    
    def plot_property_verification(self, save_path: Optional[str] = None) -> Figure:
        """
        Create comprehensive property verification dashboard
        """
        fig = plt.figure(figsize=(16, 12))
        
        # Define subplot grid
        gs = fig.add_gridspec(3, 3)
        
        # 1. Self-inverse property verification
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_self_inverse_verification(ax1)
        
        # 2. Commutativity verification
        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_commutativity_verification(ax2)
        
        # 3. Determinant verification
        ax3 = fig.add_subplot(gs[0, 2])
        self._plot_determinant_verification(ax3)
        
        # 4. Trace verification
        ax4 = fig.add_subplot(gs[1, 0])
        self._plot_trace_verification(ax4)
        
        # 5. Eigenvalue verification
        ax5 = fig.add_subplot(gs[1, 1])
        self._plot_eigenvalue_verification(ax5)
        
        # 6. Orthogonality verification
        ax6 = fig.add_subplot(gs[1, 2])
        self._plot_orthogonality_verification(ax6)
        
        # 7. Composition relationships
        ax7 = fig.add_subplot(gs[2, :])
        self._plot_composition_relationships(ax7)
        
        fig.suptitle(f'Comprehensive Klein-4 Group Property Verification\n'
                    f'Dimension: {self.dimension}', fontsize=20, y=1.02)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        
        return fig
    
    def _plot_self_inverse_verification(self, ax):
        """Helper: Plot self-inverse property verification"""
        operators = ['I', 'N', 'R', 'C']
        errors = []
        
        for op in operators:
            matrix = self.matrices[op]
            squared = matrix @ matrix
            error = np.max(np.abs(squared - np.eye(self.dimension)))
            errors.append(error)
        
        bars = ax.bar(operators, errors, color=[self.config.operator_colors[op] for op in operators])
        ax.axhline(y=1e-10, color='red', linestyle='--', alpha=0.7, label='Tolerance (1e-10)')
        
        ax.set_yscale('log')
        ax.set_ylabel('Max Error (log scale)')
        ax.set_title('Self-inverse Property: A² = I')
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend()
        
        # Add value labels
        for bar, error in zip(bars, errors):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{error:.1e}', ha='center', va='bottom', fontsize=9)
    
    def _plot_commutativity_verification(self, ax):
        """Helper: Plot commutativity verification"""
        operators = ['I', 'N', 'R', 'C']
        pairs = []
        errors = []
        
        for i, a in enumerate(operators):
            for j, b in enumerate(operators):
                if i < j:  # Avoid duplicates and self-comparisons
                    AB = self.matrices[a] @ self.matrices[b]
                    BA = self.matrices[b] @ self.matrices[a]
                    error = np.max(np.abs(AB - BA))
                    pairs.append(f'{a}{b}')
                    errors.append(error)
        
        bars = ax.bar(range(len(pairs)), errors)
        ax.axhline(y=1e-10, color='red', linestyle='--', alpha=0.7, label='Tolerance')
        
        ax.set_xticks(range(len(pairs)))
        ax.set_xticklabels(pairs, rotation=45)
        ax.set_yscale('log')
        ax.set_ylabel('Max Error (log scale)')
        ax.set_title('Commutativity: AB = BA')
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend()
    
    def _plot_determinant_verification(self, ax):
        """Helper: Plot determinant verification"""
        operators = ['I', 'N', 'R', 'C']
        determinants = []
        expected = []
        
        for op in operators:
            det = np.linalg.det(self.matrices[op])
            determinants.append(det)
            
            # Expected values
            if op == 'I':
                expected.append(1.0)
            elif op == 'N':
                expected.append((-1) ** self.dimension)
            elif op == 'R':
                expected.append((-1) ** (self.dimension * (self.dimension - 1) // 2))
            elif op == 'C':
                expected.append(((-1) ** self.dimension) * 
                               ((-1) ** (self.dimension * (self.dimension - 1) // 2)))
        
        x = np.arange(len(operators))
        width = 0.35
        
        ax.bar(x - width/2, determinants, width, label='Calculated', 
               color=[self.config.operator_colors[op] for op in operators])
        ax.bar(x + width/2, expected, width, label='Expected', alpha=0.7, color='gray')
        
        ax.set_xticks(x)
        ax.set_xticklabels(operators)
        ax.set_ylabel('Determinant')
        ax.set_title('Determinant Values')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_trace_verification(self, ax):
        """Helper: Plot trace verification"""
        operators = ['I', 'N', 'R', 'C']
        traces = []
        expected = []
        
        for op in operators:
            trace = np.trace(self.matrices[op])
            traces.append(trace)
            
            # Expected values
            if op == 'I':
                expected.append(self.dimension)
            elif op == 'N':
                expected.append(-self.dimension)
            elif op == 'R':
                expected.append(1 if self.dimension % 2 == 1 else 0)
            elif op == 'C':
                expected.append(-1 if self.dimension % 2 == 1 else 0)
        
        x = np.arange(len(operators))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, traces, width, label='Calculated',
                      color=[self.config.operator_colors[op] for op in operators])
        bars2 = ax.bar(x + width/2, expected, width, label='Expected', alpha=0.7, color='gray')
        
        ax.set_xticks(x)
        ax.set_xticklabels(operators)
        ax.set_ylabel('Trace')
        ax.set_title('Trace Values')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def _plot_eigenvalue_verification(self, ax):
        """Helper: Plot eigenvalue verification"""
        operators = ['I', 'N', 'R', 'C']
        all_eigenvalues = []
        colors = []
        
        for op in operators:
            eigenvalues = np.linalg.eigvals(self.matrices[op])
            all_eigenvalues.extend(eigenvalues)
            colors.extend([self.config.operator_colors[op]] * len(eigenvalues))
        
        # Plot eigenvalues on complex plane
        real_parts = np.real(all_eigenvalues)
        imag_parts = np.imag(all_eigenvalues)
        
        scatter = ax.scatter(real_parts, imag_parts, c=colors, s=100, alpha=0.7,
                           edgecolors='black', linewidth=1)
        
        # Unit circle
        theta = np.linspace(0, 2*np.pi, 100)
        ax.plot(np.cos(theta), np.sin(theta), '--', color='red', alpha=0.5, 
               linewidth=2, label='Unit circle')
        
        # ±1 points
        ax.scatter([1, -1], [0, 0], color='red', s=200, marker='x', 
                  linewidth=3, label='±1', zorder=5)
        
        ax.set_xlabel('Real')
        ax.set_ylabel('Imaginary')
        ax.set_title('Eigenvalues (should be ±1)')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.2)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.2)
        ax.set_aspect('equal')
        ax.legend()
        
        # Set limits
        max_val = max(np.max(np.abs(real_parts)), np.max(np.abs(imag_parts))) * 1.2
        ax.set_xlim(-max_val, max_val)
        ax.set_ylim(-max_val, max_val)
    
    def _plot_orthogonality_verification(self, ax):
        """Helper: Plot orthogonality verification"""
        operators = ['I', 'N', 'R', 'C']
        errors = []
        
        for op in operators:
            matrix = self.matrices[op]
            ortho_check = matrix @ matrix.T
            error = np.max(np.abs(ortho_check - np.eye(self.dimension)))
            errors.append(error)
        
        bars = ax.bar(operators, errors, color=[self.config.operator_colors[op] for op in operators])
        ax.axhline(y=1e-10, color='red', linestyle='--', alpha=0.7, label='Tolerance')
        
        ax.set_yscale('log')
        ax.set_ylabel('Max Error (log scale)')
        ax.set_title('Orthogonality: AAᵀ = I')
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend()
    
    def _plot_composition_relationships(self, ax):
        """Helper: Plot composition relationships"""
        # Test specific Klein-4 relations
        relations = [
            ('N', 'R', 'C', 'N∘R = C'),
            ('R', 'N', 'C', 'R∘N = C'),
            ('R', 'C', 'N', 'R∘C = N'),
            ('C', 'R', 'N', 'C∘R = N'),
            ('N', 'C', 'R', 'N∘C = R'),
            ('C', 'N', 'R', 'C∘N = R')
        ]
        
        errors = []
        labels = []
        
        for a, b, expected, label in relations:
            result = self.matrices[a] @ self.matrices[b]
            expected_matrix = self.matrices[expected]
            error = np.max(np.abs(result - expected_matrix))
            errors.append(error)
            labels.append(label)
        
        x = np.arange(len(labels))
        bars = ax.bar(x, errors)
        
        ax.axhline(y=1e-10, color='red', linestyle='--', alpha=0.7, label='Tolerance')
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_yscale('log')
        ax.set_ylabel('Max Error (log scale)')
        ax.set_title('Klein-4 Specific Relations')
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend()


# ============================================================================
# 3. DIALECTICAL PROCESS VISUALIZATIONS
# ============================================================================

class DialecticalVisualizer:
    """Visualizations for dialectical processes"""
    
    def __init__(self, engine: Optional[DialecticalEngine] = None, 
                 config: Optional[VisualConfig] = None):
        """
        Initialize dialectical visualizer
        
        Args:
            engine: DialecticalEngine instance
            config: Visualization configuration
        """
        self.engine = engine or DialecticalEngine()
        self.config = config or VisualConfig()
        
        # Apply style
        self.config.apply_style()
    
    # ------------------------------------------------------------------------
    # 3.1 PROCESS EVOLUTION VISUALIZATIONS
    # ------------------------------------------------------------------------
    
    def plot_dialectical_cycle(self, initial_thesis: List[float],
                              cycles: int = 2,
                              synthesis_method: SynthesisMethod = SynthesisMethod.DIALECTICAL,
                              save_path: Optional[str] = None) -> Figure:
        """
        Plot complete dialectical cycle evolution
        
        Shows how thesis, antithesis, and synthesis evolve through cycles
        """
        # Run dialectical cycles
        states = self.engine.run_dialectical_cycle(
            initial_thesis, 
            cycles=cycles,
            synthesis_method=synthesis_method
        )
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        
        # Extract data
        stages = [state.stage for state in states]
        theses = [state.thesis for state in states]
        antitheses = [state.antithesis for state in states]
        syntheses = [state.synthesis if state.has_synthesis else [None] * len(state.thesis) 
                    for state in states]
        
        # 1. Component evolution
        ax1 = axes[0]
        for i in range(min(3, len(initial_thesis))):  # Plot first 3 components
            ax1.plot(range(len(states)), [t[i] for t in theses], 
                    label=f'Thesis[{i}]', linestyle='-', marker='o')
            ax1.plot(range(len(states)), [a[i] for a in antitheses], 
                    label=f'Antithesis[{i}]', linestyle='--', marker='s', alpha=0.7)
            if any(s[i] is not None for s in syntheses):
                ax1.plot(range(len(states)), [s[i] if s[i] is not None else np.nan 
                        for s in syntheses], 
                        label=f'Synthesis[{i}]', linestyle=':', marker='^', alpha=0.7)
        
        ax1.set_xlabel('State Index')
        ax1.set_ylabel('Value')
        ax1.set_title('Component Evolution Through Dialectical Process')
        ax1.legend(ncol=2, fontsize=9)
        ax1.grid(True, alpha=0.3)
        
        # Mark stage transitions
        for i, stage in enumerate(stages):
            ax1.axvline(x=i, color=self.config.stage_colors[stage], 
                       alpha=0.2, linestyle='-', linewidth=3)
        
        # 2. Stage duration
        ax2 = axes[1]
        stage_counts = {}
        for stage in DialecticalStage:
            count = sum(1 for s in stages if s == stage)
            stage_counts[stage.value] = count
        
        bars = ax2.bar(stage_counts.keys(), stage_counts.values(),
                      color=[self.config.stage_colors[stage] 
                            for stage in DialecticalStage])
        ax2.set_xlabel('Stage')
        ax2.set_ylabel('Count')
        ax2.set_title('Stage Distribution')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        # 3. Tension evolution
        ax3 = axes[2]
        tensions = [self.engine.analyze_tension(state).tension_index 
                   for state in states]
        
        ax3.plot(range(len(tensions)), tensions, marker='o', linewidth=2,
                color='darkred', label='Tension Index')
        ax3.fill_between(range(len(tensions)), tensions, alpha=0.3, color='darkred')
        
        ax3.set_xlabel('State Index')
        ax3.set_ylabel('Tension Index')
        ax3.set_title('Dialectical Tension Evolution')
        ax3.set_ylim(0, 1.1)
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # Mark high and low tension points
        max_idx = np.argmax(tensions)
        min_idx = np.argmin(tensions)
        ax3.scatter([max_idx], [tensions[max_idx]], color='red', s=100, 
                   zorder=5, label=f'Max: {tensions[max_idx]:.3f}')
        ax3.scatter([min_idx], [tensions[min_idx]], color='green', s=100,
                   zorder=5, label=f'Min: {tensions[min_idx]:.3f}')
        
        # 4. Vector space trajectory (first 3 dimensions)
        ax4 = axes[3]
        if len(initial_thesis) >= 3:
            # Extract first 3 dimensions
            x = [t[0] for t in theses]
            y = [t[1] for t in theses]
            z = [t[2] for t in theses]
            
            # Create 3D plot
            from mpl_toolkits.mplot3d import Axes3D
            ax4.remove()
            ax4 = fig.add_subplot(2, 2, 4, projection='3d')
            
            # Plot trajectory
            line = ax4.plot(x, y, z, 'b-', alpha=0.5, linewidth=2, label='Trajectory')
            scatter = ax4.scatter(x, y, z, c=range(len(x)), cmap='viridis', 
                                 s=100, alpha=0.8, label='States')
            
            # Color by stage
            for i, stage in enumerate(stages):
                ax4.scatter(x[i], y[i], z[i], 
                           color=self.config.stage_colors[stage], 
                           s=150, edgecolors='black', linewidth=1.5)
            
            ax4.set_xlabel('Dimension 1')
            ax4.set_ylabel('Dimension 2')
            ax4.set_zlabel('Dimension 3')
            ax4.set_title('3D State Space Trajectory')
            ax4.legend()
            
            # Add stage labels
            for i, stage in enumerate(stages):
                if i % 2 == 0:  # Label every other state to avoid clutter
                    ax4.text(x[i], y[i], z[i], stage.value[:3], fontsize=9)
        
        else:
            # 2D plot if dimensions < 3
            dims = len(initial_thesis)
            if dims >= 2:
                x = [t[0] for t in theses]
                y = [t[1] for t in theses]
            else:
                x = range(len(states))
                y = [t[0] for t in theses]
            
            ax4.plot(x, y, 'b-', alpha=0.5, linewidth=2, label='Trajectory')
            scatter = ax4.scatter(x, y, c=range(len(x)), cmap='viridis', 
                                 s=100, alpha=0.8, label='States')
            
            # Color by stage
            for i, stage in enumerate(stages):
                ax4.scatter(x[i], y[i], color=self.config.stage_colors[stage], 
                           s=150, edgecolors='black', linewidth=1.5)
            
            ax4.set_xlabel('Dimension 1' if dims >= 2 else 'State Index')
            ax4.set_ylabel('Dimension 2' if dims >= 2 else 'Value')
            ax4.set_title(f'State Space Trajectory ({dims}D)')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        
        fig.suptitle(f'Dialectical Process Evolution\n'
                    f'Initial thesis: {initial_thesis[:3]}... | '
                    f'Cycles: {cycles} | Synthesis method: {synthesis_method.value}',
                    fontsize=16, y=1.02)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        
        return fig
    
    def plot_tension_analysis(self, state: DialecticalState,
                            save_path: Optional[str] = None) -> Figure:
        """
        Detailed tension analysis visualization
        """
        # Analyze tension
        tension = self.engine.analyze_tension(state)
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        
        # 1. Tension components
        ax1 = axes[0]
        components = ['Mean Difference', 'Max Difference', 'Mean Similarity',
                     'Tension Index', 'Correlation', 'Entropy']
        values = [
            tension.mean_difference,
            tension.max_difference,
            tension.mean_similarity,
            tension.tension_index,
            tension.correlation,
            tension.entropy
        ]
        
        colors = plt.cm.RdYlBu_r(np.linspace(0, 1, len(components)))
        bars = ax1.bar(components, values, color=colors)
        ax1.set_xticklabels(components, rotation=45, ha='right')
        ax1.set_title('Tension Components')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.3f}', ha='center', va='bottom', fontsize=9)
        
        # 2. Component-wise differences
        ax2 = axes[1]
        differences = [abs(t - a) for t, a in zip(state.thesis, state.antithesis)]
        similarities = [abs(t + a) for t, a in zip(state.thesis, state.antithesis)]
        
        x = np.arange(len(differences))
        width = 0.35
        
        ax2.bar(x - width/2, differences, width, label='Difference |t-a|', color='red')
        ax2.bar(x + width/2, similarities, width, label='Similarity |t+a|', color='blue')
        
        ax2.set_xlabel('Component Index')
        ax2.set_ylabel('Value')
        ax2.set_title('Component-wise Comparison')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. Thesis vs Antithesis scatter
        ax3 = axes[2]
        ax3.scatter(state.thesis, state.antithesis, alpha=0.7, s=100,
                   c=range(len(state.thesis)), cmap='viridis')
        ax3.plot([min(state.thesis), max(state.thesis)],
                [min(state.thesis), max(state.thesis)],
                'k--', alpha=0.5, label='y=x')
        ax3.set_xlabel('Thesis')
        ax3.set_ylabel('Antithesis')
        ax3.set_title('Thesis vs Antithesis')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_aspect('equal')
        
        # 4. Correlation visualization
        ax4 = axes[3]
        if len(state.thesis) > 1:
            import seaborn as sns
            data = pd.DataFrame({
                'Thesis': state.thesis,
                'Antithesis': state.antithesis
            })
            sns.heatmap(data.corr(), annot=True, cmap='coolwarm', 
                       center=0, ax=ax4, cbar_kws={'label': 'Correlation'})
            ax4.set_title(f'Correlation Matrix: {tension.correlation:.3f}')
        else:
            ax4.text(0.5, 0.5, 'Need at least 2 dimensions\nfor correlation matrix',
                    ha='center', va='center', transform=ax4.transAxes)
            ax4.set_title('Correlation Visualization')
        
        # 5. Radial tension plot
        ax5 = axes[4]
        angles = np.linspace(0, 2*np.pi, len(differences), endpoint=False)
        differences = np.array(differences)
        
        # Close the plot
        values = np.concatenate((differences, [differences[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        
        ax5.plot(angles, values, 'o-', linewidth=2)
        ax5.fill(angles, values, alpha=0.25)
        
        ax5.set_xticks(angles[:-1])
        ax5.set_xticklabels([f'C{i}' for i in range(len(differences))])
        ax5.set_title('Radial Difference Plot')
        ax5.grid(True)
        
        # 6. Summary metrics
        ax6 = axes[5]
        ax6.axis('off')
        
        summary_text = (
            f'Stage: {state.stage.value}\n'
            f'Dimensions: {state.dimensions}\n'
            f'Tension Index: {tension.tension_index:.3f}\n'
            f'Mean Difference: {tension.mean_difference:.3f}\n'
            f'Max Difference: {tension.max_difference:.3f}\n'
            f'Correlation: {tension.correlation:.3f}\n'
            f'Entropy: {tension.entropy:.3f}\n'
            f'Has Synthesis: {state.has_synthesis}\n'
        )
        
        ax6.text(0.1, 0.9, 'TENSION ANALYSIS SUMMARY', 
                fontsize=14, fontweight='bold', transform=ax6.transAxes)
        ax6.text(0.1, 0.7, summary_text, fontsize=11, 
                transform=ax6.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Add tension interpretation
        if tension.tension_index > 0.7:
            interpretation = 'HIGH TENSION: Strong opposition'
        elif tension.tension_index > 0.3:
            interpretation = 'MODERATE TENSION: Balanced opposition'
        else:
            interpretation = 'LOW TENSION: Similar positions'
        
        ax6.text(0.1, 0.3, interpretation, fontsize=12, fontweight='bold',
                color='darkred' if tension.tension_index > 0.7 else 
                'darkorange' if tension.tension_index > 0.3 else 'darkgreen',
                transform=ax6.transAxes)
        
        fig.suptitle(f'Detailed Tension Analysis\n'
                    f'Thesis: {state.thesis[:3]}... | '
                    f'Antithesis: {state.antithesis[:3]}...',
                    fontsize=16, y=1.02)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.config.dpi, bbox_inches='tight')
        
        return fig


# ============================================================================
# 5. EXPORT & UTILITY FUNCTIONS
# ============================================================================

class VisualizationExporter:
    """Export visualizations to various formats"""
    
    @staticmethod
    def figure_to_base64(fig: Figure) -> str:
        """Convert matplotlib figure to base64 string"""
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        return img_str
    
    @staticmethod
    def create_html_report(visualizations: Dict[str, str], 
                          title: str = "Klein-4 Visualization Report") -> str:
        """Create HTML report with embedded visualizations"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .header {{
                    text-align: center;
                    background: linear-gradient(135deg, #2E86AB, #A23B72);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                }}
                .visualization {{
                    background: white;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .vis-title {{
                    color: #2E86AB;
                    border-bottom: 2px solid #F18F01;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                    display: block;
                    margin: 0 auto;
                }}
                .grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                    gap: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{title}</h1>
                <p>Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Klein-4 Group & Dialectical Process Visualizations</p>
            </div>
            
            <div class="grid">
        """
        
        for vis_name, vis_img in visualizations.items():
            html += f"""
                <div class="visualization">
                    <h2 class="vis-title">{vis_name}</h2>
                    <img src="data:image/png;base64,{vis_img}" 
                         alt="{vis_name}" />
                </div>
            """
        
        html += """
            </div>
            
            <div style="text-align: center; margin-top: 40px; padding: 20px; 
                        background: #2E86AB; color: white; border-radius: 10px;">
                <p>Generated by Xenopoulos Dialectical Framework Visualization System</p>
                <p>Klein-4 Group: I, N, R, C | Dimension: Variable | Python Implementation</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    @staticmethod
    def save_report(visualizations: Dict[str, Figure], 
                   output_dir: str = "./visualization_output"):
        """Save all visualizations to files"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        saved_files = []
        
        for name, fig in visualizations.items():
            # Clean filename
            filename = name.lower().replace(' ', '_').replace(':', '').replace('/', '_')
            filepath = os.path.join(output_dir, f"{filename}.png")
            
            fig.savefig(filepath, dpi=300, bbox_inches='tight')
            saved_files.append(filepath)
            
            # Also save as PDF for high quality
            pdf_path = os.path.join(output_dir, f"{filename}.pdf")
            fig.savefig(pdf_path, bbox_inches='tight')
        
        # Create summary HTML
        base64_images = {}
        for name, fig in visualizations.items():
            base64_images[name] = VisualizationExporter.figure_to_base64(fig)
        
        html_report = VisualizationExporter.create_html_report(base64_images)
        html_path = os.path.join(output_dir, "visualization_report.html")
        with open(html_path, 'w') as f:
            f.write(html_report)
        saved_files.append(html_path)
        
        print(f"Saved {len(saved_files)} files to {output_dir}/")
        return saved_files


# ============================================================================
# 6. COMPREHENSIVE VISUALIZATION DASHBOARD
# ============================================================================

class Klein4VisualizationDashboard:
    """
    Complete visualization dashboard for Klein-4 dialectical system
    
    One-stop shop for all visualizations
    """
    
    def __init__(self, dimension: int = 3, 
                 config: Optional[VisualConfig] = None):
        self.dimension = dimension
        self.config = config or VisualConfig()
        self.klein4_viz = Klein4Visualizer(dimension, config)
        self.dialectical_viz = DialecticalVisualizer(config=config)
        self.exporter = VisualizationExporter()
        
        # Apply style
        self.config.apply_style()
    
    def generate_comprehensive_report(self, 
                                     initial_thesis: Optional[List[float]] = None,
                                     output_dir: str = "./visualization_report"):
        """
        Generate comprehensive visualization report
        
        Creates all possible visualizations and saves them
        """
        if initial_thesis is None:
            initial_thesis = np.random.randn(self.dimension).tolist()
        
        print(f"Generating comprehensive visualization report...")
        print(f"Dimension: {self.dimension}")
        print(f"Initial thesis: {initial_thesis}")
        print(f"Output directory: {output_dir}")
        
        all_visualizations = {}
        
        try:
            # 1. Klein-4 Group Visualizations
            print("\n1. Generating Klein-4 group visualizations...")
            
            # Cayley table
            print("  - Cayley table")
            fig1 = self.klein4_viz.plot_cayley_table()
            all_visualizations["Klein-4 Cayley Table"] = fig1
            plt.close(fig1)
            
            # Group structure
            print("  - Group structure diagram")
            fig2 = self.klein4_viz.plot_group_structure_diagram()
            all_visualizations["Group Structure Diagram"] = fig2
            plt.close(fig2)
            
            # Operator matrices
            print("  - Operator matrices")
            fig3 = self.klein4_viz.plot_operator_matrices()
            all_visualizations["Operator Matrices"] = fig3
            plt.close(fig3)
            
            # Eigenvalues
            print("  - Eigenvalue visualization")
            fig4 = self.klein4_viz.plot_matrix_eigenvalues()
            all_visualizations["Eigenvalue Analysis"] = fig4
            plt.close(fig4)
            
            # Property verification
            print("  - Property verification dashboard")
            fig5 = self.klein4_viz.plot_property_verification()
            all_visualizations["Property Verification Dashboard"] = fig5
            plt.close(fig5)
            
            # 2. Vector Transformations
            print("\n2. Generating vector transformation visualizations...")
            
            if self.dimension == 2:
                print("  - 2D vector transformations")
                fig6 = self.klein4_viz.plot_vector_transformations_2d()
                all_visualizations["2D Vector Transformations"] = fig6
                plt.close(fig6)
            else:
                print("  - 3D vector transformations")
                fig6 = self.klein4_viz.plot_vector_transformations_3d()
                all_visualizations["3D Vector Transformations"] = fig6
                plt.close(fig6)
            
            # 3. Dialectical Process Visualizations
            print("\n3. Generating dialectical process visualizations...")
            
            # Dialectical cycle
            print("  - Dialectical cycle evolution")
            fig7 = self.dialectical_viz.plot_dialectical_cycle(initial_thesis, cycles=2)
            all_visualizations["Dialectical Cycle Evolution"] = fig7
            plt.close(fig7)
            
            # Create initial state for tension analysis
            engine = DialecticalEngine()
            initial_state = engine.initialize_state(initial_thesis)
            
            # Tension analysis
            print("  - Tension analysis")
            fig8 = self.dialectical_viz.plot_tension_analysis(initial_state)
            all_visualizations["Tension Analysis"] = fig8
            plt.close(fig8)
            
        except Exception as e:
            print(f"Error during visualization generation: {e}")
            print("Continuing with available visualizations...")
        
        # 4. Save all visualizations
        print("\n4. Saving all visualizations...")
        saved_files = self.exporter.save_report(all_visualizations, output_dir)
        
        print(f"\n✅ Report generation complete!")
        print(f"📁 Saved {len(saved_files)} files to {output_dir}/")
        print(f"🌐 Open {output_dir}/visualization_report.html to view the complete report")
        
        return saved_files
    
    def create_live_dashboard(self):
        """
        Create live interactive dashboard (Jupyter compatible)
        
        Note: This is a template - implement with ipywidgets for full interactivity
        """
        print("Live Dashboard Template")
        print("=" * 60)
        print("\nFor full interactivity, install and use:")
        print("  pip install ipywidgets plotly")
        print("\nAvailable visualizations:")
        print("  1. Interactive Cayley table")
        print("  2. 3D vector transformer")
        print("  3. Dialectical process animator")
        print("  4. Property verification dashboard")
        
        return {
            'cayley_table': "Use plot_cayley_table() method",
            'vector_transformer': "Use plot_vector_transformations_3d() method"
        }


# ============================================================================
# 7. MAIN: Example Usage
# ============================================================================

if __name__ == "__main__":
    print("Klein-4 Dialectical System Visualization")
    print("=" * 60)
    
    try:
        # Create dashboard
        dashboard = Klein4VisualizationDashboard(dimension=3)
        
        # Generate comprehensive report
        initial_thesis = [1.0, 0.5, -0.3]
        saved_files = dashboard.generate_comprehensive_report(
            initial_thesis=initial_thesis,
            output_dir="./visual_output"
        )
        
        print("\n✅ Visualization system ready!")
        print("\nFor best results:")
        print("  - Use Jupyter notebooks for interactive visualizations")
        print("  - Install plotly for 3D interactivity: pip install plotly")
        print("  - Use generate_comprehensive_report() for PDF/HTML reports")
        
    except Exception as e:
        print(f"Error in main execution: {e}")
        print("\nTrying individual visualizations...")
        
        # Try individual visualizations
        try:
            # 1. Klein-4 specific visualizations
            klein4_viz = Klein4Visualizer(dimension=3)
            
            fig1 = klein4_viz.plot_cayley_table()
            plt.show()
            
            fig2 = klein4_viz.plot_operator_matrices()
            plt.show()
            
            # 2. Dialectical process visualizations
            engine = DialecticalEngine()
            initial_state = engine.initialize_state([1.0, 0.5, -0.3])
            
            dialectical_viz = DialecticalVisualizer(engine)
            
            fig3 = dialectical_viz.plot_dialectical_cycle([1.0, 0.5, -0.3], cycles=2)
            plt.show()
            
            fig4 = dialectical_viz.plot_tension_analysis(initial_state)
            plt.show()
            
            print("\n✅ Individual visualizations completed successfully!")
            
        except Exception as e2:
            print(f"Error in individual visualizations: {e2}")
            print("\nPlease check the error messages above.")