"""
Pyrl VM Environment

Variable environment with lexical scoping support for the Pyrl VM.
"""
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .vm import PyrlVM


class Environment:
    """Variable environment with scoping.
    
    The Environment class implements lexical scoping for Pyrl variables.
    Each environment has a reference to its parent environment (if any),
    creating a scope chain for variable lookup.
    
    Attributes:
        variables: Dictionary mapping variable names to their values
        parent: Reference to the parent environment (for nested scopes)
        vm: Reference to the PyrlVM instance (for executing code)
    
    Example:
        >>> env = Environment()
        >>> env.define('$x', 10)
        >>> env.get('$x')
        10
        >>> child = Environment(parent=env)
        >>> child.get('$x')  # Looks up in parent
        10
    """

    def __init__(self, parent: Optional['Environment'] = None):
        """Initialize a new environment.
        
        Args:
            parent: Optional parent environment for nested scopes
        """
        self.variables: Dict[str, Any] = {}
        self.parent = parent
        self.vm: Optional['PyrlVM'] = None

    def define(self, name: str, value: Any) -> None:
        """Define a new variable in the current scope.
        
        Args:
            name: Variable name (with sigil prefix, e.g., '$x', '@arr', '%hash')
            value: Variable value
        """
        self.variables[name] = value

    def get(self, name: str) -> Any:
        """Get a variable value, searching up the scope chain.
        
        Args:
            name: Variable name (with sigil prefix)
            
        Returns:
            The variable's value
            
        Raises:
            PyrlRuntimeError: If the variable is not defined
        """
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        from .exceptions import PyrlRuntimeError
        raise PyrlRuntimeError(f"Undefined variable: {name}")

    def set(self, name: str, value: Any) -> None:
        """Set a variable value, searching up the scope chain.
        
        If the variable exists in an ancestor scope, it will be updated there.
        Otherwise, it will be created in the current scope.
        
        Args:
            name: Variable name (with sigil prefix)
            value: New value for the variable
        """
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            # Create new variable in current scope
            self.variables[name] = value

    def has(self, name: str) -> bool:
        """Check if a variable exists in the scope chain.
        
        Args:
            name: Variable name (with sigil prefix)
            
        Returns:
            True if the variable is defined, False otherwise
        """
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.has(name)
        return False

    def delete(self, name: str) -> bool:
        """Delete a variable from the current scope.
        
        Args:
            name: Variable name (with sigil prefix)
            
        Returns:
            True if the variable was deleted, False if not found
        """
        if name in self.variables:
            del self.variables[name]
            return True
        return False

    def keys(self) -> list:
        """Get all variable names in the current scope.
        
        Returns:
            List of variable names
        """
        return list(self.variables.keys())

    def all_keys(self) -> list:
        """Get all variable names in the entire scope chain.
        
        Returns:
            List of all variable names (including from parent scopes)
        """
        keys = list(self.variables.keys())
        if self.parent:
            # Add parent keys that aren't shadowed
            for key in self.parent.all_keys():
                if key not in keys:
                    keys.append(key)
        return keys
