"""
Pyrl Builtins Module
Built-in functions for the Pyrl language.
"""
from typing import Any, List, Dict, Callable
import math
import random
import re
from .exceptions import RuntimeError


class PyrlBuiltin:
    """Wrapper for built-in functions."""
    
    def __init__(self, name: str, func: Callable, min_args: int = 0, max_args: int = None):
        self.name = name
        self.func = func
        self.min_args = min_args
        self.max_args = max_args if max_args is not None else float('inf')
    
    def __call__(self, *args):
        if len(args) < self.min_args:
            raise RuntimeError(f"{self.name}() takes at least {self.min_args} argument(s)")
        if len(args) > self.max_args:
            raise RuntimeError(f"{self.name}() takes at most {self.max_args} argument(s)")
        return self.func(*args)
    
    def __repr__(self):
        return f"<builtin function {self.name}>"


# Type conversion functions
def pyrl_int(x=None, base=10):
    if x is None:
        return 0
    if isinstance(x, str):
        return int(x, base)
    return int(x)


def pyrl_float(x=None):
    if x is None:
        return 0.0
    return float(x)


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


def pyrl_bool(x=None):
    if x is None:
        return False
    return bool(x)


def pyrl_list(x=None):
    if x is None:
        return []
    return list(x)


def pyrl_dict(x=None):
    if x is None:
        return {}
    return dict(x)


def pyrl_len(x):
    return len(x)


def pyrl_range(start, stop=None, step=1):
    if stop is None:
        return list(range(int(start)))
    return list(range(int(start), int(stop), int(step)))


def pyrl_print(*args):
    output = ' '.join(pyrl_str(arg) for arg in args)
    print(output)
    return None


def pyrl_input(prompt=None):
    if prompt:
        print(prompt, end='')
    return input()


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


def pyrl_isinstance(obj, classinfo):
    return isinstance(obj, classinfo)


def pyrl_issubclass(cls, classinfo):
    return issubclass(cls, classinfo)


# Math functions
def pyrl_abs(x):
    return abs(x)


def pyrl_round(x, ndigits=0):
    return round(x, ndigits)


def pyrl_min(*args):
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        return min(args[0])
    return min(args)


def pyrl_max(*args):
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        return max(args[0])
    return max(args)


def pyrl_sum(iterable, start=0):
    return sum(iterable, start)


def pyrl_pow(x, y, z=None):
    if z is None:
        return x ** y
    return pow(x, y, z)


def pyrl_sqrt(x):
    return math.sqrt(x)


def pyrl_sin(x):
    return math.sin(x)


def pyrl_cos(x):
    return math.cos(x)


def pyrl_tan(x):
    return math.tan(x)


def pyrl_log(x, base=None):
    if base is None:
        return math.log(x)
    return math.log(x, base)


def pyrl_exp(x):
    return math.exp(x)


def pyrl_floor(x):
    return math.floor(x)


def pyrl_ceil(x):
    return math.ceil(x)


# String functions
def pyrl_lower(s):
    return str(s).lower()


def pyrl_upper(s):
    return str(s).upper()


def pyrl_strip(s, chars=None):
    return str(s).strip(chars)


def pyrl_split(s, sep=None, maxsplit=-1):
    return str(s).split(sep, maxsplit)


def pyrl_join(sep, iterable):
    return sep.join(str(x) for x in iterable)


def pyrl_replace(s, old, new, count=-1):
    return str(s).replace(old, new, count)


def pyrl_find(s, sub, start=0, end=None):
    if end is None:
        return str(s).find(sub, start)
    return str(s).find(sub, start, end)


def pyrl_startswith(s, prefix, start=0, end=None):
    return str(s).startswith(prefix, start, end)


def pyrl_endswith(s, suffix, start=0, end=None):
    return str(s).endswith(suffix, start, end)


def pyrl_format(template, *args, **kwargs):
    return template.format(*args, **kwargs)


# List functions
def pyrl_append(lst, item):
    lst.append(item)
    return lst


def pyrl_extend(lst, items):
    lst.extend(items)
    return lst


def pyrl_insert(lst, index, item):
    lst.insert(index, item)
    return lst


