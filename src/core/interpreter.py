"""
Pyrl Interpreter Module
Interprets the AST and executes Pyrl code.
"""
from typing import Any, Dict, List, Optional, Callable
from .ast_nodes import *
from .exceptions import (
    RuntimeError, VariableError, FunctionError, TypeError_,
    IndexError_, KeyError_, ReturnException, BreakException, ContinueException
)
from .builtins import get_builtins, BUILTIN_CONSTANTS, PyrlBuiltin


class Environment:
    """Environment for variable scoping."""
    
    def __init__(self, parent: 'Environment' = None):
        self.parent = parent
        self.variables: Dict[str, Any] = {}
        self.constants: set = set()
    
    def define(self, name: str, value: Any, constant: bool = False) -> None:
        """Define a new variable."""
        self.variables[name] = value
        if constant:
            self.constants.add(name)
    
    def get(self, name: str) -> Any:
        """Get a variable value."""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise VariableError(f"Undefined variable '{name}'", name)
    
    def set(self, name: str, value: Any) -> None:
        """Set a variable value."""
        if name in self.variables:
            if name in self.constants:
                raise VariableError(f"Cannot assign to constant '{name}'", name)
            self.variables[name] = value
            return
        if self.parent:
            self.parent.set(name, value)
            return
        raise VariableError(f"Undefined variable '{name}'", name)
    
    def has(self, name: str) -> bool:
        """Check if a variable exists."""
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.has(name)
        return False


class PyrlFunction:
    """Represents a user-defined function."""
    
    def __init__(self, name: str, params: List[str], body: List[ASTNode], closure: Environment):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure
    
    def __call__(self, *args):
        # Create new environment with closure
        env = Environment(self.closure)
        
        # Bind parameters
        for i, param in enumerate(self.params):
            if i < len(args):
                env.define(param, args[i])
            else:
                env.define(param, None)
        
        # Execute body
        interpreter = Interpreter(env)
        try:
            result = None
            for stmt in self.body:
                result = interpreter.execute(stmt)
            return result
        except ReturnException as e:
            return e.value
    
    def __repr__(self):
        return f"<function {self.name}>"


class PyrlClass:
    """Represents a user-defined class."""
    
    def __init__(self, name: str, bases: List[str], body: List[ASTNode], env: Environment):
        self.name = name
        self.bases = bases
        self.methods: Dict[str, PyrlFunction] = {}
        self.attributes: Dict[str, Any] = {}
        self.env = env
        
        # Process body
        for stmt in body:
            if isinstance(stmt, DefNode):
                func = PyrlFunction(stmt.name, stmt.params, stmt.body, env)
                self.methods[stmt.name] = func
            elif isinstance(stmt, AssignNode):
                if isinstance(stmt.target, ScalarNode):
                    self.attributes[stmt.target.name] = env.get('__temp__') if env.has('__temp__') else None
    
    def __call__(self, *args, **kwargs):
        instance = PyrlInstance(self)
        
        # Call __init__ if exists
        if '__init__' in self.methods:
            init_method = BoundMethod(instance, self.methods['__init__'])
            init_method(*args)
        
        return instance
    
    def __repr__(self):
        return f"<class {self.name}>"


class PyrlInstance:
    """Represents an instance of a class."""
    
    def __init__(self, klass: PyrlClass):
        self.klass = klass
        self.attributes: Dict[str, Any] = {}
    
    def get(self, name: str) -> Any:
        if name in self.attributes:
            return self.attributes[name]
        
        if name in self.klass.methods:
            return BoundMethod(self, self.klass.methods[name])
        
        raise AttributeError(f"'{self.klass.name}' has no attribute '{name}'")
    
    def set(self, name: str, value: Any) -> None:
        self.attributes[name] = value
    
    def __repr__(self):
        return f"<{self.klass.name} instance>"


class BoundMethod:
    """Represents a method bound to an instance."""
    
    def __init__(self, instance: PyrlInstance, method: PyrlFunction):
        self.instance = instance
        self.method = method
    
    def __call__(self, *args):
        return self.method(self.instance, *args)
    
    def __repr__(self):
        return f"<bound method {self.method.name}>"


