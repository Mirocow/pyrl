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
    # OOP and Anonymous Functions
    Block,
    AnonymousFuncDef,
    ClassDef,
    MethodDef,
    PropertyDef,
    MethodCall,
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


# Environment functions
@builtin('env_get')
def pyrl_env_get(name, default=None):
    """Get environment variable."""
    import os
    return os.environ.get(name, default)


@builtin('env_set')
def pyrl_env_set(name, value):
    """Set environment variable."""
    import os
    os.environ[name] = str(value)
    return value


# URL encoding functions
@builtin('url_encode')
def pyrl_url_encode(s):
    """URL encode a string."""
    import urllib.parse
    return urllib.parse.quote(str(s))


@builtin('url_decode')
def pyrl_url_decode(s):
    """URL decode a string."""
    import urllib.parse
    return urllib.parse.unquote(str(s))


@builtin('parse_form')
def pyrl_parse_form(data):
    """Parse URL-encoded form data into a hash."""
    import urllib.parse
    result = {}
    if data:
        pairs = data.split('&')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                result[urllib.parse.unquote(key)] = urllib.parse.unquote_plus(value)
    return result


# HTTP Response helpers
@builtin('html_response')
def pyrl_html_response(content, status=200):
    """Create an HTML response."""
    return {
        'status': status,
        'headers': {'Content-Type': 'text/html; charset=utf-8'},
        'body': content
    }


@builtin('json_response')
def pyrl_json_response(data, status=200):
    """Create a JSON response."""
    return {
        'status': status,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data, default=str)
    }


@builtin('redirect')
def pyrl_redirect(location, permanent=False):
    """Create a redirect response."""
    return {
        'status': 301 if permanent else 302,
        'headers': {'Location': location},
        'body': ''
    }


@builtin('parse_cookies')
def pyrl_parse_cookies(cookie_header):
    """Parse Cookie header into a hash."""
    result = {}
    if cookie_header:
        cookies = cookie_header.split(';')
        for cookie in cookies:
            cookie = cookie.strip()
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                result[key.strip()] = value.strip()
    return result


# ===========================================
# SQLite Database Functions
# ===========================================

# Store for database connections
_db_connections: Dict[int, Any] = {}


