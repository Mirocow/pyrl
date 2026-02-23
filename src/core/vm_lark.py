"""
Pyrl VM based on Lark Parser
Virtual Machine that executes Pyrl code using Lark grammar-based parsing.
"""
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
import math
import random
import re
import json
import time as time_module

# Import Lark parser
from .lark_parser import (
    PyrlLarkParser,
    Program,
    ScalarVar,
    ArrayVar,
    HashVar,
    FuncVar,
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
)


class ReturnValue(Exception):
    """Exception used to return values from functions."""
    def __init__(self, value: Any = None):
        self.value = value


class BreakException(Exception):
    """Exception used for break statement."""
    pass


class ContinueException(Exception):
    """Exception used for continue statement."""
    pass


class PyrlRuntimeError(Exception):
    """Runtime error in Pyrl code."""
    pass


# ===========================================
# Built-in Functions
# ===========================================

BUILTINS: Dict[str, Callable] = {}


def builtin(name: str):
    """Decorator to register built-in functions."""
    def decorator(func: Callable) -> Callable:
        BUILTINS[name] = func
        return func
    return decorator


# Type conversion
@builtin('int')
def pyrl_int(x=None, base=10):
    if x is None:
        return 0
    if isinstance(x, str):
        return int(x, base)
    return int(x)


@builtin('float')
def pyrl_float(x=None):
    if x is None:
        return 0.0
    return float(x)


@builtin('str')
def pyrl_str(x=None):
    if x is None:
        return 'None'
    if isinstance(x, bool):
        return 'True' if x else 'False'
    if isinstance(x, list):
        return '[' + ', '.join(pyrl_str(e) for e in x) + ']'
    if isinstance(x, dict):
        return '{' + ', '.join(f'{k}: {pyrl_str(v)}' for k, v in x.items()) + '}'
    return str(x)


@builtin('bool')
def pyrl_bool(x=None):
    if x is None:
        return False
    return bool(x)


@builtin('list')
def pyrl_list(x=None):
    if x is None:
        return []
    return list(x)


@builtin('dict')
def pyrl_dict(x=None):
    if x is None:
        return {}
    return dict(x)


@builtin('len')
def pyrl_len(x):
    return len(x)


@builtin('range')
def pyrl_range(start, stop=None, step=1):
    if stop is None:
        return list(range(int(start)))
    return list(range(int(start), int(stop), int(step)))


@builtin('type')
def pyrl_type(x):
    type_names = {
        int: 'int',
        float: 'float',
        str: 'str',
        bool: 'bool',
        list: 'array',
        dict: 'hash',
        type(None): 'none',
    }
    return type_names.get(type(x), type(x).__name__)


# Math functions
@builtin('abs')
def pyrl_abs(x):
    return abs(x)


@builtin('round')
def pyrl_round(x, ndigits=0):
    return round(x, ndigits)


@builtin('min')
def pyrl_min(*args):
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        return min(args[0])
    return min(args)


@builtin('max')
def pyrl_max(*args):
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        return max(args[0])
    return max(args)


@builtin('sum')
def pyrl_sum(iterable, start=0):
    return sum(iterable, start)


@builtin('pow')
def pyrl_pow(x, y, z=None):
    if z is None:
        return x ** y
    return pow(x, y, z)


@builtin('sqrt')
def pyrl_sqrt(x):
    return math.sqrt(x)


@builtin('sin')
def pyrl_sin(x):
    return math.sin(x)


@builtin('cos')
def pyrl_cos(x):
    return math.cos(x)


@builtin('tan')
def pyrl_tan(x):
    return math.tan(x)


@builtin('log')
def pyrl_log(x, base=None):
    if base is None:
        return math.log(x)
    return math.log(x, base)


@builtin('exp')
def pyrl_exp(x):
    return math.exp(x)


@builtin('floor')
def pyrl_floor(x):
    return math.floor(x)


@builtin('ceil')
def pyrl_ceil(x):
    return math.ceil(x)


# String functions
@builtin('lower')
def pyrl_lower(s):
    return str(s).lower()


@builtin('upper')
def pyrl_upper(s):
    return str(s).upper()


@builtin('strip')
def pyrl_strip(s, chars=None):
    return str(s).strip(chars)


@builtin('split')
def pyrl_split(s, sep=None, maxsplit=-1):
    return str(s).split(sep, maxsplit)


@builtin('join')
def pyrl_join(sep, iterable):
    return sep.join(str(x) for x in iterable)