def pyrl_remove(lst, item):
    lst.remove(item)
    return lst


def pyrl_pop(lst, index=-1):
    return lst.pop(index)


def pyrl_index(lst, item, start=0, end=None):
    if end is None:
        return lst.index(item, start)
    return lst.index(item, start, end)


def pyrl_count(lst, item):
    return lst.count(item)


def pyrl_sort(lst, reverse=False):
    lst.sort(reverse=reverse)
    return lst


def pyrl_reverse(lst):
    lst.reverse()
    return lst


def pyrl_copy(lst):
    return lst.copy()


def pyrl_clear(lst):
    lst.clear()
    return lst


# Dict functions
def pyrl_keys(d):
    return list(d.keys())


def pyrl_values(d):
    return list(d.values())


def pyrl_items(d):
    return list(d.items())


def pyrl_get(d, key, default=None):
    return d.get(key, default)


def pyrl_setdefault(d, key, default=None):
    return d.setdefault(key, default)


def pyrl_update(d, other):
    d.update(other)
    return d


def pyrl_popitem(d):
    return d.popitem()


# Random functions
def pyrl_random():
    return random.random()


def pyrl_randint(a, b):
    return random.randint(a, b)


def pyrl_choice(seq):
    return random.choice(seq)


def pyrl_shuffle(lst):
    random.shuffle(lst)
    return lst


def pyrl_seed(x=None):
    random.seed(x)


# Utility functions
def pyrl_enumerate(iterable, start=0):
    return list(enumerate(iterable, start))


def pyrl_zip(*iterables):
    return list(zip(*iterables))


def pyrl_map(func, iterable):
    return list(map(func, iterable))


def pyrl_filter(func, iterable):
    return list(filter(func, iterable))


def pyrl_sorted(iterable, reverse=False, key=None):
    return sorted(iterable, reverse=reverse, key=key)


def pyrl_reversed(iterable):
    return list(reversed(iterable))


def pyrl_any(iterable):
    return any(iterable)


def pyrl_all(iterable):
    return all(iterable)


def pyrl_hasattr(obj, name):
    return hasattr(obj, name)


def pyrl_getattr(obj, name, default=None):
    return getattr(obj, name, default)


def pyrl_setattr(obj, name, value):
    setattr(obj, name, value)


def pyrl_delattr(obj, name):
    delattr(obj, name)


def pyrl_callable(obj):
    return callable(obj)


def pyrl_repr(obj):
    return repr(obj)


def pyrl_id(obj):
    return id(obj)


def pyrl_hash(obj):
    return hash(obj)


def pyrl_dir(obj=None):
    if obj is None:
        return list(globals().keys())
    return dir(obj)


def pyrl_vars(obj=None):
    if obj is None:
        return globals()
    return vars(obj)


def pyrl_help(obj=None):
    if obj is None:
        print("Pyrl Interactive Help")
        return None
    print(f"Help on {obj}")
    return None


def pyrl_exit(code=0):
    import sys
    sys.exit(code)


# Regular expression functions
def pyrl_re_match(pattern, string, flags=0):
    match = re.match(pattern, string, flags)
    if match:
        return match.groups()
    return None


def pyrl_re_search(pattern, string, flags=0):
    match = re.search(pattern, string, flags)
    if match:
        return match.groups()
    return None


def pyrl_re_findall(pattern, string, flags=0):
    return re.findall(pattern, string, flags)


def pyrl_re_sub(pattern, repl, string, count=0, flags=0):
    return re.sub(pattern, repl, string, count, flags)


def pyrl_re_split(pattern, string, maxsplit=0, flags=0):
    return re.split(pattern, string, maxsplit, flags)