@builtin('db_connect')
def pyrl_db_connect(filename: str = ":memory:"):
    """Connect to SQLite database. Returns connection handle.
    
    Args:
        filename: Path to database file (default: in-memory database)
    
    Returns:
        Database connection handle (integer id)
    """
    import sqlite3
    conn = sqlite3.connect(filename, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Enable row access by column name
    handle = id(conn)
    _db_connections[handle] = {
        'connection': conn,
        'cursor': conn.cursor(),
        'filename': filename
    }
    return handle


@builtin('db_execute')
def pyrl_db_execute(handle: int, sql: str, params: list = None):
    """Execute SQL statement (INSERT, UPDATE, DELETE, CREATE, etc.).
    
    Args:
        handle: Database connection handle from db_connect
        sql: SQL statement to execute
        params: Optional list of parameters for parameterized queries
    
    Returns:
        Dict with 'success', 'rowcount', 'lastrowid' or 'error'
    """
    if handle not in _db_connections:
        return {'success': False, 'error': 'Invalid database handle'}
    
    db = _db_connections[handle]
    conn = db['connection']
    cursor = db['cursor']
    
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
        return {
            'success': True,
            'rowcount': cursor.rowcount,
            'lastrowid': cursor.lastrowid
        }
    except Exception as e:
        conn.rollback()
        return {'success': False, 'error': str(e)}


@builtin('db_query')
def pyrl_db_query(handle: int, sql: str, params: list = None):
    """Execute SELECT query and fetch all results.
    
    Args:
        handle: Database connection handle from db_connect
        sql: SELECT SQL statement
        params: Optional list of parameters for parameterized queries
    
    Returns:
        Dict with 'success', 'rows' (list of dicts) or 'error'
    """
    if handle not in _db_connections:
        return {'success': False, 'error': 'Invalid database handle'}
    
    db = _db_connections[handle]
    cursor = db['cursor']
    
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        
        rows = cursor.fetchall()
        # Convert sqlite3.Row to dict
        result_rows = []
        for row in rows:
            result_rows.append(dict(row))
        
        return {'success': True, 'rows': result_rows}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@builtin('db_query_one')
def pyrl_db_query_one(handle: int, sql: str, params: list = None):
    """Execute SELECT query and fetch one result.
    
    Args:
        handle: Database connection handle from db_connect
        sql: SELECT SQL statement
        params: Optional list of parameters
    
    Returns:
        Dict with 'success', 'row' (dict or None) or 'error'
    """
    if handle not in _db_connections:
        return {'success': False, 'error': 'Invalid database handle'}
    
    db = _db_connections[handle]
    cursor = db['cursor']
    
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        
        row = cursor.fetchone()
        if row:
            return {'success': True, 'row': dict(row)}
        return {'success': True, 'row': None}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@builtin('db_close')
def pyrl_db_close(handle: int):
    """Close database connection.
    
    Args:
        handle: Database connection handle to close
    
    Returns:
        Dict with 'success' or 'error'
    """
    if handle not in _db_connections:
        return {'success': False, 'error': 'Invalid database handle'}
    
    db = _db_connections[handle]
    try:
        db['connection'].close()
        del _db_connections[handle]
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@builtin('db_tables')
def pyrl_db_tables(handle: int):
    """Get list of all tables in database.
    
    Args:
        handle: Database connection handle
    
    Returns:
        Dict with 'success', 'tables' (list of table names) or 'error'
    """
    result = pyrl_db_query(handle, 
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    if result['success']:
        tables = [row['name'] for row in result['rows']]
        return {'success': True, 'tables': tables}
    return result


@builtin('db_begin')
def pyrl_db_begin(handle: int):
    """Begin a database transaction.
    
    Args:
        handle: Database connection handle
    
    Returns:
        Dict with 'success' or 'error'
    """
    if handle not in _db_connections:
        return {'success': False, 'error': 'Invalid database handle'}
    
    db = _db_connections[handle]
    try:
        db['connection'].execute("BEGIN")
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@builtin('db_commit')
def pyrl_db_commit(handle: int):
    """Commit current transaction.
    
    Args:
        handle: Database connection handle
    
    Returns:
        Dict with 'success' or 'error'
    """
    if handle not in _db_connections:
        return {'success': False, 'error': 'Invalid database handle'}
    
    db = _db_connections[handle]
    try:
        db['connection'].commit()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@builtin('db_rollback')
def pyrl_db_rollback(handle: int):
    """Rollback current transaction.
    
    Args:
        handle: Database connection handle
    
    Returns:
        Dict with 'success' or 'error'
    """
    if handle not in _db_connections:
        return {'success': False, 'error': 'Invalid database handle'}
    
    db = _db_connections[handle]
    try:
        db['connection'].rollback()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


# ===========================================
# Utility Functions for Sessions
# ===========================================

@builtin('uuid')
def pyrl_uuid():
    """Generate a UUID4 string.
    
    Returns:
        UUID string like '550e8400-e29b-41d4-a716-446655440000'
    """
    import uuid as uuid_module
    return str(uuid_module.uuid4())


@builtin('hmac_sha256')
def pyrl_hmac_sha256(key: str, message: str):
    """Generate HMAC-SHA256 hash.
    
    Args:
        key: Secret key for HMAC
        message: Message to hash
    
    Returns:
        Hexadecimal hash string
    """
    import hmac
    import hashlib
    return hmac.new(
        key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


@builtin('sha256')
def pyrl_sha256(data: str):
    """Generate SHA256 hash of a string.
    
    Args:
        data: String to hash
    
    Returns:
        Hexadecimal hash string
    """
    import hashlib
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


@builtin('base64_encode')
def pyrl_base64_encode(data: str):
    """Encode string to base64.
    
    Args:
        data: String to encode
    
    Returns:
        Base64 encoded string
    """
    import base64
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


@builtin('base64_decode')
def pyrl_base64_decode(data: str):
    """Decode base64 string.
    
    Args:
        data: Base64 encoded string
    
    Returns:
        Decoded string
    """
    import base64
    return base64.b64decode(data.encode('utf-8')).decode('utf-8')


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
# OOP Classes
# ===========================================

class PyrlClass:
    """Pyrl class definition."""
    
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
            if isinstance(init_method, MethodDef):
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
        """Get a method by name."""
        if name in self.methods:
            method_def = self.methods[name]
            if isinstance(method_def, MethodDef):
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


class PyrlInstance:
    """Instance of a Pyrl class."""
    
    def __init__(self, cls: PyrlClass):
        self._class = cls
        self._properties = {}
        
        # Initialize properties from class definition
        for name, prop_def in cls.properties.items():
            if prop_def is not None:
                if isinstance(prop_def, PropertyDef):
                    self._properties[name] = prop_def.value
                else:
                    self._properties[name] = prop_def
    
    def get_property(self, name: str) -> Any:
        """Get a property value."""
        if name in self._properties:
            return self._properties[name]
        raise PyrlRuntimeError(f"Property '{name}' not found on {self._class.name}")
    
    def set_property(self, name: str, value: Any) -> None:
        """Set a property value."""
        self._properties[name] = value
    
    def get_method(self, name: str) -> 'PyrlMethod':
        """Get a bound method."""
        if name in self._class.methods:
            method_def = self._class.methods[name]
            if isinstance(method_def, MethodDef):
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


class PyrlMethod:
    """Bound method on a Pyrl instance."""
    
    def __init__(self, name: str, params: List[str], body: List[Any],
                 instance: Optional[PyrlInstance], closure: 'Environment'):
        self.name = name
        self.params = params
        self.body = body
        self.instance = instance
        self.closure = closure
    
    def __call__(self, *args):
        """Execute the method."""
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


# ===========================================
# Environment
# ===========================================

class Environment:
    """Variable environment with scoping."""

    def __init__(self, parent: Optional['Environment'] = None):
        self.variables: Dict[str, Any] = {}
        self.parent = parent
        self.vm: Optional['PyrlVM'] = None

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

class PyrlVM:
    """Virtual Machine for Pyrl based on Lark parser.
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
        self.parser = PyrlLarkParser()
        self.env.vm = self
        self.output: List[str] = []

        # Initialize built-ins
        self._init_builtins()

    def _init_builtins(self):
        """Initialize built-in functions and constants."""
        for name, func in BUILTINS.items():
            self.env.define(name, func)

        for name, value in CONSTANTS.items():
            self.env.define(name, value)

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
            result = self.execute(stmt, self.env)
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
            # Use $-prefixed name to avoid shadowing builtins
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
        else:
            raise PyrlRuntimeError(f"Invalid assignment target: {type(target).__name__}")

        return value

    # Function call
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

    # Function definition
    def exec_FunctionDef(self, node: FunctionDef, env: Environment) -> Any:
        func = PyrlFunction(
            name=node.name,
            params=node.params,
            body=node.body,
            closure=env
        )
        # Store function with & prefix
        env.define('&' + node.name, func)
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

        # Use $-prefixed name for loop variable
        var_name = '$' + node.var
        for item in iterable:
            # Use set() to update existing variable, or define if it doesn't exist
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

    # ===========================================
    # OOP and Anonymous Functions Execution
    # ===========================================

    def exec_Block(self, node: Block, env: Environment) -> Any:
        """Execute a block of statements."""
        # Make sure env has vm reference
        if env.vm is None:
            env.vm = self
        result = None
        for stmt in node.statements:
            result = self.execute(stmt, env)
        return result

    def exec_AnonymousFuncDef(self, node: AnonymousFuncDef, env: Environment) -> Any:
        """Execute anonymous function definition: &name($params) = { body }"""
        # Ensure the closure env has a vm reference
        if env.vm is None:
            env.vm = self
        func = PyrlFunction(
            name=node.name,
            params=node.params,
            body=node.body,
            closure=env
        )
        # Store function with & prefix
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
        return node  # Return the definition itself, used by class definition

    def exec_PropertyDef(self, node: PropertyDef, env: Environment) -> Any:
        """Execute property definition."""
        if node.value:
            return self.execute(node.value, env)
        return None

    def exec_MethodCall(self, node: MethodCall, env: Environment) -> Any:
        """Execute method call: $obj.method(args)"""
        obj = self.execute(node.obj, env)
        args = [self.execute(arg, env) for arg in node.args]

        # Check if it's a PyrlInstance
        if isinstance(obj, PyrlInstance):
            method = obj.get_method(node.method)
            return method(*args)
        
        # Check if it's a PyrlClass (static method call)
        if isinstance(obj, PyrlClass):
            method = obj.get_method(node.method)
            if method:
                return method(*args)

        # Check if obj is a dict with a method-like property
        if isinstance(obj, dict) and node.method in obj:
            prop = obj[node.method]
            if callable(prop):
                return prop(*args)

        # Check if it's a string method
        if isinstance(obj, str):
            string_methods = {
                'lower': lambda s: s.lower(),
                'upper': lambda s: s.upper(),
                'strip': lambda s: s.strip(),
                'split': lambda s, sep=None: s.split(sep),
                'replace': lambda s, old, new: s.replace(old, new),
                'find': lambda s, sub: s.find(sub),
                'startswith': lambda s, prefix: s.startswith(prefix),
                'endswith': lambda s, suffix: s.endswith(suffix),
            }
            if node.method in string_methods:
                return string_methods[node.method](obj, *args)

        # Check if it's a list method
        if isinstance(obj, list):
            list_methods = {
                'append': lambda l, x: l.append(x) or l,
                'extend': lambda l, x: l.extend(x) or l,
                'pop': lambda l, i=-1: l.pop(i),
                'insert': lambda l, i, x: l.insert(i, x) or l,
                'remove': lambda l, x: l.remove(x) or l,
                'reverse': lambda l: l.reverse() or l,
                'sort': lambda l: l.sort() or l,
            }
            if node.method in list_methods:
                return list_methods[node.method](obj, *args)

        raise PyrlRuntimeError(f"Cannot call method '{node.method}' on {type(obj).__name__}")

    # Utility methods
    def get_globals(self) -> Dict[str, Any]:
        """Get all global variables."""
        return self.env.variables.copy()

    def reset(self) -> None:
        """Reset VM state."""
        self.env = Environment()
        self.env.vm = self
        self.output = []
        self._init_builtins()

    def get_variable(self, name: str) -> Any:
        """Get a variable value by name."""
        # Try with sigils first
        if '$' + name in self.env.variables:
            return self.env.get('$' + name)
        elif '@' + name in self.env.variables:
            return self.env.get('@' + name)
        elif '%' + name in self.env.variables:
            return self.env.get('%' + name)
        elif '&' + name in self.env.variables:
            return self.env.get('&' + name)
        # Fallback to direct lookup
        return self.env.get(name)

    def set_variable(self, name: str, value: Any) -> None:
        """Set a variable value by name."""
        # Determine sigil from value type or use default
        if name.startswith(('$', '@', '%', '&')):
            self.env.set(name, value)
        elif isinstance(value, list):
            self.env.set('@' + name, value)
        elif isinstance(value, dict):
            self.env.set('%' + name, value)
        elif callable(value) and not isinstance(value, type):
            self.env.set('&' + name, value)
        else:
            self.env.set('$' + name, value)

    def has_variable(self, name: str) -> bool:
        """Check if a variable exists."""
        # Check with all sigils
        return (self.env.has('$' + name) or
                self.env.has('@' + name) or
                self.env.has('%' + name) or
                self.env.has('&' + name) or
                self.env.has(name))


# ===========================================
# Convenience Functions
# ===========================================

def run(source: str) -> Any:
    """Run Pyrl source code using Lark parser."""
    vm = PyrlVM()
    return vm.run(source)


def run_file(filepath: str) -> Any:
    """Run a Pyrl file using Lark parser."""
    vm = PyrlVM()
    return vm.run_file(filepath)


def create_vm() -> PyrlVM:
    """Create a new Pyrl Lark VM instance."""
    return PyrlVM()