@builtin('replace')
def pyrl_replace(s, old, new, count=-1):
    return str(s).replace(old, new, count)


@builtin('find')
def pyrl_find(s, sub, start=0, end=None):
    if end is None:
        return str(s).find(sub, start)
    return str(s).find(sub, start, end)


@builtin('startswith')
def pyrl_startswith(s, prefix, start=0, end=None):
    return str(s).startswith(prefix, start, end)


@builtin('endswith')
def pyrl_endswith(s, suffix, start=0, end=None):
    return str(s).endswith(suffix, start, end)


@builtin('format')
def pyrl_format(template, *args, **kwargs):
    return template.format(*args, **kwargs)


# List functions
@builtin('append')
def pyrl_append(lst, item):
    lst.append(item)
    return lst


@builtin('extend')
def pyrl_extend(lst, items):
    lst.extend(items)
    return lst


@builtin('insert')
def pyrl_insert(lst, index, item):
    lst.insert(index, item)
    return lst


@builtin('remove')
def pyrl_remove(lst, item):
    lst.remove(item)
    return lst


@builtin('pop')
def pyrl_pop(lst, index=-1):
    return lst.pop(index)


@builtin('index')
def pyrl_index(lst, item, start=0, end=None):
    if end is None:
        return lst.index(item, start)
    return lst.index(item, start, end)


@builtin('count')
def pyrl_count(lst, item):
    return lst.count(item)


@builtin('sort')
def pyrl_sort(lst, reverse=False):
    lst.sort(reverse=reverse)
    return lst


@builtin('reverse')
def pyrl_reverse(lst):
    lst.reverse()
    return lst


@builtin('copy')
def pyrl_copy(lst):
    return lst.copy()


@builtin('clear')
def pyrl_clear(lst):
    lst.clear()
    return lst


# Dict functions
@builtin('keys')
def pyrl_keys(d):
    return list(d.keys())


@builtin('values')
def pyrl_values(d):
    return list(d.values())


@builtin('items')
def pyrl_items(d):
    return list(d.items())


@builtin('get')
def pyrl_get(d, key, default=None):
    return d.get(key, default)


@builtin('setdefault')
def pyrl_setdefault(d, key, default=None):
    return d.setdefault(key, default)


@builtin('update')
def pyrl_update(d, other):
    d.update(other)
    return d


@builtin('popitem')
def pyrl_popitem(d):
    return d.popitem()


# Random functions
@builtin('random')
def pyrl_random():
    return random.random()


@builtin('randint')
def pyrl_randint(a, b):
    return random.randint(a, b)


@builtin('choice')
def pyrl_choice(seq):
    return random.choice(seq)


@builtin('shuffle')
def pyrl_shuffle(lst):
    random.shuffle(lst)
    return lst


@builtin('seed')
def pyrl_seed(x=None):
    random.seed(x)


# Utility functions
@builtin('enumerate')
def pyrl_enumerate(iterable, start=0):
    return list(enumerate(iterable, start))


@builtin('zip')
def pyrl_zip(*iterables):
    return list(zip(*iterables))


@builtin('map')
def pyrl_map(func, iterable):
    return list(map(func, iterable))


@builtin('filter')
def pyrl_filter(func, iterable):
    return list(filter(func, iterable))


@builtin('sorted')
def pyrl_sorted(iterable, reverse=False, key=None):
    return sorted(iterable, reverse=reverse, key=key)


@builtin('reversed')
def pyrl_reversed(iterable):
    return list(reversed(iterable))


@builtin('any')
def pyrl_any(iterable):
    return any(iterable)


@builtin('all')
def pyrl_all(iterable):
    return all(iterable)


@builtin('hasattr')
def pyrl_hasattr(obj, name):
    return hasattr(obj, name)


@builtin('getattr')
def pyrl_getattr(obj, name, default=None):
    return getattr(obj, name, default)


@builtin('setattr')
def pyrl_setattr(obj, name, value):
    setattr(obj, name, value)


@builtin('callable')
def pyrl_callable(obj):
    return callable(obj)


@builtin('repr')
def pyrl_repr(obj):
    return repr(obj)


@builtin('id')
def pyrl_id(obj):
    return id(obj)


@builtin('hash')
def pyrl_hash(obj):
    return hash(obj)


@builtin('dir')
def pyrl_dir(obj=None):
    if obj is None:
        return list(globals().keys())
    return dir(obj)


