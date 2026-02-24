"""
Pyrl VM - Main Virtual Machine

Virtual Machine for executing Pyrl code. This module provides the main
PyrlVM class that coordinates parsing and execution of Pyrl programs.

The Pyrl language is a hybrid Python-Perl inspired language with:
- Sigil-based variables: $scalar, @array, %hash, &function
- Python-style indentation syntax
- Dynamic typing with runtime type checking
- Built-in functions for common operations
- Object-oriented programming support

Architecture:
    The VM follows a tree-walking interpreter pattern:
    1. Parse source code into AST using PyrlLarkParser
    2. Execute AST nodes via dispatch to exec_* methods
    3. Manage variable scopes with Environment class
    
Example:
    >>> from pyrl.vm import PyrlVM
    >>> vm = PyrlVM()
    >>> vm.run('$x = 10; print($x)')
    10
"""
from typing import Any, List, Optional, Dict, Union

# Import parser
from ..lark_parser import (
    PyrlLarkParser,
    Program,
    ScalarVar,
    ArrayVar,
    HashVar,
    FuncVar,
    IdentRef,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    NoneLiteral,
    ArrayLiteral,
    HashLiteral,
    RegexLiteral,
    BinaryOp,
    UnaryOp,
    Assignment,
    HashAccess,
    ArrayAccess,
    AttributeAccess,
    FunctionCall,
    FunctionDef,
    IfStatement,
    ForLoop,
    WhileLoop,
    ReturnStatement,
    PrintStatement,
    AssertStatement,
    TestBlock,
    VueComponent,
    Block,
    AnonymousFuncDef,
    ClassDef,
    MethodDef,
    PropertyDef,
    MethodCall,
)

# Import VM components
from .exceptions import ReturnValue, BreakException, ContinueException, PyrlRuntimeError
from .environment import Environment
from .objects import PyrlFunction, PyrlClass, PyrlInstance, PyrlMethod

# Import builtins
from .builtins import BUILTINS, CONSTANTS
from .builtins_http import HTTP_BUILTINS
from .builtins_db import DB_BUILTINS
from .builtins_crypto import CRYPTO_BUILTINS


# Combine all builtins into a single registry
ALL_BUILTINS: Dict[str, Any] = {
    **BUILTINS, 
    **HTTP_BUILTINS, 
    **DB_BUILTINS, 
    **CRYPTO_BUILTINS
}


# Type alias for AST nodes
ASTNode = Union[
    Program, ScalarVar, ArrayVar, HashVar, FuncVar, IdentRef,
    NumberLiteral, StringLiteral, BooleanLiteral, NoneLiteral,
    ArrayLiteral, HashLiteral, RegexLiteral,
    BinaryOp, UnaryOp, Assignment, HashAccess, ArrayAccess, AttributeAccess,
    FunctionCall, FunctionDef, IfStatement, ForLoop, WhileLoop,
    ReturnStatement, PrintStatement, AssertStatement, TestBlock,
    VueComponent, Block, AnonymousFuncDef, ClassDef, MethodDef,
    PropertyDef, MethodCall
]


