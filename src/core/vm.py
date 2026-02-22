"""
Pyrl Virtual Machine Module
Main VM class for the Pyrl language interpreter.
"""
from typing import Any, Dict, List, Optional
from .lexer import tokenize, Lexer
from .parser import parse, Parser
from .interpreter import Interpreter, Environment, interpret
from .exceptions import PyrlError, LexerError, ParseError, RuntimeError
from .ast_nodes import Token, ProgramNode


class PyrlVM:
    """
    Pyrl Virtual Machine - main entry point for executing Pyrl code.
    
    The Pyrl language is a hybrid Python-Perl inspired language with:
    - Sigil-based variables: $scalar, @array, %hash, &function
    - Python-style indentation syntax (no braces)
    - Dynamic typing with runtime type checking
    - Built-in functions for common operations
    """
    
    def __init__(self, debug: bool = False):
        """
        Initialize the Pyrl VM.
        
        Args:
            debug: Enable debug mode for verbose output
        """
        self.debug = debug
        self.env = Environment()
        self.interpreter = Interpreter(self.env)
        self._last_result = None
        self._globals: Dict[str, Any] = {}
    
    def run(self, source: str) -> Any:
        """
        Execute Pyrl source code.
        
        Args:
            source: The Pyrl source code to execute
            
        Returns:
            The result of the last expression
        """
        if self.debug:
            print(f"[DEBUG] Executing source:\n{source}")
        
        try:
            tokens = tokenize(source)
            if self.debug:
                print(f"[DEBUG] Tokens: {tokens}")
            
            ast = parse(tokens)
            if self.debug:
                print(f"[DEBUG] AST: {ast}")
            
            result = self.interpreter.execute(ast)
            self._last_result = result
            
            return result
        except PyrlError as e:
            if self.debug:
                print(f"[DEBUG] Pyrl Error: {e}")
            raise
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Unexpected Error: {e}")
            raise RuntimeError(str(e))
    
    def run_file(self, filepath: str) -> Any:
        """
        Execute a Pyrl source file.
        
        Args:
            filepath: Path to the .pyrl source file
            
        Returns:
            The result of the last expression
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        return self.run(source)
    
    def tokenize(self, source: str) -> List[Token]:
        """
        Tokenize Pyrl source code.
        
        Args:
            source: The Pyrl source code to tokenize
            
        Returns:
            List of tokens
        """
        return tokenize(source)
    
    def parse(self, source: str) -> ProgramNode:
        """
        Parse Pyrl source code into an AST.
        
        Args:
            source: The Pyrl source code to parse
            
        Returns:
            The AST program node
        """
        tokens = tokenize(source)
        return parse(tokens)
    
    def get_variable(self, name: str) -> Any:
        """
        Get the value of a variable.
        
        Args:
            name: Variable name (without sigil)
            
        Returns:
            The variable's value
        """
        return self.env.get(name)
    
    def set_variable(self, name: str, value: Any) -> None:
        """
        Set the value of a variable.
        
        Args:
            name: Variable name (without sigil)
            value: The value to set
        """
        self.env.define(name, value)
    
    def has_variable(self, name: str) -> bool:
        """
        Check if a variable exists.
        
        Args:
            name: Variable name (without sigil)
            
        Returns:
            True if the variable exists
        """
        return self.env.has(name)
    
    def define_function(self, name: str, func: callable) -> None:
        """
        Define a callable as a Pyrl function.
        
        Args:
            name: Function name
            func: Callable to register
        """
        self.env.define(name, func)
    
    def call_function(self, name: str, *args) -> Any:
        """
        Call a Pyrl function by name.
        
        Args:
            name: Function name
            *args: Arguments to pass
            
        Returns:
            The function's return value
        """
        func = self.env.get(name)
        if not callable(func):
            raise RuntimeError(f"'{name}' is not callable")
        return func(*args)
    
    def reset(self) -> None:
        """Reset the VM state, clearing all variables."""
        self.env = Environment()
        self.interpreter = Interpreter(self.env)
        self._last_result = None
    
    @property
    def last_result(self) -> Any:
        """Get the result of the last executed expression."""
        return self._last_result
    
    def get_globals(self) -> Dict[str, Any]:
        """Get all global variables."""
        return dict(self.env.variables)
    
    def eval_expr(self, expr: str) -> Any:
        """
        Evaluate a single expression.
        
        Args:
            expr: The expression to evaluate
            
        Returns:
            The result of the expression
        """
        # Wrap expression to ensure it returns a value
        source = f"_result = {expr}"
        self.run(source)
        return self.env.get("_result")
    
    def repl(self) -> None:
        """Start an interactive REPL session."""
        print("Pyrl Interactive Shell")
        print("Type 'exit' to quit, 'help' for help")
        print("-" * 40)
        
        while True:
            try:
                line = input("pyrl> ")
                
                if line.strip() == "exit":
                    print("Goodbye!")
                    break
                
                if line.strip() == "help":
                    self._print_help()
                    continue
                
                if line.strip() == "vars":
                    print(self.get_globals())
                    continue
                
                result = self.run(line)
                if result is not None:
                    print(result)
                    
            except KeyboardInterrupt:
                print("\nInterrupted. Type 'exit' to quit.")
            except PyrlError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error: {e}")
    
    def _print_help(self) -> None:
        """Print help information."""
        help_text = """
Pyrl Language Help
==================

Variables:
    $name   - Scalar variable (single value)
    @array  - Array variable (list)
    %hash   - Hash/dict variable
    &func   - Function reference

Examples:
    $x = 10
    @arr = [1, 2, 3]
    %person = {name: "Alice", age: 30}
    
    def greet($name):
        print("Hello, " + $name)
    
    greet("World")

Commands:
    exit    - Exit the REPL
    help    - Show this help
    vars    - Show all variables
"""
        print(help_text)
    
    def __repr__(self) -> str:
        return f"<PyrlVM debug={self.debug}>"


# Convenience functions
def run(source: str, debug: bool = False) -> Any:
    """Execute Pyrl source code."""
    vm = PyrlVM(debug=debug)
    return vm.run(source)


def run_file(filepath: str, debug: bool = False) -> Any:
    """Execute a Pyrl source file."""
    vm = PyrlVM(debug=debug)
    return vm.run_file(filepath)


def create_vm(debug: bool = False) -> PyrlVM:
    """Create a new Pyrl VM instance."""
    return PyrlVM(debug=debug)


# Export main classes and functions
__all__ = [
    'PyrlVM',
    'run',
    'run_file',
    'create_vm',
    'tokenize',
    'parse',
    'interpret',
    'Environment',
    'Interpreter',
    'PyrlError',
    'LexerError',
    'ParseError',
    'RuntimeError',
]