@builtin('help')
def pyrl_help(obj=None):
    if obj is None:
        print("Pyrl Interactive Help")
        return None
    print(f"Help on {obj}")
    return None


@builtin('exit')
def pyrl_exit(code=0):
    import sys
    sys.exit(code)


# Regex functions
@builtin('re_match')
def pyrl_re_match(pattern, string, flags=0):
    match = re.match(pattern, string, flags)
    if match:
        return match.groups()
    return None


@builtin('re_search')
def pyrl_re_search(pattern, string, flags=0):
    match = re.search(pattern, string, flags)
    if match:
        return match.groups()
    return None


@builtin('re_findall')
def pyrl_re_findall(pattern, string, flags=0):
    return re.findall(pattern, string, flags)


@builtin('re_sub')
def pyrl_re_sub(pattern, repl, string, count=0, flags=0):
    return re.sub(pattern, repl, string, count, flags)


@builtin('re_split')
def pyrl_re_split(pattern, string, maxsplit=0, flags=0):
    return re.split(pattern, string, maxsplit, flags)


# HTTP and JSON
@builtin('http_get')
def pyrl_http_get(url, timeout=30):
    try:
        import requests
        response = requests.get(url, timeout=timeout)
        return {
            'status': response.status_code,
            'data': response.text,
            'headers': dict(response.headers),
            'ok': response.ok
        }
    except ImportError:
        raise PyrlRuntimeError("HTTP functions require 'requests' library")
    except Exception as e:
        return {'status': 0, 'error': str(e), 'ok': False}


@builtin('http_post')
def pyrl_http_post(url, data=None, timeout=30):
    try:
        import requests
        response = requests.post(url, data=data, timeout=timeout)
        return {
            'status': response.status_code,
            'data': response.text,
            'headers': dict(response.headers),
            'ok': response.ok
        }
    except ImportError:
        raise PyrlRuntimeError("HTTP functions require 'requests' library")
    except Exception as e:
        return {'status': 0, 'error': str(e), 'ok': False}


@builtin('json_parse')
def pyrl_json_parse(s):
    return json.loads(s)


@builtin('json_stringify')
def pyrl_json_stringify(obj, indent=None):
    return json.dumps(obj, indent=indent, default=str)


@builtin('time')
def pyrl_time():
    return time_module.time()


@builtin('sleep')
def pyrl_sleep(seconds):
    time_module.sleep(seconds)
    return None


@builtin('print')
def pyrl_print(*args):
    output = ' '.join(pyrl_str(arg) for arg in args)
    print(output)
    return None


@builtin('input')
def pyrl_input(prompt=None):
    if prompt:
        print(prompt, end='')
    return input()


# Constants
CONSTANTS = {
    'True': True,
    'False': False,
    'None': None,
    'PI': math.pi,
    'E': math.e,
    'INF': float('inf'),
    'NAN': float('nan'),
}


# ===========================================
# User-defined Function
# ===========================================

@dataclass
class PyrlFunction:
    """User-defined Pyrl function."""
    name: str
    params: List[str]
    body: List[Any]
    closure: 'Environment'
    
    def __call__(self, *args):
        # Create new environment with closure
        local_env = Environment(parent=self.closure)
        
        # Bind parameters
        for i, param in enumerate(self.params):
            if i < len(args):
                local_env.define(param, args[i])
            else:
                local_env.define(param, None)
        
        # Execute body
        try:
            result = None
            for stmt in self.body:
                result = self.closure.vm.execute(stmt, local_env)
            return result
        except ReturnValue as ret:
            return ret.value


# ===========================================
# Environment
# ===========================================

class Environment:
    """Variable environment with scoping."""
    
    def __init__(self, parent: Optional['Environment'] = None):
        self.variables: Dict[str, Any] = {}
        self.parent = parent
        self.vm: Optional['PyrlLarkVM'] = None
    
    def define(self, name: str, value: Any) -> None:
        """Define a new variable."""
        self.variables[name] = value
    
    def get(self, name: str) -> Any:
        """Get a variable value."""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise PyrlRuntimeError(f"Undefined variable: {name}")
    
    def set(self, name: str, value: Any) -> None:
        """Set a variable value (searches up the scope chain)."""
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            # Create new variable in current scope
            self.variables[name] = value
    
    def has(self, name: str) -> bool:
        """Check if variable exists."""
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.has(name)
        return False


# ===========================================
# VM Implementation
# ===========================================

