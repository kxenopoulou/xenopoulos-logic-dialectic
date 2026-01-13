"""
Dialectical Service Layer
Layer 4: High-level API and process coordination
Coordinates between engine, repositories, and external interfaces
"""

from typing import List, Dict, Optional, Any, Tuple
import uuid
import time
import json
from dataclasses import dataclass, asdict, field
from enum import Enum
from datetime import datetime
import pickle
import hashlib

from core.core_foundations import DialecticalStage
from dynamics.dialectical_engine import (
    DialecticalEngine, 
    DialecticalState,
    SynthesisMethod,
    TensionMetrics
)
from operators.inrc_operators import INRCOperatorFactory

# ============================================================================
# 1. DATA MODELS & REPOSITORY
# ============================================================================

class ProcessStatus(Enum):
    """Status of dialectical process"""
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CONVERGED = "converged"


@dataclass
class DialecticalProcess:
    """Complete dialectical process with metadata and history"""
    
    id: str
    name: str
    initial_state: DialecticalState
    current_state: DialecticalState
    states: List[DialecticalState] = field(default_factory=list)
    status: ProcessStatus = ProcessStatus.CREATED
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.states:
            self.states = [self.initial_state]
    
    @property
    def age(self) -> float:
        """Age of process in seconds"""
        return time.time() - self.created_at
    
    @property
    def dimensions(self) -> int:
        """Dimension of process state space"""
        return self.current_state.dimensions
    
    @property
    def cycle_count(self) -> int:
        """Number of completed dialectical cycles"""
        return len([s for s in self.states 
                   if s.stage == DialecticalStage.NEGATION_OF_NEGATION])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'age': self.age,
            'dimensions': self.dimensions,
            'cycle_count': self.cycle_count,
            'current_stage': self.current_state.stage.value,
            'tags': self.tags,
            'metadata': self.metadata
        }
    
    def to_json(self) -> str:
        """Serialize to JSON string"""
        data = self.to_dict()
        data['states'] = [s.to_dict() for s in self.states]
        data['initial_state'] = self.initial_state.to_dict()
        data['current_state'] = self.current_state.to_dict()
        return json.dumps(data, indent=2, default=str)
    
    def get_state_hash(self) -> str:
        """Get hash of current state for change detection"""
        state_str = json.dumps(self.current_state.to_dict(), sort_keys=True)
        return hashlib.sha256(state_str.encode()).hexdigest()[:16]


