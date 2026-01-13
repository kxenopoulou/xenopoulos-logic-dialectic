"""
Factory Pattern Implementation
Central factory for creating all system components with proper configuration and validation
Ensures consistent creation, dependency injection, and initialization across the entire system
"""

from typing import Dict, Any, Optional, Type, Union
import importlib
import sys
from pathlib import Path
import json
import yaml

from core.core_foundations import AbstractGroup, AbstractOperator
from operators.inrc_operators import (
    INRCOperatorFactory, 
    IdentityOperator, 
    NegationOperator, 
    ReciprocityOperator, 
    CorrelationOperator
)
from dynamics.dialectical_engine import DialecticalEngine, ConservativeDialecticalEngine, RadicalDialecticalEngine
from services.dialectical_service import DialecticalService, PersistentDialecticalService, APIDialecticalService
from validation.mathematical_validator import MathematicalValidator

# ============================================================================
# 1. CONFIGURATION MANAGEMENT
# ============================================================================

class SystemConfig:
    """
    System-wide configuration management
    Supports multiple configuration sources and validation
    """
    
    DEFAULT_CONFIG = {
        'system': {
            'name': 'Xenopoulos Dialectical Framework',
            'version': '1.0.0',
            'description': 'Mathematical implementation of Piaget\'s INRC operators as Klein-4 group'
        },
        'operators': {
            'dimension': 3,
            'validation_tolerance': 1e-12,
            'enable_matrix_representations': True,
            'enable_pure_python_mode': True
        },
        'engine': {
            'default_synthesis_method': 'dialectical',
            'convergence_tolerance': 1e-6,
            'max_convergence_cycles': 100,
            'enable_history_tracking': True
        },
        'service': {
            'default_repository_type': 'memory',
            'persistence_path': './dialectical_data',
            'api_rate_limit': 100,
            'enable_batch_operations': True
        },
        'validation': {
            'run_on_startup': True,
            'generate_reports': True,
            'report_format': 'all',  # console, json, markdown
            'validation_tolerance': 1e-10
        }
    }
    
    def __init__(self, config_source: Optional[Union[str, Dict, Path]] = None):
        """
        Initialize configuration
        
        Args:
            config_source: Configuration source - can be:
                - Dict: Direct configuration dictionary
                - str: Path to JSON/YAML config file
                - Path: Path object to config file
                - None: Use default configuration
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_source is not None:
            if isinstance(config_source, dict):
                self._merge_config(config_source)
            else:
                self._load_config_file(config_source)
    
    def _load_config_file(self, filepath: Union[str, Path]):
        """Load configuration from file"""
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")
        
        if path.suffix.lower() == '.json':
            with open(path, 'r') as f:
                file_config = json.load(f)
        elif path.suffix.lower() in ['.yaml', '.yml']:
            try:
                import yaml
                with open(path, 'r') as f:
                    file_config = yaml.safe_load(f)
            except ImportError:
                raise ImportError("PyYAML required for YAML config files")
        else:
            raise ValueError(f"Unsupported config file format: {path.suffix}")
        
        self._merge_config(file_config)
    
    def _merge_config(self, new_config: Dict[str, Any]):
        """Merge new configuration into existing (deep merge)"""
        def merge_dicts(d1: Dict, d2: Dict) -> Dict:
            for key, value in d2.items():
                if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
                    d1[key] = merge_dicts(d1[key], value)
                else:
                    d1[key] = value
            return d1
        
        self.config = merge_dicts(self.config, new_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self.config
        
        # Navigate to parent
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set value
        config[keys[-1]] = value
    
    def save(self, filepath: Union[str, Path], format: str = 'json'):
        """Save configuration to file"""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'json':
            with open(path, 'w') as f:
                json.dump(self.config, f, indent=2)
        elif format == 'yaml':
            try:
                import yaml
                with open(path, 'w') as f:
                    yaml.dump(self.config, f, default_flow_style=False)
            except ImportError:
                raise ImportError("PyYAML required for YAML format")
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def validate(self) -> bool:
        """Validate configuration"""
        # Check required settings
        required = [
            'operators.dimension',
            'engine.default_synthesis_method',
            'validation.run_on_startup'
        ]
        
        for req in required:
            if self.get(req) is None:
                return False
        
        # Validate dimension
        dimension = self.get('operators.dimension')
        if not isinstance(dimension, int) or dimension < 2:
            return False
        
        # Validate synthesis method
        valid_methods = ['standard', 'geometric', 'dialectical', 'harmonic', 'max_tension', 'min_tension']
        method = self.get('engine.default_synthesis_method')
        if method not in valid_methods:
            return False
        
        return True
    
    def __repr__(self) -> str:
        return f"SystemConfig(valid={self.validate()}, dimension={self.get('operators.dimension')})"


# ============================================================================
# 2. COMPONENT REGISTRY
# ============================================================================

class ComponentRegistry:
    """
    Registry for managing component instances and dependencies
    Implements singleton pattern for shared components
    """
    
    _instance = None
    _components: Dict[str, Any] = {}
    _dependencies: Dict[str, List[str]] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def register(cls, name: str, component: Any, dependencies: Optional[List[str]] = None):
        """Register a component"""
        cls._components[name] = component
        if dependencies:
            cls._dependencies[name] = dependencies
    
    @classmethod
    def get(cls, name: str) -> Any:
        """Get a registered component"""
        if name not in cls._components:
            raise KeyError(f"Component not registered: {name}")
        return cls._components[name]
    
    @classmethod
    def has(cls, name: str) -> bool:
        """Check if component is registered"""
        return name in cls._components
    
    @classmethod
    def resolve_dependencies(cls, component_name: str) -> Dict[str, Any]:
        """Resolve and return dependencies for a component"""
        if component_name not in cls._dependencies:
            return {}
        
        dependencies = {}
        for dep_name in cls._dependencies[component_name]:
            if dep_name in cls._components:
                dependencies[dep_name] = cls._components[dep_name]
            else:
                raise ValueError(f"Dependency not found: {dep_name} for {component_name}")
        
        return dependencies
    
    @classmethod
    def clear(cls):
        """Clear all registered components"""
        cls._components.clear()
        cls._dependencies.clear()
    
    @classmethod
    def list_components(cls) -> Dict[str, str]:
        """List all registered components with their types"""
        return {
            name: type(component).__name__
            for name, component in cls._components.items()
        }


# ============================================================================
# 3. MAIN FACTORY CLASS
# ============================================================================

class DialecticalFactory:
    """
    Main factory class for creating all system components
    
    Responsibilities:
    1. Create properly configured components
    2. Manage dependencies between components
    3. Ensure validation on creation
    4. Support different creation modes (default, custom, from config)
    """
    
    def __init__(self, config: Optional[SystemConfig] = None):
        """
        Initialize factory
        
        Args:
            config: System configuration. If None, uses default.
        """
        self.config = config or SystemConfig()
        self.registry = ComponentRegistry()
        
        # Validate configuration
        if not self.config.validate():
            raise ValueError("Invalid system configuration")
        
        # Run startup validation if configured
        if self.config.get('validation.run_on_startup'):
            self._run_startup_validation()
    
    # ------------------------------------------------------------------------
    # CORE COMPONENT FACTORIES
    # ------------------------------------------------------------------------
    
    def create_operators(self, 
                        dimension: Optional[int] = None,
                        validate: bool = True) -> Dict[str, AbstractOperator]:
        """
        Create INRC operators
        
        Args:
            dimension: Dimension for operators. If None, uses config.
            validate: Whether to validate operators on creation
            
        Returns:
            Dictionary of INRC operators
        """
        dimension = dimension or self.config.get('operators.dimension', 3)
        
        if dimension < 2:
            raise ValueError(f"Dimension must be ≥ 2, got {dimension}")
        
        # Create operator factory
        op_factory = INRCOperatorFactory()
        
        if validate:
            operators = op_factory.create_with_validation()
        else:
            operators = op_factory.create_operators()
        
        # Register in component registry
        self.registry.register('operators', operators)
        
        # Create matrix representations if enabled
        if self.config.get('operators.enable_matrix_representations', True):
            matrix_ops = op_factory.create_matrix_operators(dimension)
            self.registry.register('matrix_operators', matrix_ops)
        
        return operators
    
    def create_engine(self,
                     engine_type: str = 'standard',
                     custom_operators: Optional[Dict[str, AbstractOperator]] = None) -> DialecticalEngine:
        """
        Create dialectical engine
        
        Args:
            engine_type: Type of engine ('standard', 'conservative', 'radical', 'custom')
            custom_operators: Custom operators to use (for 'custom' type)
            
        Returns:
            Configured dialectical engine
        """
        # Get or create operators
        if custom_operators:
            operators = custom_operators
        else:
            operators = self.registry.get('operators') if self.registry.has('operators') \
                       else self.create_operators()
        
        # Create appropriate engine type
        if engine_type == 'standard':
            engine = DialecticalEngine(INRCOperatorFactory())
        elif engine_type == 'conservative':
            engine = ConservativeDialecticalEngine(INRCOperatorFactory())
        elif engine_type == 'radical':
            engine = RadicalDialecticalEngine(INRCOperatorFactory())
        elif engine_type == 'custom':
            if not custom_operators:
                raise ValueError("Custom operators required for custom engine type")
            # Create custom factory with provided operators
            class CustomOperatorFactory:
                @staticmethod
                def create_with_validation():
                    return custom_operators
            engine = DialecticalEngine(CustomOperatorFactory())
        else:
            raise ValueError(f"Unknown engine type: {engine_type}")
        
        # Configure engine
        engine_type_config = self.config.get(f'engine.{engine_type}', {})
        if isinstance(engine_type_config, dict):
            # Apply configuration to engine if it has settable attributes
            for key, value in engine_type_config.items():
                if hasattr(engine, key):
                    setattr(engine, key, value)
        
        # Register in component registry
        self.registry.register('engine', engine, dependencies=['operators'])
        
        return engine
    
    def create_service(self,
                      service_type: str = 'default',
                      custom_engine: Optional[DialecticalEngine] = None) -> DialecticalService:
        """
        Create dialectical service
        
        Args:
            service_type: Type of service ('default', 'persistent', 'api', 'custom')
            custom_engine: Custom engine to use (for 'custom' type)
            
        Returns:
            Configured dialectical service
        """
        # Get or create engine
        if custom_engine:
            engine = custom_engine
        else:
            engine = self.registry.get('engine') if self.registry.has('engine') \
                    else self.create_engine()
        
        # Create appropriate service type
        if service_type == 'default':
            service = DialecticalService(engine=engine)
        elif service_type == 'persistent':
            storage_path = self.config.get('service.persistence_path', './dialectical_data')
            service = PersistentDialecticalService(
                storage_path=storage_path,
                engine=engine
            )
        elif service_type == 'api':
            rate_limit = self.config.get('service.api_rate_limit', 100)
            service = APIDialecticalService(
                engine=engine,
                rate_limit=rate_limit
            )
        elif service_type == 'custom':
            if not custom_engine:
                raise ValueError("Custom engine required for custom service type")
            service = DialecticalService(engine=custom_engine)
        else:
            raise ValueError(f"Unknown service type: {service_type}")
        
        # Configure service
        service_type_config = self.config.get(f'service.{service_type}', {})
        if isinstance(service_type_config, dict):
            for key, value in service_type_config.items():
                if hasattr(service, key):
                    setattr(service, key, value)
        
        # Register in component registry
        self.registry.register('service', service, dependencies=['engine'])
        
        return service
    
    def create_validator(self,
                        tolerance: Optional[float] = None) -> MathematicalValidator:
        """
        Create mathematical validator
        
        Args:
            tolerance: Validation tolerance. If None, uses config.
            
        Returns:
            Configured mathematical validator
        """
        tolerance = tolerance or self.config.get('validation.validation_tolerance', 1e-10)
        validator = MathematicalValidator(tolerance=tolerance)
        
        # Register in component registry
        self.registry.register('validator', validator)
        
        return validator
    
    # ------------------------------------------------------------------------
    # COMPOSITE FACTORIES (Complete systems)
    # ------------------------------------------------------------------------
    
    def create_complete_system(self,
                              dimension: Optional[int] = None,
                              engine_type: str = 'standard',
                              service_type: str = 'default',
                              validate: bool = True) -> Dict[str, Any]:
        """
        Create complete dialectical system
        
        Args:
            dimension: System dimension
            engine_type: Type of dialectical engine
            service_type: Type of service layer
            validate: Whether to validate the complete system
            
        Returns:
            Dictionary containing all system components
        """
        # Update config if dimension provided
        if dimension is not None:
            self.config.set('operators.dimension', dimension)
        
        # Create all components
        operators = self.create_operators(validate=validate)
        engine = self.create_engine(engine_type=engine_type)
        service = self.create_service(service_type=service_type)
        validator = self.create_validator()
        
        # Validate complete system if requested
        if validate:
            validation_result = validator.run_comprehensive_validation()
            
            if validation_result.success_rate < 1.0:
                failed_tests = [
                    t.name for t in validation_result.tests 
                    if not t.passed()
                ]
                warnings.warn(
                    f"System validation passed {validation_result.passed_count}/"
                    f"{validation_result.total_count} tests. "
                    f"Failed: {', '.join(failed_tests[:3])}"
                )
        
        system = {
            'config': self.config,
            'operators': operators,
            'engine': engine,
            'service': service,
            'validator': validator,
            'registry': self.registry
        }
        
        # Register complete system
        self.registry.register('complete_system', system, 
                              dependencies=['operators', 'engine', 'service', 'validator'])
        
        return system
    
    def create_from_config_file(self, config_file: Union[str, Path]) -> Dict[str, Any]:
        """
        Create complete system from configuration file
        
        Args:
            config_file: Path to configuration file
            
        Returns:
            Complete system configured from file
        """
        # Load configuration
        config = SystemConfig(config_file)
        self.config = config
        
        # Create system using configuration
        dimension = config.get('operators.dimension', 3)
        engine_type = config.get('engine.type', 'standard')
        service_type = config.get('service.type', 'default')
        
        return self.create_complete_system(
            dimension=dimension,
            engine_type=engine_type,
            service_type=service_type,
            validate=config.get('validation.run_on_startup', True)
        )
    
    # ------------------------------------------------------------------------
    # SPECIALIZED FACTORIES
    # ------------------------------------------------------------------------
    
    def create_batch_system(self,
                           count: int = 3,
                           dimensions: Optional[List[int]] = None) -> List[DialecticalService]:
        """
        Create multiple independent systems for batch processing
        
        Args:
            count: Number of systems to create
            dimensions: List of dimensions for each system
            
        Returns:
            List of independent dialectical services
        """
        services = []
        
        for i in range(count):
            # Use provided dimension or generate
            if dimensions and i < len(dimensions):
                dimension = dimensions[i]
            else:
                dimension = self.config.get('operators.dimension', 3) + i
            
            # Create independent factory for each system
            factory = DialecticalFactory(self.config)
            system = factory.create_complete_system(dimension=dimension)
            services.append(system['service'])
        
        return services
    
    def create_research_environment(self,
                                   dimensions: List[int] = [2, 3, 4, 5],
                                   engine_types: List[str] = ['standard', 'conservative', 'radical']) -> Dict[str, Any]:
        """
        Create research environment with multiple configurations
        
        Args:
            dimensions: List of dimensions to test
            engine_types: List of engine types to compare
            
        Returns:
            Research environment with multiple systems
        """
        environment = {
            'dimensions': {},
            'engines': {},
            'comparisons': []
        }
        
        # Test each dimension
        for dim in dimensions:
            self.config.set('operators.dimension', dim)
            system = self.create_complete_system(dimension=dim, validate=False)
            environment['dimensions'][dim] = system
        
        # Test each engine type (using first dimension)
        base_dim = dimensions[0] if dimensions else 3
        for engine_type in engine_types:
            self.config.set('operators.dimension', base_dim)
            system = self.create_complete_system(
                dimension=base_dim,
                engine_type=engine_type,
                validate=False
            )
            environment['engines'][engine_type] = system
        
        # Create validator for comparisons
        validator = self.create_validator()
        
        # Run comparative validation
        for dim, system in environment['dimensions'].items():
            validation = validator.validate_dimensional_consistency(max_dim=dim)
            environment['comparisons'].append({
                'dimension': dim,
                'validation': validation
            })
        
        return environment
    
    # ------------------------------------------------------------------------
    # UTILITY METHODS
    # ------------------------------------------------------------------------
    
    def _run_startup_validation(self):
        """Run startup validation if configured"""
        validator = self.create_validator()
        suite = validator.run_comprehensive_validation()
        
        if self.config.get('validation.generate_reports', True):
            report_format = self.config.get('validation.report_format', 'console')
            
            if report_format in ['console', 'all']:
                from validation.mathematical_validator import ValidationReporter
                ValidationReporter.console_report(suite)
            
            if report_format in ['json', 'all']:
                import json
                report = ValidationReporter.json_report(suite)
                report_path = Path('./validation_reports/startup_validation.json')
                report_path.parent.mkdir(exist_ok=True)
                report_path.write_text(report)
            
            if report_format in ['markdown', 'all']:
                report = ValidationReporter.markdown_report(
                    suite, 
                    './validation_reports/startup_validation.md'
                )
        
        if suite.success_rate < 1.0:
            warnings.warn(
                f"Startup validation passed {suite.passed_count}/{suite.total_count} tests. "
                "Some components may not be mathematically correct."
            )
    
    def get_component_tree(self) -> Dict[str, Any]:
        """Get dependency tree of all created components"""
        tree = {}
        
        for name, component in self.registry._components.items():
            deps = self.registry._dependencies.get(name, [])
            tree[name] = {
                'type': type(component).__name__,
                'dependencies': deps,
                'has_dependencies': bool(deps)
            }
        
        return tree
    
    def export_configuration(self, filepath: Union[str, Path], format: str = 'json'):
        """Export current configuration to file"""
        self.config.save(filepath, format)
    
    def reset(self):
        """Reset factory to initial state"""
        self.registry.clear()
        self.config = SystemConfig()


# ============================================================================
# 4. GLOBAL FACTORY INSTANCE
# ============================================================================

# Global factory instance for easy access
_default_factory = None

def get_default_factory() -> DialecticalFactory:
    """Get or create default factory instance (singleton)"""
    global _default_factory
    if _default_factory is None:
        _default_factory = DialecticalFactory()
    return _default_factory

def create_default_system(**kwargs) -> Dict[str, Any]:
    """Create default system using global factory"""
    factory = get_default_factory()
    return factory.create_complete_system(**kwargs)

def reset_default_factory():
    """Reset global factory to default state"""
    global _default_factory
    _default_factory = None


# ============================================================================
# 5. CONFIGURATION TEMPLATES
# ============================================================================

class ConfigTemplates:
    """Pre-defined configuration templates for common use cases"""
    
    @staticmethod
    def research_template() -> Dict[str, Any]:
        """Configuration template for research use"""
        return {
            'system': {
                'name': 'Xenopoulos Research Environment',
                'description': 'Configuration for academic research and experimentation'
            },
            'operators': {
                'dimension': 4,
                'validation_tolerance': 1e-14,
                'enable_matrix_representations': True,
                'enable_pure_python_mode': True
            },
            'engine': {
                'default_synthesis_method': 'dialectical',
                'convergence_tolerance': 1e-8,
                'max_convergence_cycles': 1000,
                'enable_history_tracking': True
            },
            'service': {
                'default_repository_type': 'persistent',
                'persistence_path': './research_data',
                'enable_batch_operations': True
            },
            'validation': {
                'run_on_startup': True,
                'generate_reports': True,
                'report_format': 'all',
                'validation_tolerance': 1e-12
            }
        }
    
    @staticmethod
    def production_template() -> Dict[str, Any]:
        """Configuration template for production use"""
        return {
            'system': {
                'name': 'Xenopoulos Production System',
                'description': 'Configuration for production deployment'
            },
            'operators': {
                'dimension': 3,
                'validation_tolerance': 1e-10,
                'enable_matrix_representations': True,
                'enable_pure_python_mode': False  # Prefer numpy for performance
            },
            'engine': {
                'default_synthesis_method': 'standard',
                'convergence_tolerance': 1e-6,
                'max_convergence_cycles': 100,
                'enable_history_tracking': False  # Disable for performance
            },
            'service': {
                'default_repository_type': 'memory',
                'api_rate_limit': 1000,
                'enable_batch_operations': True
            },
            'validation': {
                'run_on_startup': False,  # Disable in production
                'generate_reports': False,
                'validation_tolerance': 1e-8
            }
        }
    
    @staticmethod
    def education_template() -> Dict[str, Any]:
        """Configuration template for educational use"""
        return {
            'system': {
                'name': 'Xenopoulos Educational Edition',
                'description': 'Configuration for teaching and learning'
            },
            'operators': {
                'dimension': 2,  # 2D for visualization
                'validation_tolerance': 1e-6,
                'enable_matrix_representations': True,
                'enable_pure_python_mode': True  # For clarity
            },
            'engine': {
                'default_synthesis_method': 'geometric',
                'convergence_tolerance': 0.01,
                'max_convergence_cycles': 10,
                'enable_history_tracking': True
            },
            'service': {
                'default_repository_type': 'memory',
                'enable_batch_operations': False
            },
            'validation': {
                'run_on_startup': True,
                'generate_reports': True,
                'report_format': 'console',
                'validation_tolerance': 1e-6
            }
        }


# ============================================================================
# 6. MAIN: Example usage
# ============================================================================

if __name__ == "__main__":
    print("Testing Dialectical Factory...")
    
    # Example 1: Create default system
    print("\n1. Creating default system:")
    factory = DialecticalFactory()
    system = factory.create_complete_system()
    
    print(f"  Created system with:")
    print(f"    • Dimension: {factory.config.get('operators.dimension')}")
    print(f"    • Engine: {type(system['engine']).__name__}")
    print(f"    • Service: {type(system['service']).__name__}")
    
    # Example 2: Use global factory
    print("\n2. Using global factory:")
    default_system = create_default_system()
    print(f"  Default system created via global factory")
    
    # Example 3: Create from configuration template
    print("\n3. Creating research environment:")
    research_config = ConfigTemplates.research_template()
    research_factory = DialecticalFactory(research_config)
    research_env = research_factory.create_research_environment(
        dimensions=[2, 3, 4],
        engine_types=['standard', 'conservative']
    )
    print(f"  Research environment created with {len(research_env['dimensions'])} dimensions")
    
    # Example 4: Show component tree
    print("\n4. Component dependency tree:")
    tree = factory.get_component_tree()
    for name, info in tree.items():
        deps = ', '.join(info['dependencies']) if info['dependencies'] else 'none'
        print(f"  {name} ({info['type']}) -> depends on: {deps}")
    
    # Example 5: Export configuration
    print("\n5. Exporting configuration...")
    factory.export_configuration('./example_config.json')
    print("  Configuration exported to example_config.json")
    
    print("\n✅ Factory pattern implementation test completed successfully!")