class PyrlLarkVM:
    """Virtual Machine for Pyrl based on Lark parser."""
    
    def __init__(self):
        self.parser = PyrlLarkParser()
        self.global_env = Environment()
        self.global_env.vm = self
        self.output: List[str] = []
        
        # Initialize built-ins
        self._init_builtins()
    
    def _init_builtins(self):
        """Initialize built-in functions and constants."""
        for name, func in BUILTINS.items():
            self.global_env.define(name, func)
        
        for name, value in CONSTANTS.items():
            self.global_env.define(name, value)
    
    def run(self, source: str) -> Any:
        """Run Pyrl source code."""
        ast = self.parser.parse(source)
        return self.execute_program(ast)
    
    def run_file(self, filepath: str) -> Any:
        """Run a Pyrl file."""
        ast = self.parser.parse_file(filepath)
        return self.execute_program(ast)
    
    def execute_program(self, program: Program) -> Any:
        """Execute a program AST."""
        result = None
        for stmt in program.statements:
            result = self.execute(stmt, self.global_env)
        return result
    
    def execute(self, node: Any, env: Environment) -> Any:
        """Execute an AST node."""
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
    
    # Literals
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
        return re.compile(node.pattern)
    
    # Variables
    def exec_ScalarVar(self, node: ScalarVar, env: Environment) -> Any:
        return env.get(node.name)
    
    def exec_ArrayVar(self, node: ArrayVar, env: Environment) -> Any:
        return env.get(node.name)
    
    def exec_HashVar(self, node: HashVar, env: Environment) -> Any:
        return env.get(node.name)
    
    def exec_FuncVar(self, node: FuncVar, env: Environment) -> Any:
        return env.get(node.name)
    
    # Expressions
    def exec_BinaryOp(self, node: BinaryOp, env: Environment) -> Any:
        left = self.execute(node.left, env)
        
        # Short-circuit evaluation
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
    
    # Access
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
    
    # Assignment
    def exec_Assignment(self, node: Assignment, env: Environment) -> Any:
        value = self.execute(node.value, env)
        
        # Determine target
        target = node.target
        
        if isinstance(target, ScalarVar):
            env.set(target.name, value)
        elif isinstance(target, ArrayVar):
            env.set(target.name, value)
        elif isinstance(target, HashVar):
            env.set(target.name, value)
        elif isinstance(target, (HashAccess, ArrayAccess)):
            obj = self.execute(target.obj, env)
            key = self.execute(target.key, env)
            obj[key] = value
        else:
            raise PyrlRuntimeError(f"Invalid assignment target: {type(target).__name__}")
        
        return value
    
    # Function call
    def exec_FunctionCall(self, node: FunctionCall, env: Environment) -> Any:
        func = env.get(node.name)
        args = [self.execute(arg, env) for arg in node.args]
        
        if callable(func):
            return func(*args)
        
        raise PyrlRuntimeError(f"'{node.name}' is not callable")
    
    # Function definition
    def exec_FunctionDef(self, node: FunctionDef, env: Environment) -> Any:
        func = PyrlFunction(
            name=node.name,
            params=node.params,
            body=node.body,
            closure=env
        )
        env.define(node.name, func)
        return func
    
    # Control flow
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
        
        for item in iterable:
            env.define(node.var, item)
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
    
    # Statements
    def exec_ReturnStatement(self, node: ReturnStatement, env: Environment) -> Any:
        value = None
        if node.value:
            value = self.execute(node.value, env)
        raise ReturnValue(value)
    
    def exec_PrintStatement(self, node: PrintStatement, env: Environment) -> Any:
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
    
    # Utility methods
    def get_globals(self) -> Dict[str, Any]:
        """Get all global variables."""
        return self.global_env.variables.copy()
    
    def reset(self) -> None:
        """Reset VM state."""
        self.global_env = Environment()
        self.global_env.vm = self
        self.output = []
        self._init_builtins()


# ===========================================
# Convenience Functions
# ===========================================

def run_lark(source: str) -> Any:
    """Run Pyrl source code using Lark parser."""
    vm = PyrlLarkVM()
    return vm.run(source)


def run_file_lark_vm(filepath: str) -> Any:
    """Run a Pyrl file using Lark parser."""
    vm = PyrlLarkVM()
    return vm.run_file(filepath)


def create_lark_vm() -> PyrlLarkVM:
    """Create a new Pyrl Lark VM instance."""
    return PyrlLarkVM()