class Interpreter:
    """Interpreter for the Pyrl language."""
    
    def __init__(self, env: Environment = None):
        self.env = env or Environment()
        self.global_env = self.env
        
        # Initialize builtins
        for name, func in get_builtins().items():
            self.env.define(name, func)
        
        for name, value in BUILTIN_CONSTANTS.items():
            self.env.define(name, value, constant=True)
    
    def execute(self, node: ASTNode) -> Any:
        """Execute an AST node."""
        method_name = f'execute_{type(node).__name__}'
        method = getattr(self, method_name, None)
        
        if method:
            return method(node)
        
        raise RuntimeError(f"Unknown node type: {type(node).__name__}")
    
    def execute_ProgramNode(self, node: ProgramNode) -> Any:
        result = None
        for stmt in node.statements:
            result = self.execute(stmt)
        return result
    
    def execute_NumberNode(self, node: NumberNode) -> float:
        return node.value
    
    def execute_StringNode(self, node: StringNode) -> str:
        return node.value
    
    def execute_BooleanNode(self, node: BooleanNode) -> bool:
        return node.value
    
    def execute_NoneNode(self, node: NoneNode) -> None:
        return None
    
    def execute_ScalarNode(self, node: ScalarNode) -> Any:
        return self.env.get(node.name)
    
    def execute_ArrayNode(self, node: ArrayNode) -> List:
        return self.env.get(node.name)
    
    def execute_HashNode(self, node: HashNode) -> Dict:
        return self.env.get(node.name)
    
    def execute_FunctionRefNode(self, node: FunctionRefNode) -> Any:
        return self.env.get(node.name)
    
    def execute_ArrayLiteralNode(self, node: ArrayLiteralNode) -> List:
        return [self.execute(elem) for elem in node.elements]
    
    def execute_HashLiteralNode(self, node: HashLiteralNode) -> Dict:
        return {key: self.execute(value) for key, value in node.pairs.items()}
    
    def execute_BinaryOpNode(self, node: BinaryOpNode) -> Any:
        # Short-circuit evaluation for and/or
        if node.operator == 'and':
            left = self.execute(node.left)
            if not left:
                return left
            return self.execute(node.right)
        
        if node.operator == 'or':
            left = self.execute(node.left)
            if left:
                return left
            return self.execute(node.right)
        
        left = self.execute(node.left)
        right = self.execute(node.right)
        
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
        elif op == '**':
            return left ** right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '<':
            return left < right
        elif op == '<=':
            return left <= right
        elif op == '>':
            return left > right
        elif op == '>=':
            return left >= right
        else:
            raise RuntimeError(f"Unknown operator: {op}")
    
    def execute_UnaryOpNode(self, node: UnaryOpNode) -> Any:
        operand = self.execute(node.operand)
        
        if node.operator == '+':
            return +operand
        elif node.operator == '-':
            return -operand
        elif node.operator == 'not':
            return not operand
        else:
            raise RuntimeError(f"Unknown unary operator: {node.operator}")
    
    def execute_IndexNode(self, node: IndexNode) -> Any:
        obj = self.execute(node.obj)
        index = self.execute(node.index)
        
        try:
            return obj[index]
        except IndexError:
            raise IndexError_(f"Index out of range", index)
        except KeyError:
            raise KeyError_(f"Key not found", str(index))
    
    def execute_AttributeNode(self, node: AttributeNode) -> Any:
        obj = self.execute(node.obj)
        
        if isinstance(obj, PyrlInstance):
            return obj.get(node.attr)
        
        # Try to get attribute from Python object
        try:
            return getattr(obj, node.attr)
        except AttributeError:
            raise RuntimeError(f"'{type(obj).__name__}' has no attribute '{node.attr}'")
    
    def execute_CallNode(self, node: CallNode) -> Any:
        callee = self.execute(node.callee)
        args = [self.execute(arg) for arg in node.args]
        
        if callable(callee):
            return callee(*args)
        
        raise FunctionError(f"'{type(callee).__name__}' is not callable")
    
    def execute_LambdaNode(self, node: LambdaNode) -> PyrlFunction:
        return PyrlFunction('<lambda>', node.params, [node.body], self.env)
    
    def execute_AssignNode(self, node: AssignNode) -> Any:
        value = self.execute(node.value)
        
        if isinstance(node.target, ScalarNode):
            name = node.target.name
            # Handle both '=' string and 'ASSIGN' token value
            if node.operator in ('=', 'ASSIGN'):
                if self.env.has(name):
                    self.env.set(name, value)
                else:
                    self.env.define(name, value)
            else:
                current = self.env.get(name)
                if node.operator in ('+=', 'PLUS_ASSIGN'):
                    current += value
                elif node.operator in ('-=', 'MINUS_ASSIGN'):
                    current -= value
                elif node.operator in ('*=', 'STAR_ASSIGN'):
                    current *= value
                elif node.operator in ('/=', 'SLASH_ASSIGN'):
                    current /= value
                self.env.set(name, current)
            return value
        
        elif isinstance(node.target, IndexNode):
            obj = self.execute(node.target.obj)
            index = self.execute(node.target.index)
            obj[index] = value
            return value
        
        elif isinstance(node.target, AttributeNode):
            obj = self.execute(node.target.obj)
            if isinstance(obj, PyrlInstance):
                obj.set(node.target.attr, value)
            else:
                setattr(obj, node.target.attr, value)
            return value
        
        raise RuntimeError(f"Invalid assignment target: {type(node.target).__name__}")
    
    def execute_PrintNode(self, node: PrintNode) -> None:
        value = self.execute(node.value)
        print(value)
        return None
    
    def execute_IfNode(self, node: IfNode) -> Any:
        condition = self.execute(node.condition)
        
        if condition:
            result = None
            for stmt in node.then_body:
                result = self.execute(stmt)
            return result
        
        for elif_cond, elif_body in node.elif_clauses:
            if self.execute(elif_cond):
                result = None
                for stmt in elif_body:
                    result = self.execute(stmt)
                return result
        
        if node.else_body:
            result = None
            for stmt in node.else_body:
                result = self.execute(stmt)
            return result
        
        return None
    
    def execute_WhileNode(self, node: WhileNode) -> Any:
        result = None
        
        while self.execute(node.condition):
            try:
                for stmt in node.body:
                    result = self.execute(stmt)
            except BreakException:
                break
            except ContinueException:
                continue
        
        return result
    
    def execute_ForNode(self, node: ForNode) -> Any:
        iterable = self.execute(node.iterable)
        result = None
        
        for item in iterable:
            self.env.define(node.var, item)
            try:
                for stmt in node.body:
                    result = self.execute(stmt)
            except BreakException:
                break
            except ContinueException:
                continue
        
        return result
    
    def execute_ForRangeNode(self, node: ForRangeNode) -> Any:
        start = int(self.execute(node.start))
        end = int(self.execute(node.end))
        step = int(self.execute(node.step)) if node.step else 1
        
        result = None
        
        for i in range(start, end, step):
            self.env.define(node.var, i)
            try:
                for stmt in node.body:
                    result = self.execute(stmt)
            except BreakException:
                break
            except ContinueException:
                continue
        
        return result
    
    def execute_DefNode(self, node: DefNode) -> None:
        func = PyrlFunction(node.name, node.params, node.body, self.env)
        self.env.define(node.name, func)
        return None
    
    def execute_ClassNode(self, node: ClassNode) -> None:
        klass = PyrlClass(node.name, node.bases, node.body, self.env)
        self.env.define(node.name, klass)
        return None
    
    def execute_ReturnNode(self, node: ReturnNode) -> None:
        value = self.execute(node.value) if node.value else None
        raise ReturnException(value)
    
    def execute_BreakNode(self, node: BreakNode) -> None:
        raise BreakException()
    
    def execute_ContinueNode(self, node: ContinueNode) -> None:
        raise ContinueException()
    
    def execute_PassNode(self, node: PassNode) -> None:
        return None
    
    def execute_ImportNode(self, node: ImportNode) -> None:
        # For now, just define the module name as a placeholder
        # In a full implementation, this would load the actual module
        self.env.define(node.alias or node.module.split('.')[0], {})
        return None
    
    def execute_FromImportNode(self, node: FromImportNode) -> None:
        # For now, just define the imported names as placeholders
        for i, name in enumerate(node.names):
            alias = node.aliases[i] if node.aliases else name
            self.env.define(alias, None)
        return None
    
    def execute_TryNode(self, node: TryNode) -> Any:
        try:
            result = None
            for stmt in node.try_body:
                result = self.execute(stmt)
            return result
        except Exception as e:
            for exc_type, exc_var, exc_body in node.except_clauses:
                # Match any exception if no type specified
                if exc_type is None or isinstance(e, eval(exc_type)):
                    # Bind exception variable if specified
                    if exc_var:
                        self.env.define(exc_var, e)
                    
                    result = None
                    for stmt in exc_body:
                        result = self.execute(stmt)
                    return result
            raise
        finally:
            if node.finally_body:
                for stmt in node.finally_body:
                    self.execute(stmt)
    
    def execute_RaiseNode(self, node: RaiseNode) -> None:
        exception = self.execute(node.exception)
        raise exception
    
    def execute_WithNode(self, node: WithNode) -> Any:
        context = self.execute(node.expr)
        
        if node.var:
            self.env.define(node.var, context)
        
        try:
            result = None
            for stmt in node.body:
                result = self.execute(stmt)
            return result
        finally:
            if hasattr(context, '__exit__'):
                context.__exit__(None, None, None)
    
    def execute_GlobalNode(self, node: GlobalNode) -> None:
        # Mark variables as global (simplified implementation)
        for name in node.names:
            if not self.global_env.has(name):
                self.global_env.define(name, None)
        return None
    
    def execute_NonlocalNode(self, node: NonlocalNode) -> None:
        # Nonlocal declaration (simplified implementation)
        return None


def interpret(source: str, env: Environment = None) -> Any:
    """Convenience function to interpret source code."""
    from .lexer import tokenize
    from .parser import parse
    
    tokens = tokenize(source)
    ast = parse(tokens)
    interpreter = Interpreter(env)
    return interpreter.execute(ast)