class PyrlVM:
    """Virtual Machine for Pyrl based on Lark parser.
    
    The PyrlVM executes Pyrl source code by:
    1. Parsing source code into an AST using PyrlLarkParser
    2. Executing the AST nodes with the execute() method
    3. Managing variable scopes with Environment
    
    Attributes:
        debug: Enable debug mode for verbose output
        env: Root environment for variable storage
        parser: Lark-based parser for Pyrl code
        output: List of captured output strings
    """

    def __init__(self, debug: bool = False):
        """Initialize the Pyrl VM.
        
        Args:
            debug: Enable debug mode for verbose output
        """
        self.debug: bool = debug
        self.env: Environment = Environment()
        self.parser: PyrlLarkParser = PyrlLarkParser()
        self.env.vm = self
        self.output: List[str] = []

        # Initialize built-ins
        self._init_builtins()

    def _init_builtins(self) -> None:
        """Initialize built-in functions and constants."""
        for name, func in ALL_BUILTINS.items():
            self.env.define(name, func)

        for name, value in CONSTANTS.items():
            self.env.define(name, value)

    # ===========================================
    # Public API
    # ===========================================

    def run(self, source: str) -> Any:
        """Run Pyrl source code.
        
        Args:
            source: Pyrl source code string
            
        Returns:
            Result of the last statement
        """
        ast = self.parser.parse(source)
        return self.execute_program(ast)

    def run_file(self, filepath: str) -> Any:
        """Run a Pyrl file.
        
        Args:
            filepath: Path to .pyrl file
            
        Returns:
            Result of the last statement
        """
        ast = self.parser.parse_file(filepath)
        return self.execute_program(ast)

    def execute_program(self, program: Program) -> Any:
        """Execute a program AST.
        
        Args:
            program: Program AST node
            
        Returns:
            Result of the last statement
        """
        result = None
        for stmt in program.statements:
            result = self.execute(stmt, self.env)
        return result

    # ===========================================
    # Execution Engine
    # ===========================================

    def execute(self, node: Optional[ASTNode], env: Environment) -> Any:
        """Execute an AST node.
        
        Dispatches to the appropriate exec_* method based on node type.
        
        Args:
            node: AST node to execute
            env: Environment for variable lookup
            
        Returns:
            Result of executing the node
        """
        if node is None:
            return None

        # Dispatch based on node type
        method_name = f'exec_{type(node).__name__}'
        method = getattr(self, method_name, self.exec_default)
        return method(node, env)

    def exec_default(self, node: Any, env: Environment) -> Any:
        """Default handler for unknown nodes."""
        if isinstance(node, (int, float, str, bool)):
            return node
        if node is None:
            return None
        raise PyrlRuntimeError(f"Unknown node type: {type(node).__name__}")

    # ===========================================
    # Literal Execution
    # ===========================================

    def exec_NumberLiteral(self, node: NumberLiteral, env: Environment) -> Any:
        return node.value

    def exec_StringLiteral(self, node: StringLiteral, env: Environment) -> Any:
        return node.value

    def exec_BooleanLiteral(self, node: BooleanLiteral, env: Environment) -> Any:
        return node.value

    def exec_NoneLiteral(self, node: NoneLiteral, env: Environment) -> Any:
        return None

    def exec_ArrayLiteral(self, node: ArrayLiteral, env: Environment) -> Any:
        return [self.execute(elem, env) for elem in node.elements]

    def exec_HashLiteral(self, node: HashLiteral, env: Environment) -> Any:
        result = {}
        for key, value in node.pairs.items():
            result[key] = self.execute(value, env)
        return result

    def exec_RegexLiteral(self, node: RegexLiteral, env: Environment) -> Any:
        import re
        return re.compile(node.pattern)

    # ===========================================
    # Variable Execution
    # ===========================================

    def exec_ScalarVar(self, node: ScalarVar, env: Environment) -> Any:
        return env.get('$' + node.name)

    def exec_ArrayVar(self, node: ArrayVar, env: Environment) -> Any:
        return env.get('@' + node.name)

    def exec_HashVar(self, node: HashVar, env: Environment) -> Any:
        return env.get('%' + node.name)

    def exec_FuncVar(self, node: FuncVar, env: Environment) -> Any:
        """Handle function variable (&name)."""
        return env.get('&' + node.name)

    def exec_IdentRef(self, node: IdentRef, env: Environment) -> Any:
        """Handle identifier reference (built-in functions)."""
        return env.get(node.name)

    # ===========================================
    # Expression Execution
    # ===========================================

    def exec_BinaryOp(self, node: BinaryOp, env: Environment) -> Any:
        import re
        
        left = self.execute(node.left, env)

        # Short-circuit evaluation for logical operators
        if node.operator == 'and':
            if not left:
                return left
            return self.execute(node.right, env)

        if node.operator == 'or':
            if left:
                return left
            return self.execute(node.right, env)

        right = self.execute(node.right, env)

        op = node.operator
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '//':
            return left // right
        elif op == '%':
            return left % right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        elif op == '=~':
            # Regex match
            if isinstance(right, str):
                return bool(re.search(right, str(left)))
            return bool(right.search(str(left)))
        elif op == '!~':
            # Regex not match
            if isinstance(right, str):
                return not bool(re.search(right, str(left)))
            return not bool(right.search(str(left)))
        else:
            raise PyrlRuntimeError(f"Unknown operator: {op}")

    def exec_UnaryOp(self, node: UnaryOp, env: Environment) -> Any:
        operand = self.execute(node.operand, env)
        op = node.operator

        if op == '-':
            return -operand
        elif op == '!':
            return not operand
        elif op == 'not':
            return not operand
        else:
            raise PyrlRuntimeError(f"Unknown unary operator: {op}")

    # ===========================================
    # Access Execution
    # ===========================================

    def exec_HashAccess(self, node: HashAccess, env: Environment) -> Any:
        obj = self.execute(node.obj, env)
        key = self.execute(node.key, env)
        try:
            return obj[key]
        except (KeyError, IndexError, TypeError):
            raise PyrlRuntimeError(f"Cannot access key '{key}' on {type(obj).__name__}")

    def exec_ArrayAccess(self, node: ArrayAccess, env: Environment) -> Any:
        obj = self.execute(node.obj, env)
        index = self.execute(node.index, env)
        try:
            return obj[int(index) if isinstance(index, float) else index]
        except (IndexError, KeyError, TypeError):
            raise PyrlRuntimeError(f"Cannot access index '{index}' on {type(obj).__name__}")

    def exec_AttributeAccess(self, node: AttributeAccess, env: Environment) -> Any:
        """Execute attribute access: $obj.attr"""
        obj = self.execute(node.obj, env)
        
        # Handle Pyrl instances
        if hasattr(obj, '__dict__') and node.attr in obj.__dict__:
            return obj.__dict__[node.attr]
        
        # Handle dict-like objects
        if isinstance(obj, dict) and node.attr in obj:
            return obj[node.attr]
        
        # Handle Python objects
        if hasattr(obj, node.attr):
            return getattr(obj, node.attr)
        
        raise PyrlRuntimeError(f"Attribute '{node.attr}' not found on {type(obj).__name__}")

    # ===========================================
    # Assignment Execution
    # ===========================================

    def exec_Assignment(self, node: Assignment, env: Environment) -> Any:
        value = self.execute(node.value, env)
        target = node.target

        if isinstance(target, ScalarVar):
            env.set('$' + target.name, value)
        elif isinstance(target, ArrayVar):
            env.set('@' + target.name, value)
        elif isinstance(target, HashVar):
            env.set('%' + target.name, value)
        elif isinstance(target, HashAccess):
            obj = self.execute(target.obj, env)
            key = self.execute(target.key, env)
            obj[key] = value
        elif isinstance(target, ArrayAccess):
            obj = self.execute(target.obj, env)
            index = self.execute(target.index, env)
            obj[index] = value
        elif isinstance(target, AttributeAccess):
            obj = self.execute(target.obj, env)
            setattr(obj, target.attr, value)
        else:
            raise PyrlRuntimeError(f"Invalid assignment target: {type(target).__name__}")

        return value

    # ===========================================
    # Function Execution
    # ===========================================

    def exec_FunctionCall(self, node: FunctionCall, env: Environment) -> Any:
        # First try with & prefix (for user-defined functions)
        # Then try without prefix (for builtins)
        try:
            func = env.get('&' + node.name)
        except PyrlRuntimeError:
            func = env.get(node.name)
        args = [self.execute(arg, env) for arg in node.args]

        if callable(func):
            return func(*args)

        raise PyrlRuntimeError(f"'{node.name}' is not callable")

    def exec_FunctionDef(self, node: FunctionDef, env: Environment) -> Any:
        func = PyrlFunction(
            name=node.name,
            params=node.params,
            body=node.body,
            closure=env
        )
        env.define('&' + node.name, func)
        return func

    # ===========================================
    # Control Flow Execution
    # ===========================================

    def exec_IfStatement(self, node: IfStatement, env: Environment) -> Any:
        condition = self.execute(node.condition, env)

        if condition:
            result = None
            for stmt in node.then_body:
                result = self.execute(stmt, env)
            return result

        # Check elif clauses
        for elif_cond, elif_body in node.elif_clauses:
            if self.execute(elif_cond, env):
                result = None
                for stmt in elif_body:
                    result = self.execute(stmt, env)
                return result

        # Else clause
        if node.else_body:
            result = None
            for stmt in node.else_body:
                result = self.execute(stmt, env)
            return result

        return None

    def exec_ForLoop(self, node: ForLoop, env: Environment) -> Any:
        iterable = self.execute(node.iterable, env)
        result = None

        var_name = '$' + node.var
        for item in iterable:
            if env.has(var_name):
                env.set(var_name, item)
            else:
                env.define(var_name, item)
            try:
                for stmt in node.body:
                    result = self.execute(stmt, env)
            except BreakException:
                break
            except ContinueException:
                continue

        return result

    def exec_WhileLoop(self, node: WhileLoop, env: Environment) -> Any:
        result = None

        while self.execute(node.condition, env):
            try:
                for stmt in node.body:
                    result = self.execute(stmt, env)
            except BreakException:
                break
            except ContinueException:
                continue

        return result

    # ===========================================
    # Statement Execution
    # ===========================================

    def exec_ReturnStatement(self, node: ReturnStatement, env: Environment) -> Any:
        value = None
        if node.value:
            value = self.execute(node.value, env)
        raise ReturnValue(value)

    def exec_PrintStatement(self, node: PrintStatement, env: Environment) -> Any:
        from .builtins import pyrl_str
        value = self.execute(node.value, env)
        output = pyrl_str(value)
        print(output)
        self.output.append(output)
        return None

    def exec_AssertStatement(self, node: AssertStatement, env: Environment) -> Any:
        left = self.execute(node.left, env)

        if node.right is not None:
            right = self.execute(node.right, env)
            op = node.operator

            if op == '==':
                result = left == right
            elif op == '!=':
                result = left != right
            elif op == '<':
                result = left < right
            elif op == '>':
                result = left > right
            elif op == '<=':
                result = left <= right
            elif op == '>=':
                result = left >= right
            else:
                result = bool(left)
        else:
            result = bool(left)

        if not result:
            raise PyrlRuntimeError(f"Assertion failed: {left} {node.operator or ''} {node.right or ''}")

        return True

    def exec_TestBlock(self, node: TestBlock, env: Environment) -> Any:
        """Execute a test block."""
        test_name = node.name or "unnamed test"
        print(f"\n=== Running test: {test_name} ===")

        result = None
        try:
            for stmt in node.body:
                result = self.execute(stmt, env)
            print(f"✓ Test passed: {test_name}")
        except Exception as e:
            print(f"✗ Test failed: {test_name}")
            print(f"  Error: {e}")

        return result

    def exec_VueComponent(self, node: VueComponent, env: Environment) -> Any:
        """Generate Vue component."""
        props = {}
        for key, value_node in node.properties.items():
            props[key] = self.execute(value_node, env)

        component = {
            'name': node.name,
            'props': props,
            'template': props.get('template', ''),
        }

        print(f"Vue Component: {node.name}")
        print(f"Props: {list(props.keys())}")

        return component

    # ===========================================
    # OOP Execution
    # ===========================================

    def exec_Block(self, node: Block, env: Environment) -> Any:
        """Execute a block of statements."""
        if env.vm is None:
            env.vm = self
        result = None
        for stmt in node.statements:
            result = self.execute(stmt, env)
        return result

    def exec_AnonymousFuncDef(self, node: AnonymousFuncDef, env: Environment) -> Any:
        """Execute anonymous function definition."""
        if env.vm is None:
            env.vm = self
        func = PyrlFunction(
            name=node.name,
            params=node.params,
            body=node.body,
            closure=env
        )
        env.define('&' + node.name, func)
        return func

    def exec_ClassDef(self, node: ClassDef, env: Environment) -> Any:
        """Execute class definition."""
        cls = PyrlClass(
            name=node.name,
            extends=node.extends,
            methods=node.methods,
            properties=node.properties,
            closure=env
        )
        env.define(node.name, cls)
        return cls

    def exec_MethodDef(self, node: MethodDef, env: Environment) -> Any:
        """Execute method definition (usually inside a class)."""
        return node

    def exec_PropertyDef(self, node: PropertyDef, env: Environment) -> Any:
        """Execute property definition."""
        if node.value:
            return self.execute(node.value, env)
        return None

    def exec_MethodCall(self, node: MethodCall, env: Environment) -> Any:
        """Execute method call: $obj.method(args)"""
        obj = self.execute(node.obj, env)
        args = [self.execute(arg, env) for arg in node.args]

        # Handle Pyrl instances
        if isinstance(obj, PyrlInstance):
            method = obj.get_method(node.method)
            return method(*args)
        
        # Handle Pyrl classes (static methods)
        if isinstance(obj, PyrlClass):
            method = obj.get_method(node.method)
            if method:
                return method(*args)

        # Handle Python objects
        method = getattr(obj, node.method, None)
        if method is None:
            raise PyrlRuntimeError(f"Method '{node.method}' not found on {type(obj).__name__}")
        
        if callable(method):
            return method(*args)
        
        raise PyrlRuntimeError(f"'{node.method}' is not callable on {type(obj).__name__}")

    # ===========================================
    # Utility Methods
    # ===========================================

    def get_variable(self, name: str) -> Any:
        """Get a variable from the root environment.
        
        Args:
            name: Variable name (without sigil)
            
        Returns:
            Variable value
        """
        # Try with each sigil
        for sigil in ['$', '@', '%', '&', '']:
            try:
                return self.env.get(sigil + name)
            except PyrlRuntimeError:
                continue
        return None

    def set_variable(self, name: str, value: Any) -> None:
        """Set a variable in the root environment.
        
        Args:
            name: Variable name (with sigil)
            value: Value to set
        """
        self.env.define(name, value)

    def get_output(self) -> str:
        """Get all captured output as a string."""
        return '\n'.join(self.output)

    def clear_output(self) -> None:
        """Clear captured output."""
        self.output = []

    def has_variable(self, name: str) -> bool:
        """Check if a variable exists.
        
        Args:
            name: Variable name (without sigil)
            
        Returns:
            True if variable exists, False otherwise
        """
        # Try with each sigil
        for sigil in ['$', '@', '%', '&', '']:
            if self.env.has(sigil + name):
                return True
        return False

    def reset(self) -> None:
        """Reset the VM to initial state.
        
        Clears all user-defined variables and output, but keeps builtins.
        """
        # Clear output
        self.output = []
        
        # Reinitialize environment
        self.env = Environment()
        self.env.vm = self
        self._init_builtins()
        
        # Reset parser
        self.parser = PyrlLarkParser()

    def get_globals(self) -> Dict[str, Any]:
        """Get all global variables.
        
        Returns:
            Dict of all variables in the root environment
        """
        return dict(self.env.variables)


# ===========================================
# Module-level Helper Functions
# ===========================================

def run(source: str) -> Any:
    """Run Pyrl source code using a new VM instance.
    
    Convenience function for quickly executing Pyrl code.
    
    Args:
        source: Pyrl source code string
        
    Returns:
        Result of the last statement
    """
    vm = PyrlVM()
    return vm.run(source)


def run_file(filepath: str) -> Any:
    """Run a Pyrl file using a new VM instance.
    
    Convenience function for quickly executing a Pyrl file.
    
    Args:
        filepath: Path to .pyrl file
        
    Returns:
        Result of the last statement
    """
    vm = PyrlVM()
    return vm.run_file(filepath)


def create_vm() -> PyrlVM:
    """Create a new PyrlVM instance.
    
    Convenience function for creating a VM with default settings.
    
    Returns:
        New PyrlVM instance
    """
    return PyrlVM()