class ProcessRepository:
    """
    Repository for storing and retrieving dialectical processes
    
    In-memory implementation - can be extended to database, file, etc.
    """
    
    def __init__(self):
        self._processes: Dict[str, DialecticalProcess] = {}
        self._tags_index: Dict[str, List[str]] = {}  # tag -> process_ids
        self._status_index: Dict[ProcessStatus, List[str]] = {
            status: [] for status in ProcessStatus
        }
    
    def save(self, process: DialecticalProcess) -> None:
        """Save or update process"""
        process.updated_at = time.time()
        
        # Update indices
        old_process = self._processes.get(process.id)
        if old_process:
            # Remove from old indices
            for tag in old_process.tags:
                if tag in self._tags_index and process.id in self._tags_index[tag]:
                    self._tags_index[tag].remove(process.id)
            if old_process.status in self._status_index:
                if process.id in self._status_index[old_process.status]:
                    self._status_index[old_process.status].remove(process.id)
        
        # Add to storage
        self._processes[process.id] = process
        
        # Update indices
        for tag in process.tags:
            if tag not in self._tags_index:
                self._tags_index[tag] = []
            if process.id not in self._tags_index[tag]:
                self._tags_index[tag].append(process.id)
        
        if process.status in self._status_index:
            if process.id not in self._status_index[process.status]:
                self._status_index[process.status].append(process.id)
    
    def get(self, process_id: str) -> Optional[DialecticalProcess]:
        """Get process by ID"""
        return self._processes.get(process_id)
    
    def get_or_raise(self, process_id: str) -> DialecticalProcess:
        """Get process or raise error if not found"""
        process = self.get(process_id)
        if not process:
            raise ValueError(f"Process not found: {process_id}")
        return process
    
    def delete(self, process_id: str) -> bool:
        """Delete process by ID"""
        process = self._processes.pop(process_id, None)
        if process:
            # Remove from indices
            for tag in process.tags:
                if tag in self._tags_index and process_id in self._tags_index[tag]:
                    self._tags_index[tag].remove(process_id)
            if process.status in self._status_index:
                if process_id in self._status_index[process.status]:
                    self._status_index[process.status].remove(process_id)
            return True
        return False
    
    def find_by_tag(self, tag: str) -> List[DialecticalProcess]:
        """Find processes by tag"""
        process_ids = self._tags_index.get(tag, [])
        return [self._processes[pid] for pid in process_ids if pid in self._processes]
    
    def find_by_status(self, status: ProcessStatus) -> List[DialecticalProcess]:
        """Find processes by status"""
        process_ids = self._status_index.get(status, [])
        return [self._processes[pid] for pid in process_ids if pid in self._processes]
    
    def find_all(self, 
                tags: Optional[List[str]] = None,
                status: Optional[ProcessStatus] = None,
                min_cycles: Optional[int] = None,
                max_age: Optional[float] = None) -> List[DialecticalProcess]:
        """Find processes with filters"""
        results = list(self._processes.values())
        
        # Apply filters
        if tags:
            results = [p for p in results if any(tag in p.tags for tag in tags)]
        if status:
            results = [p for p in results if p.status == status]
        if min_cycles is not None:
            results = [p for p in results if p.cycle_count >= min_cycles]
        if max_age is not None:
            cutoff = time.time() - max_age
            results = [p for p in results if p.created_at >= cutoff]
        
        return sorted(results, key=lambda p: p.updated_at, reverse=True)
    
    def count(self) -> int:
        """Count total processes"""
        return len(self._processes)
    
    def clear(self) -> None:
        """Clear all processes"""
        self._processes.clear()
        self._tags_index.clear()
        for status in self._status_index:
            self._status_index[status].clear()
    
    def export_all(self) -> Dict[str, Any]:
        """Export all processes as serializable data"""
        return {
            'processes': [p.to_dict() for p in self._processes.values()],
            'count': self.count(),
            'exported_at': time.time(),
            'version': '1.0'
        }


# ============================================================================
# 2. CORE SERVICE
# ============================================================================