# Get all builtins
def get_builtins() -> Dict[str, PyrlBuiltin]:
    """Return a dictionary of all built-in functions."""
    builtins = {}
    
    # Type conversion
    builtins['int'] = PyrlBuiltin('int', pyrl_int, 0, 2)
    builtins['float'] = PyrlBuiltin('float', pyrl_float, 0, 1)
    builtins['str'] = PyrlBuiltin('str', pyrl_str, 0, 1)
    builtins['bool'] = PyrlBuiltin('bool', pyrl_bool, 0, 1)
    builtins['list'] = PyrlBuiltin('list', pyrl_list, 0, 1)
    builtins['dict'] = PyrlBuiltin('dict', pyrl_dict, 0, 1)
    builtins['len'] = PyrlBuiltin('len', pyrl_len, 1, 1)
    builtins['range'] = PyrlBuiltin('range', pyrl_range, 1, 3)
    builtins['type'] = PyrlBuiltin('type', pyrl_type, 1, 1)
    builtins['isinstance'] = PyrlBuiltin('isinstance', pyrl_isinstance, 2, 2)
    builtins['issubclass'] = PyrlBuiltin('issubclass', pyrl_issubclass, 2, 2)
    
    # Math
    builtins['abs'] = PyrlBuiltin('abs', pyrl_abs, 1, 1)
    builtins['round'] = PyrlBuiltin('round', pyrl_round, 1, 2)
    builtins['min'] = PyrlBuiltin('min', pyrl_min, 1)
    builtins['max'] = PyrlBuiltin('max', pyrl_max, 1)
    builtins['sum'] = PyrlBuiltin('sum', pyrl_sum, 1, 2)
    builtins['pow'] = PyrlBuiltin('pow', pyrl_pow, 2, 3)
    builtins['sqrt'] = PyrlBuiltin('sqrt', pyrl_sqrt, 1, 1)
    builtins['sin'] = PyrlBuiltin('sin', pyrl_sin, 1, 1)
    builtins['cos'] = PyrlBuiltin('cos', pyrl_cos, 1, 1)
    builtins['tan'] = PyrlBuiltin('tan', pyrl_tan, 1, 1)
    builtins['log'] = PyrlBuiltin('log', pyrl_log, 1, 2)
    builtins['exp'] = PyrlBuiltin('exp', pyrl_exp, 1, 1)
    builtins['floor'] = PyrlBuiltin('floor', pyrl_floor, 1, 1)
    builtins['ceil'] = PyrlBuiltin('ceil', pyrl_ceil, 1, 1)
    
    # I/O
    builtins['print'] = PyrlBuiltin('print', pyrl_print, 0)
    builtins['input'] = PyrlBuiltin('input', pyrl_input, 0, 1)
    
    # String
    builtins['lower'] = PyrlBuiltin('lower', pyrl_lower, 1, 1)
    builtins['upper'] = PyrlBuiltin('upper', pyrl_upper, 1, 1)
    builtins['strip'] = PyrlBuiltin('strip', pyrl_strip, 1, 2)
    builtins['split'] = PyrlBuiltin('split', pyrl_split, 1, 3)
    builtins['join'] = PyrlBuiltin('join', pyrl_join, 2, 2)
    builtins['replace'] = PyrlBuiltin('replace', pyrl_replace, 3, 4)
    builtins['find'] = PyrlBuiltin('find', pyrl_find, 2, 4)
    builtins['startswith'] = PyrlBuiltin('startswith', pyrl_startswith, 2, 4)
    builtins['endswith'] = PyrlBuiltin('endswith', pyrl_endswith, 2, 4)
    builtins['format'] = PyrlBuiltin('format', pyrl_format, 1)
    
    # List
    builtins['append'] = PyrlBuiltin('append', pyrl_append, 2, 2)
    builtins['extend'] = PyrlBuiltin('extend', pyrl_extend, 2, 2)
    builtins['insert'] = PyrlBuiltin('insert', pyrl_insert, 3, 3)
    builtins['remove'] = PyrlBuiltin('remove', pyrl_remove, 2, 2)
    builtins['pop'] = PyrlBuiltin('pop', pyrl_pop, 1, 2)
    builtins['index'] = PyrlBuiltin('index', pyrl_index, 2, 4)
    builtins['count'] = PyrlBuiltin('count', pyrl_count, 2, 2)
    builtins['sort'] = PyrlBuiltin('sort', pyrl_sort, 1, 2)
    builtins['reverse'] = PyrlBuiltin('reverse', pyrl_reverse, 1, 1)
    builtins['copy'] = PyrlBuiltin('copy', pyrl_copy, 1, 1)
    builtins['clear'] = PyrlBuiltin('clear', pyrl_clear, 1, 1)
    
    # Dict
    builtins['keys'] = PyrlBuiltin('keys', pyrl_keys, 1, 1)
    builtins['values'] = PyrlBuiltin('values', pyrl_values, 1, 1)
    builtins['items'] = PyrlBuiltin('items', pyrl_items, 1, 1)
    builtins['get'] = PyrlBuiltin('get', pyrl_get, 2, 3)
    builtins['setdefault'] = PyrlBuiltin('setdefault', pyrl_setdefault, 2, 3)
    builtins['update'] = PyrlBuiltin('update', pyrl_update, 2, 2)
    builtins['popitem'] = PyrlBuiltin('popitem', pyrl_popitem, 1, 1)
    
    # Random
    builtins['random'] = PyrlBuiltin('random', pyrl_random, 0, 0)
    builtins['randint'] = PyrlBuiltin('randint', pyrl_randint, 2, 2)
    builtins['choice'] = PyrlBuiltin('choice', pyrl_choice, 1, 1)
    builtins['shuffle'] = PyrlBuiltin('shuffle', pyrl_shuffle, 1, 1)
    builtins['seed'] = PyrlBuiltin('seed', pyrl_seed, 0, 1)
    
    # Utility
    builtins['enumerate'] = PyrlBuiltin('enumerate', pyrl_enumerate, 1, 2)
    builtins['zip'] = PyrlBuiltin('zip', pyrl_zip, 1)
    builtins['map'] = PyrlBuiltin('map', pyrl_map, 2, 2)
    builtins['filter'] = PyrlBuiltin('filter', pyrl_filter, 2, 2)
    builtins['sorted'] = PyrlBuiltin('sorted', pyrl_sorted, 1, 3)
    builtins['reversed'] = PyrlBuiltin('reversed', pyrl_reversed, 1, 1)
    builtins['any'] = PyrlBuiltin('any', pyrl_any, 1, 1)
    builtins['all'] = PyrlBuiltin('all', pyrl_all, 1, 1)
    builtins['hasattr'] = PyrlBuiltin('hasattr', pyrl_hasattr, 2, 2)
    builtins['getattr'] = PyrlBuiltin('getattr', pyrl_getattr, 2, 3)
    builtins['setattr'] = PyrlBuiltin('setattr', pyrl_setattr, 3, 3)
    builtins['delattr'] = PyrlBuiltin('delattr', pyrl_delattr, 2, 2)
    builtins['callable'] = PyrlBuiltin('callable', pyrl_callable, 1, 1)
    builtins['repr'] = PyrlBuiltin('repr', pyrl_repr, 1, 1)
    builtins['id'] = PyrlBuiltin('id', pyrl_id, 1, 1)
    builtins['hash'] = PyrlBuiltin('hash', pyrl_hash, 1, 1)
    builtins['dir'] = PyrlBuiltin('dir', pyrl_dir, 0, 1)
    builtins['vars'] = PyrlBuiltin('vars', pyrl_vars, 0, 1)
    builtins['help'] = PyrlBuiltin('help', pyrl_help, 0, 1)
    builtins['exit'] = PyrlBuiltin('exit', pyrl_exit, 0, 1)
    
    # Regex
    builtins['re_match'] = PyrlBuiltin('re_match', pyrl_re_match, 2, 3)
    builtins['re_search'] = PyrlBuiltin('re_search', pyrl_re_search, 2, 3)
    builtins['re_findall'] = PyrlBuiltin('re_findall', pyrl_re_findall, 2, 3)
    builtins['re_sub'] = PyrlBuiltin('re_sub', pyrl_re_sub, 3, 5)
    builtins['re_split'] = PyrlBuiltin('re_split', pyrl_re_split, 2, 4)
    
    return builtins


# Constants
BUILTIN_CONSTANTS = {
    'True': True,
    'False': False,
    'None': None,
    'PI': 3.141592653589793,
    'E': 2.718281828459045,
    'INF': float('inf'),
    'NAN': float('nan'),
}
