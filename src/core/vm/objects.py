"""
Pyrl VM Objects

Object-oriented programming support for Pyrl including:
- PyrlFunction: User-defined functions
- PyrlClass: Class definitions
- PyrlInstance: Class instances
- PyrlMethod: Bound methods
"""
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from .environment import Environment
    from .vm import PyrlVM

from .exceptions import ReturnValue, PyrlRuntimeError


# ===========================================
# User-defined Function
# ===========================================

@dataclass
class PyrlFunction:
    """User-defined Pyrl function.
    
    Represents a function defined in Pyrl code using the `def` keyword.
    Functions capture their defining environment (closure) for variable access.
    
    Attributes:
        name: Function name
        params: List of parameter names (with sigils)
        body: List of AST nodes representing the function body
        closure: Environment captured at function definition time
    """
    name: str
    params: List[str]
    body: List[Any]
    closure: 'Environment'

    def __call__(self, *args):
        """Execute the function with given arguments."""
        # Create new environment with closure
        from .environment import Environment
        local_env = Environment(parent=self.closure)
        
        # Ensure local_env has vm reference
        if self.closure and self.closure.vm:
            local_env.vm = self.closure.vm

        # Bind parameters
        for i, param in enumerate(self.params):
            # Handle both old format (string) and new format (tuple)
            if isinstance(param, tuple):
                param_name, param_type = param
            else:
                # Old format: just a string name
                param_name = param if param.startswith(('$', '@', '%', '&')) else '$' + param
                param_type = 'scalar'
            
            if i < len(args):
                local_env.define(param_name, args[i])
            else:
                local_env.define(param_name, None)

        # Execute body
        try:
            result = None
            for stmt in self.body:
                result = self.closure.vm.execute(stmt, local_env)
            return result
        except ReturnValue as ret:
            return ret.value


# ===========================================
# Class Definition
# ===========================================

class PyrlClass:
    """Pyrl class definition.
    
    Represents a class defined in Pyrl code. Classes can have:
    - Properties (declared with `prop`)
    - Methods (declared with `method`)
    - An init method (constructor)
    - Optional parent class (extends)
    
    Attributes:
        name: Class name
        extends: Optional parent class name
        methods: Dict of method definitions
        properties: Dict of property definitions
        closure: Environment captured at class definition time
    """
    
    def __init__(self, name: str, extends: Optional[str] = None,
                 methods: Dict[str, Any] = None, properties: Dict[str, Any] = None,
                 closure: 'Environment' = None):
        self.name = name
        self.extends = extends
        self.methods = methods or {}
        self.properties = properties or {}
        self.closure = closure
    
    def __call__(self, *args, **kwargs):
        """Create a new instance of the class."""
        instance = PyrlInstance(self)
        
        # Call init method if it exists
        if 'init' in self.methods:
            init_method = self.methods['init']
            if hasattr(init_method, 'params'):  # Is a MethodDef
                # Create bound method
                bound_init = PyrlMethod(
                    name='init',
                    params=init_method.params,
                    body=init_method.body,
                    instance=instance,
                    closure=self.closure
                )
                bound_init(*args)
        
        return instance
    
    def get_method(self, name: str) -> Optional['PyrlMethod']:
        """Get a method by name (unbound).
        
        Args:
            name: Method name
            
        Returns:
            PyrlMethod or None if not found
        """
        if name in self.methods:
            method_def = self.methods[name]
            if hasattr(method_def, 'params'):
                return PyrlMethod(
                    name=name,
                    params=method_def.params,
                    body=method_def.body,
                    instance=None,
                    closure=self.closure
                )
        return None
    
    def __repr__(self):
        return f"<class {self.name}>"


# ===========================================
# Class Instance
# ===========================================