class DialecticalService:
    """
    Main service layer providing high-level dialectical operations
    
    Coordinates between engine, repository, and external interfaces
    Provides business logic, validation, and orchestration
    """
    
    def __init__(self, 
                 engine: Optional[DialecticalEngine] = None,
                 repository: Optional[ProcessRepository] = None):
        """
        Initialize service
        
        Args:
            engine: DialecticalEngine instance. If None, creates default.
            repository: ProcessRepository instance. If None, creates default.
        """
        self.engine = engine or DialecticalEngine()
        self.repository = repository or ProcessRepository()
        self._process_counters = {
            'created': 0,
            'completed': 0,
            'failed': 0
        }
    
    # ------------------------------------------------------------------------
    # PROCESS MANAGEMENT
    # ------------------------------------------------------------------------
    
    def create_process(self,
                      thesis: List[float],
                      name: Optional[str] = None,
                      antithesis: Optional[List[float]] = None,
                      tags: Optional[List[str]] = None,
                      metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Create new dialectical process
        
        Args:
            thesis: Initial thesis vector
            name: Process name. If None, generates descriptive name.
            antithesis: Optional antithesis vector. If None, uses N(thesis).
            tags: Optional tags for categorization
            metadata: Optional process metadata
            
        Returns:
            Process ID
        """
        # Generate process ID
        process_id = f"dialectical_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        # Generate name if not provided
        if not name:
            dim = len(thesis)
            name = f"Dialectical Process {self._process_counters['created'] + 1} (d={dim})"
        
        # Initialize state
        initial_state = self.engine.initialize_state(
            thesis=thesis,
            antithesis=antithesis,
            metadata={'created_by': 'dialectical_service'}
        )
        
        # Create process
        process = DialecticalProcess(
            id=process_id,
            name=name,
            initial_state=initial_state,
            current_state=initial_state,
            status=ProcessStatus.CREATED,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        # Save to repository
        self.repository.save(process)
        self._process_counters['created'] += 1
        
        return process_id
    
    def get_process(self, process_id: str) -> DialecticalProcess:
        """
        Get process by ID
        
        Args:
            process_id: Process identifier
            
        Returns:
            DialecticalProcess instance
            
        Raises:
            ValueError: If process not found
        """
        return self.repository.get_or_raise(process_id)
    
    def delete_process(self, process_id: str) -> bool:
        """
        Delete process
        
        Args:
            process_id: Process identifier
            
        Returns:
            True if deleted, False if not found
        """
        deleted = self.repository.delete(process_id)
        if deleted:
            self._process_counters['completed'] += 1
        return deleted
    
    def list_processes(self,
                      tags: Optional[List[str]] = None,
                      status: Optional[str] = None,
                      limit: Optional[int] = None,
                      offset: int = 0) -> List[Dict[str, Any]]:
        """
        List processes with optional filtering
        
        Args:
            tags: Filter by tags
            status: Filter by status (string)
            limit: Maximum number to return
            offset: Starting offset
            
        Returns:
            List of process summaries
        """
        # Convert status string to enum
        status_enum = None
        if status:
            try:
                status_enum = ProcessStatus(status)
            except ValueError:
                # Invalid status - return empty
                return []
        
        # Find processes
        processes = self.repository.find_all(
            tags=tags,
            status=status_enum
        )
        
        # Apply pagination
        end = offset + limit if limit else None
        paginated = processes[offset:end]
        
        # Convert to summary dicts
        return [p.to_dict() for p in paginated]
    
    # ------------------------------------------------------------------------
    # DIALECTICAL OPERATIONS
    # ------------------------------------------------------------------------
    
    def advance_process(self,
                       process_id: str,
                       operation: str,
                       **kwargs) -> DialecticalState:
        """
        Advance dialectical process by one operation
        
        Args:
            process_id: Process identifier
            operation: Operation to perform ('negate', 'synthesize', 'negate_negation')
            **kwargs: Operation-specific parameters
            
        Returns:
            New dialectical state
            
        Raises:
            ValueError: If process not found or operation invalid
        """
        process = self.get_process(process_id)
        
        # Update process status
        process.status = ProcessStatus.RUNNING
        self.repository.save(process)
        
        try:
            # Perform operation
            if operation == 'negate':
                intensity = kwargs.get('intensity', 1.0)
                new_state = self.engine.apply_negation(
                    process.current_state,
                    intensity=intensity
                )
            elif operation == 'synthesize':
                method_str = kwargs.get('method', 'dialectical')
                try:
                    method = SynthesisMethod(method_str)
                except ValueError:
                    method = SynthesisMethod.DIALECTICAL
                
                params = kwargs.get('parameters', {})
                new_state = self.engine.synthesize(
                    process.current_state,
                    method=method,
                    parameters=params
                )
            elif operation == 'negate_negation':
                preserve = kwargs.get('preserve_history', True)
                new_state = self.engine.negate_negation(
                    process.current_state,
                    preserve_history=preserve
                )
            else:
                raise ValueError(f"Unknown operation: {operation}")
            
            # Update process
            process.current_state = new_state
            process.states.append(new_state)
            process.status = ProcessStatus.COMPLETED
            self.repository.save(process)
            
            return new_state
            
        except Exception as e:
            # Mark as failed
            process.status = ProcessStatus.FAILED
            process.metadata['last_error'] = str(e)
            process.metadata['failed_at'] = time.time()
            self.repository.save(process)
            self._process_counters['failed'] += 1
            raise
    
    def run_cycle(self,
                 process_id: str,
                 synthesis_method: str = 'dialectical',
                 synthesis_params: Optional[Dict] = None) -> List[DialecticalState]:
        """
        Run one complete dialectical cycle
        
        Args:
            process_id: Process identifier
            synthesis_method: Synthesis method
            synthesis_params: Synthesis parameters
            
        Returns:
            List of new states generated
        """
        process = self.get_process(process_id)
        process.status = ProcessStatus.RUNNING
        self.repository.save(process)
        
        try:
            # Convert method string to enum
            try:
                method = SynthesisMethod(synthesis_method)
            except ValueError:
                method = SynthesisMethod.DIALECTICAL
            
            # Run cycle starting from current state
            new_states = []
            current_state = process.current_state
            
            # Negation
            negated = self.engine.apply_negation(current_state)
            new_states.append(negated)
            
            # Synthesis
            synthesized = self.engine.synthesize(
                negated,
                method=method,
                parameters=synthesis_params or {}
            )
            new_states.append(synthesized)
            
            # Negation of negation
            negated_negation = self.engine.negate_negation(synthesized)
            new_states.append(negated_negation)
            
            # Update process
            process.current_state = negated_negation
            process.states.extend(new_states)
            process.status = ProcessStatus.COMPLETED
            self.repository.save(process)
            
            return new_states
            
        except Exception as e:
            process.status = ProcessStatus.FAILED
            process.metadata['last_error'] = str(e)
            self.repository.save(process)
            self._process_counters['failed'] += 1
            raise
    
    def run_cycles(self,
                  process_id: str,
                  cycles: int = 3,
                  synthesis_method: str = 'dialectical',
                  synthesis_params: Optional[Dict] = None) -> List[DialecticalState]:
        """
        Run multiple dialectical cycles
        
        Args:
            process_id: Process identifier
            cycles: Number of cycles to run
            synthesis_method: Synthesis method
            synthesis_params: Synthesis parameters
            
        Returns:
            List of all new states generated
        """
        all_new_states = []
        
        for cycle in range(cycles):
            new_states = self.run_cycle(
                process_id,
                synthesis_method=synthesis_method,
                synthesis_params=synthesis_params
            )
            all_new_states.extend(new_states)
            
            # Add cycle metadata
            process = self.get_process(process_id)
            process.metadata[f'cycle_{cycle+1}_completed_at'] = time.time()
            self.repository.save(process)
        
        return all_new_states
    
    def run_until_convergence(self,
                             process_id: str,
                             max_cycles: int = 100,
                             tolerance: float = 1e-4,
                             synthesis_method: str = 'dialectical') -> Dict[str, Any]:
        """
        Run cycles until convergence
        
        Args:
            process_id: Process identifier
            max_cycles: Maximum cycles to attempt
            tolerance: Convergence tolerance
            synthesis_method: Synthesis method
            
        Returns:
            Convergence results
        """
        process = self.get_process(process_id)
        process.status = ProcessStatus.RUNNING
        self.repository.save(process)
        
        try:
            # Convert method string to enum
            try:
                method = SynthesisMethod(synthesis_method)
            except ValueError:
                method = SynthesisMethod.DIALECTICAL
            
            # Use engine's convergence method
            states, converged = self.engine.run_until_convergence(
                initial_thesis=process.current_state.thesis,
                max_cycles=max_cycles,
                tolerance=tolerance,
                synthesis_method=method
            )
            
            # Update process with new states (skip first which is current)
            if len(states) > 1:
                process.current_state = states[-1]
                process.states.extend(states[1:])  # Skip the initial state
                
                if converged:
                    process.status = ProcessStatus.CONVERGED
                    process.metadata['converged_at'] = time.time()
                    process.metadata['convergence_tolerance'] = tolerance
                else:
                    process.status = ProcessStatus.COMPLETED
                
                self.repository.save(process)
            
            return {
                'converged': converged,
                'cycles_completed': len(states) // 3,  # Each cycle = 3 states
                'final_state': process.current_state.stage.value,
                'final_tension': self.analyze_tension(process_id)['tension_index'],
                'states_generated': len(states) - 1  # Excluding initial
            }
            
        except Exception as e:
            process.status = ProcessStatus.FAILED
            process.metadata['last_error'] = str(e)
            self.repository.save(process)
            self._process_counters['failed'] += 1
            raise
    
    # ------------------------------------------------------------------------
    # ANALYSIS & METRICS
    # ------------------------------------------------------------------------
    
    def analyze_process(self, process_id: str) -> Dict[str, Any]:
        """
        Comprehensive analysis of dialectical process
        
        Args:
            process_id: Process identifier
            
        Returns:
            Analysis results
        """
        process = self.get_process(process_id)
        
        # Basic process info
        analysis = process.to_dict()
        
        # State analysis
        analysis['state_count'] = len(process.states)
        analysis['stage_distribution'] = {}
        for stage in DialecticalStage:
            count = len([s for s in process.states if s.stage == stage])
            analysis['stage_distribution'][stage.value] = count
        
        # Tension history
        tension_history = []
        for state in process.states:
            metrics = self.engine.analyze_tension(state)
            tension_history.append({
                'stage': state.stage.value,
                'tension_index': metrics.tension_index,
                'mean_difference': metrics.mean_difference,
                'correlation': metrics.correlation,
                'entropy': metrics.entropy
            })
        analysis['tension_history'] = tension_history
        
        # Current tension
        current_tension = self.engine.analyze_tension(process.current_state)
        analysis['current_tension'] = current_tension.to_dict()
        
        # Process statistics
        analysis['statistics'] = {
            'total_time': process.age,
            'states_per_second': len(process.states) / max(process.age, 1),
            'cycles_per_hour': (process.cycle_count / max(process.age, 1)) * 3600,
            'average_tension': sum(t['tension_index'] for t in tension_history) / len(tension_history),
            'tension_volatility': self._calculate_volatility([t['tension_index'] for t in tension_history])
        }
        
        return analysis
    
    def analyze_tension(self, process_id: str) -> Dict[str, float]:
        """
        Analyze current tension in process
        
        Args:
            process_id: Process identifier
            
        Returns:
            Tension metrics
        """
        process = self.get_process(process_id)
        metrics = self.engine.analyze_tension(process.current_state)
        return metrics.to_dict()
    
    def compare_processes(self, 
                         process_ids: List[str]) -> Dict[str, Any]:
        """
        Compare multiple dialectical processes
        
        Args:
            process_ids: List of process IDs
            
        Returns:
            Comparative analysis
        """
        processes = [self.get_process(pid) for pid in process_ids]
        
        comparison = {
            'process_count': len(processes),
            'processes': [p.to_dict() for p in processes],
            'comparison': {}
        }
        
        # Compare dimensions
        dimensions = [p.dimensions for p in processes]
        comparison['comparison']['dimensions'] = {
            'min': min(dimensions),
            'max': max(dimensions),
            'mean': sum(dimensions) / len(dimensions),
            'all': dimensions
        }
        
        # Compare cycle counts
        cycles = [p.cycle_count for p in processes]
        comparison['comparison']['cycles'] = {
            'min': min(cycles),
            'max': max(cycles),
            'mean': sum(cycles) / len(cycles),
            'all': cycles
        }
        
        # Compare tensions
        tensions = [self.engine.analyze_tension(p.current_state).tension_index 
                   for p in processes]
        comparison['comparison']['tensions'] = {
            'min': min(tensions),
            'max': max(tensions),
            'mean': sum(tensions) / len(tensions),
            'all': tensions
        }
        
        return comparison
    
    # ------------------------------------------------------------------------
    # BATCH OPERATIONS
    # ------------------------------------------------------------------------
    
    def batch_create(self,
                    theses: List[List[float]],
                    names: Optional[List[str]] = None,
                    tags_list: Optional[List[List[str]]] = None) -> List[str]:
        """
        Create multiple processes in batch
        
        Args:
            theses: List of thesis vectors
            names: Optional list of names
            tags_list: Optional list of tag lists
            
        Returns:
            List of process IDs
        """
        process_ids = []
        
        for i, thesis in enumerate(theses):
            name = names[i] if names and i < len(names) else None
            tags = tags_list[i] if tags_list and i < len(tags_list) else None
            
            pid = self.create_process(
                thesis=thesis,
                name=name,
                tags=tags
            )
            process_ids.append(pid)
        
        return process_ids
    
    def batch_advance(self,
                     process_ids: List[str],
                     operation: str,
                     **kwargs) -> Dict[str, Any]:
        """
        Advance multiple processes
        
        Args:
            process_ids: List of process IDs
            operation: Operation to perform
            **kwargs: Operation parameters
            
        Returns:
            Batch results
        """
        results = {
            'successful': [],
            'failed': [],
            'errors': {}
        }
        
        for pid in process_ids:
            try:
                new_state = self.advance_process(pid, operation, **kwargs)
                results['successful'].append({
                    'process_id': pid,
                    'new_stage': new_state.stage.value
                })
            except Exception as e:
                results['failed'].append(pid)
                results['errors'][pid] = str(e)
        
        return results
    
    # ------------------------------------------------------------------------
    # EXPORT & IMPORT
    # ------------------------------------------------------------------------
    
    def export_process(self, process_id: str, format: str = 'json') -> str:
        """
        Export process to serialized format
        
        Args:
            process_id: Process identifier
            format: Export format ('json' or 'pickle')
            
        Returns:
            Serialized data
        """
        process = self.get_process(process_id)
        
        if format == 'json':
            return process.to_json()
        elif format == 'pickle':
            return pickle.dumps(process)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def import_process(self, 
                      data: Any, 
                      format: str = 'json',
                      overwrite: bool = False) -> str:
        """
        Import process from serialized data
        
        Args:
            data: Serialized process data
            format: Data format ('json' or 'pickle')
            overwrite: Overwrite if process exists
            
        Returns:
            Process ID
        """
        if format == 'json':
            if isinstance(data, str):
                import_data = json.loads(data)
            else:
                import_data = data
            
            # Reconstruct process
            process = DialecticalProcess(
                id=import_data['id'],
                name=import_data['name'],
                initial_state=DialecticalState(**import_data['initial_state']),
                current_state=DialecticalState(**import_data['current_state']),
                states=[DialecticalState(**s) for s in import_data.get('states', [])],
                status=ProcessStatus(import_data['status']),
                created_at=import_data['created_at'],
                updated_at=import_data.get('updated_at', import_data['created_at']),
                metadata=import_data.get('metadata', {}),
                tags=import_data.get('tags', [])
            )
        elif format == 'pickle':
            process = pickle.loads(data)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        # Check if process exists
        existing = self.repository.get(process.id)
        if existing and not overwrite:
            raise ValueError(f"Process {process.id} already exists")
        
        # Save to repository
        self.repository.save(process)
        return process.id
    
    # ------------------------------------------------------------------------
    # UTILITY METHODS
    # ------------------------------------------------------------------------
    
    def _calculate_volatility(self, values: List[float]) -> float:
        """Calculate volatility (standard deviation) of values"""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get service statistics"""
        return {
            'process_counters': self._process_counters.copy(),
            'repository_stats': {
                'total_processes': self.repository.count(),
                'by_status': {
                    status.value: len(self.repository.find_by_status(status))
                    for status in ProcessStatus
                }
            },
            'engine_info': {
                'operator_count': len(self.engine.operators),
                'state_history_size': len(self.engine.get_state_history())
            }
        }
    
    def clear_all(self) -> None:
        """Clear all processes and reset engine"""
        self.repository.clear()
        self.engine.clear_history()
        self._process_counters = {'created': 0, 'completed': 0, 'failed': 0}
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check of service components"""
        health = {
            'service': 'healthy',
            'timestamp': time.time(),
            'components': {}
        }
        
        # Check repository
        try:
            repo_count = self.repository.count()
            health['components']['repository'] = {
                'status': 'healthy',
                'process_count': repo_count
            }
        except Exception as e:
            health['components']['repository'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health['service'] = 'degraded'
        
        # Check engine
        try:
            engine_ops = len(self.engine.operators)
            health['components']['engine'] = {
                'status': 'healthy',
                'operator_count': engine_ops
            }
        except Exception as e:
            health['components']['engine'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health['service'] = 'degraded'
        
        return health


# ============================================================================
# 3. SPECIALIZED SERVICES
# ============================================================================

class PersistentDialecticalService(DialecticalService):
    """
    Dialectical service with persistence
    
    Extends base service with file/database persistence
    """
    
    def __init__(self, 
                 storage_path: str = "./dialectical_storage",
                 engine: Optional[DialecticalEngine] = None):
        """
        Initialize with file persistence
        
        Args:
            storage_path: Directory for storing process data
            engine: DialecticalEngine instance
        """
        import os
        os.makedirs(storage_path, exist_ok=True)
        
        self.storage_path = storage_path
        super().__init__(engine=engine)
    
    def save_to_disk(self, process_id: str) -> str:
        """Save process to disk"""
        process = self.get_process(process_id)
        filepath = os.path.join(self.storage_path, f"{process_id}.json")
        
        with open(filepath, 'w') as f:
            json.dump(process.to_dict(), f, indent=2)
        
        return filepath
    
    def load_from_disk(self, filename: str) -> str:
        """Load process from disk"""
        filepath = os.path.join(self.storage_path, filename)
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return self.import_process(data, format='json')


class APIDialecticalService(DialecticalService):
    """
    Dialectical service optimized for API use
    
    Adds rate limiting, request validation, and async support
    """
    
    def __init__(self, 
                 engine: Optional[DialecticalEngine] = None,
                 rate_limit: int = 100):
        """
        Initialize API service
        
        Args:
            engine: DialecticalEngine instance
            rate_limit: Requests per minute limit
        """
        super().__init__(engine=engine)
        self.rate_limit = rate_limit
        self.request_log: List[Tuple[float, str]] = []  # (timestamp, endpoint)
    
    def _check_rate_limit(self, endpoint: str) -> bool:
        """Check if request is within rate limit"""
        now = time.time()
        minute_ago = now - 60
        
        # Remove old requests
        self.request_log = [(t, e) for t, e in self.request_log if t > minute_ago]
        
        # Count recent requests
        recent_count = len([e for t, e in self.request_log if e == endpoint])
        
        if recent_count >= self.rate_limit:
            return False
        
        # Log request
        self.request_log.append((now, endpoint))
        return True


# ============================================================================
# 4. SERVICE FACTORY
# ============================================================================

class DialecticalServiceFactory:
    """Factory for creating dialectical service instances"""
    
    @staticmethod
    def create_default_service() -> DialecticalService:
        """Create default dialectical service"""
        return DialecticalService()
    
    @staticmethod
    def create_persistent_service(storage_path: str = "./data") -> PersistentDialecticalService:
        """Create service with file persistence"""
        return PersistentDialecticalService(storage_path=storage_path)
    
    @staticmethod
    def create_api_service(rate_limit: int = 100) -> APIDialecticalService:
        """Create service optimized for API use"""
        return APIDialecticalService(rate_limit=rate_limit)
    
    @staticmethod
    def create_service_with_engine(engine: DialecticalEngine) -> DialecticalService:
        """Create service with custom engine"""
        return DialecticalService(engine=engine)


# ============================================================================
# MAIN: Example usage
# ============================================================================

if __name__ == "__main__":
    print("Testing Dialectical Service Layer...")
    
    # Create service
    service = DialecticalServiceFactory.create_default_service()
    
    # Create processes
    print("\n1. Creating dialectical processes...")
    
    process1_id = service.create_process(
        thesis=[1.0, 0.5, -0.3],
        name="Philosophical Inquiry",
        tags=["philosophy", "test"]
    )
    print(f"Created process: {process1_id}")
    
    process2_id = service.create_process(
        thesis=[0.8, -0.2, 0.4, 0.1],
        name="Scientific Theory Development",
        tags=["science", "multi-dimensional"]
    )
    print(f"Created process: {process2_id}")
    
    # List processes
    print("\n2. Listing processes:")
    processes = service.list_processes()
    for p in processes:
        print(f"  - {p['name']} (ID: {p['id'][:8]}..., Status: {p['status']})")
    
    # Run dialectical cycles
    print("\n3. Running dialectical cycles...")
    new_states = service.run_cycles(process1_id, cycles=2)
    print(f"Generated {len(new_states)} new states")
    
    # Analyze process
    print("\n4. Analyzing process:")
    analysis = service.analyze_process(process1_id)
    print(f"  Cycles completed: {analysis['cycle_count']}")
    print(f"  Current stage: {analysis['current_stage']}")
    print(f"  Current tension: {analysis['current_tension']['tension_index']:.3f}")
    
    # Compare processes
    print("\n5. Comparing processes:")
    comparison = service.compare_processes([process1_id, process2_id])
    print(f"  Dimension range: {comparison['comparison']['dimensions']['min']} to "
          f"{comparison['comparison']['dimensions']['max']}")
    print(f"  Tension range: {comparison['comparison']['tensions']['min']:.3f} to "
          f"{comparison['comparison']['tensions']['max']:.3f}")
    
    # Service statistics
    print("\n6. Service statistics:")
    stats = service.get_statistics()
    print(f"  Total processes created: {stats['process_counters']['created']}")
    print(f"  Current process count: {stats['repository_stats']['total_processes']}")
    
    # Health check
    print("\n7. Health check:")
    health = service.health_check()
    print(f"  Service status: {health['service']}")
    for component, status in health['components'].items():
        print(f"  {component}: {status['status']}")
    
    print("\n✅ Service layer test completed successfully!")