class PyrlInstance:
    """Instance of a Pyrl class.
    
    Represents an instance created from a PyrlClass. Instances have:
    - A reference to their class
    - Property values stored in _properties dict
    
    Attributes:
        _class: The PyrlClass this is an instance of
        _properties: Dict of property values
    """
    
    def __init__(self, cls: PyrlClass):
        self._class = cls
        self._properties = {}
        
        # Initialize properties from class definition
        for name, prop_def in cls.properties.items():
            if prop_def is not None:
                if hasattr(prop_def, 'value'):  # Is a PropertyDef
                    self._properties[name] = prop_def.value
                else:
                    self._properties[name] = prop_def
    
    def get_property(self, name: str) -> Any:
        """Get a property value.
        
        Args:
            name: Property name
            
        Returns:
            Property value
            
        Raises:
            PyrlRuntimeError: If property not found
        """
        if name in self._properties:
            return self._properties[name]
        raise PyrlRuntimeError(f"Property '{name}' not found on {self._class.name}")
    
    def set_property(self, name: str, value: Any) -> None:
        """Set a property value.
        
        Args:
            name: Property name
            value: New value
        """
        self._properties[name] = value
    
    def get_method(self, name: str) -> 'PyrlMethod':
        """Get a bound method.
        
        Args:
            name: Method name
            
        Returns:
            Bound PyrlMethod
            
        Raises:
            PyrlRuntimeError: If method not found
        """
        if name in self._class.methods:
            method_def = self._class.methods[name]
            if hasattr(method_def, 'params'):
                return PyrlMethod(
                    name=name,
                    params=method_def.params,
                    body=method_def.body,
                    instance=self,
                    closure=self._class.closure
                )
        raise PyrlRuntimeError(f"Method '{name}' not found on {self._class.name}")
    
    def __repr__(self):
        return f"<{self._class.name} instance>"


# ===========================================
# Bound Method
# ===========================================

class PyrlMethod:
    """Bound method on a Pyrl instance.
    
    Represents a method bound to a specific instance. When called,
    the instance is available as 'self' or '$self' in the method body.
    
    Attributes:
        name: Method name
        params: List of parameter names
        body: List of AST nodes for method body
        instance: The PyrlInstance this method is bound to (or None for unbound)
        closure: Environment captured at definition time
    """
    
    def __init__(self, name: str, params: List[str], body: List[Any],
                 instance: Optional[PyrlInstance], closure: 'Environment'):
        self.name = name
        self.params = params
        self.body = body
        self.instance = instance
        self.closure = closure
    
    def __call__(self, *args):
        """Execute the method with given arguments."""
        from .environment import Environment
        local_env = Environment(parent=self.closure)
        
        # Bind 'self' or '$self' if instance exists
        if self.instance:
            local_env.define('self', self.instance)
            local_env.define('$self', self.instance)
            # Also bind the instance's properties to the local environment
            for prop_name, prop_value in self.instance._properties.items():
                local_env.define('$' + prop_name, prop_value)
        
        # Bind parameters
        for i, param in enumerate(self.params):
            # Handle both old format (string) and new format (tuple)
            if isinstance(param, tuple):
                param_name, param_type = param
            else:
                # Old format: just a string name
                param_name = param if param.startswith(('$', '@', '%', '&')) else '$' + param
                param_type = 'scalar'
            
            if i < len(args):
                local_env.define(param_name, args[i])
            else:
                local_env.define(param_name, None)
        
        # Execute body
        try:
            result = None
            for stmt in self.body:
                result = self.closure.vm.execute(stmt, local_env)
                # Update instance properties after each statement
                if self.instance:
                    for prop_name in self.instance._class.properties.keys():
                        var_name = '$' + prop_name
                        if local_env.has(var_name):
                            self.instance._properties[prop_name] = local_env.get(var_name)
            return result
        except ReturnValue as ret:
            # Update instance properties before returning
            if self.instance:
                for prop_name in self.instance._class.properties.keys():
                    var_name = '$' + prop_name
                    if local_env.has(var_name):
                        self.instance._properties[prop_name] = local_env.get(var_name)
            return ret.value
    
    def __repr__(self):
        if self.instance:
            return f"<bound method {self.name} of {self.instance}>"
        return f"<unbound method {self.name}>"
