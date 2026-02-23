"""
Pyrl VM Built-in Functions

Core built-in functions for the Pyrl language including:
- Type conversion (int, float, str, bool, list, dict)
- Math operations (abs, round, min, max, sum, sqrt, sin, cos, etc.)
- String operations (lower, upper, strip, split, join, replace, etc.)
- List operations (append, extend, insert, remove, pop, sort, etc.)
- Dict operations (keys, values, items, get, update, etc.)
- Random operations (random, randint, choice, shuffle)
- Utility operations (enumerate, zip, map, filter, sorted, etc.)
- Regex operations (re_match, re_search, re_findall, re_sub)
- I/O operations (print, input)
- Time operations (time, sleep)
"""
from typing import Any, Dict, Callable
import math
import random
import re
import json
import time as time_module

from .exceptions import PyrlRuntimeError


# Registry for built-in functions
BUILTINS: Dict[str, Callable] = {}


def builtin(name: str):
    """Decorator to register built-in functions.
    
    Args:
        name: The name to register the function under
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        BUILTINS[name] = func
        return func
    return decorator


# ===========================================
# Type Conversion Functions
# ===========================================

@builtin('int')
def pyrl_int(x=None, base=10):
    """Convert value to integer."""
    if x is None:
        return 0
    if isinstance(x, str):
        return int(x, base)
    return int(x)


@builtin('float')
def pyrl_float(x=None):
    """Convert value to float."""
    if x is None:
        return 0.0
    return float(x)


@builtin('str')
def pyrl_str(x=None):
    """Convert value to string."""
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
    """Convert value to boolean."""
    if x is None:
        return False
    return bool(x)


@builtin('list')
def pyrl_list(x=None):
    """Convert value to list."""
    if x is None:
        return []
    return list(x)


@builtin('dict')
def pyrl_dict(x=None):
    """Convert value to dict."""
    if x is None:
        return {}
    return dict(x)


@builtin('len')
def pyrl_len(x):
    """Get length of a sequence."""
    return len(x)


@builtin('range')
def pyrl_range(start, stop=None, step=1):
    """Generate a range of numbers."""
    if stop is None:
        return list(range(int(start)))
    return list(range(int(start), int(stop), int(step)))


@builtin('type')
def pyrl_type(x):
    """Get the type of a value."""
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


# ===========================================
# Math Functions
# ===========================================

@builtin('abs')
def pyrl_abs(x):
    """Get absolute value."""
    return abs(x)


@builtin('round')
def pyrl_round(x, ndigits=0):
    """Round to nearest integer or given precision."""
    return round(x, ndigits)


@builtin('min')
def pyrl_min(*args):
    """Get minimum value."""
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        return min(args[0])
    return min(args)


@builtin('max')
def pyrl_max(*args):
    """Get maximum value."""
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        return max(args[0])
    return max(args)


@builtin('sum')
def pyrl_sum(iterable, start=0):
    """Sum all values in an iterable."""
    return sum(iterable, start)


@builtin('pow')
def pyrl_pow(x, y, z=None):
    """Raise x to the power y."""
    if z is None:
        return x ** y
    return pow(x, y, z)


@builtin('sqrt')
def pyrl_sqrt(x):
    """Get square root."""
    return math.sqrt(x)


@builtin('sin')
def pyrl_sin(x):
    """Get sine of x (in radians)."""
    return math.sin(x)


@builtin('cos')
def pyrl_cos(x):
    """Get cosine of x (in radians)."""
    return math.cos(x)


@builtin('tan')
def pyrl_tan(x):
    """Get tangent of x (in radians)."""
    return math.tan(x)


@builtin('log')
def pyrl_log(x, base=None):
    """Get logarithm of x."""
    if base is None:
        return math.log(x)
    return math.log(x, base)


@builtin('exp')
def pyrl_exp(x):
    """Get e raised to the power x."""
    return math.exp(x)


@builtin('floor')
def pyrl_floor(x):
    """Get floor of x."""
    return math.floor(x)


@builtin('ceil')
def pyrl_ceil(x):
    """Get ceiling of x."""
    return math.ceil(x)


# ===========================================
# String Functions
# ===========================================

@builtin('lower')
def pyrl_lower(s):
    """Convert string to lowercase."""
    return str(s).lower()


@builtin('upper')
def pyrl_upper(s):
    """Convert string to uppercase."""
    return str(s).upper()


@builtin('strip')
def pyrl_strip(s, chars=None):
    """Strip characters from both ends of string."""
    return str(s).strip(chars)


@builtin('split')
def pyrl_split(s, sep=None, maxsplit=-1):
    """Split string by separator."""
    return str(s).split(sep, maxsplit)


@builtin('join')
def pyrl_join(sep, iterable):
    """Join iterable with separator."""
    return sep.join(str(x) for x in iterable)


@builtin('replace')
def pyrl_replace(s, old, new, count=-1):
    """Replace occurrences in string."""
    return str(s).replace(old, new, count)


@builtin('find')
def pyrl_find(s, sub, start=0, end=None):
    """Find substring in string."""
    if end is None:
        return str(s).find(sub, start)
    return str(s).find(sub, start, end)


@builtin('startswith')
def pyrl_startswith(s, prefix, start=0, end=None):
    """Check if string starts with prefix."""
    return str(s).startswith(prefix, start, end)


@builtin('endswith')
def pyrl_endswith(s, suffix, start=0, end=None):
    """Check if string ends with suffix."""
    return str(s).endswith(suffix, start, end)


@builtin('format')
def pyrl_format(template, *args, **kwargs):
    """Format string with arguments."""
    return template.format(*args, **kwargs)


# ===========================================
# List Functions
# ===========================================

@builtin('append')
def pyrl_append(lst, item):
    """Append item to list."""
    lst.append(item)
    return lst


@builtin('extend')
def pyrl_extend(lst, items):
    """Extend list with items."""
    lst.extend(items)
    return lst


@builtin('insert')
def pyrl_insert(lst, index, item):
    """Insert item at index in list."""
    lst.insert(index, item)
    return lst


@builtin('remove')
def pyrl_remove(lst, item):
    """Remove first occurrence of item from list."""
    lst.remove(item)
    return lst


@builtin('pop')
def pyrl_pop(lst, index=-1):
    """Pop item from list at index."""
    return lst.pop(index)


@builtin('index')
def pyrl_index(lst, item, start=0, end=None):
    """Get index of item in list."""
    if end is None:
        return lst.index(item, start)
    return lst.index(item, start, end)


@builtin('count')
def pyrl_count(lst, item):
    """Count occurrences of item in list."""
    return lst.count(item)


@builtin('sort')
def pyrl_sort(lst, reverse=False):
    """Sort list in place."""
    lst.sort(reverse=reverse)
    return lst


@builtin('reverse')
def pyrl_reverse(lst):
    """Reverse list in place."""
    lst.reverse()
    return lst


@builtin('copy')
def pyrl_copy(lst):
    """Get a shallow copy of list."""
    return lst.copy()


@builtin('clear')
def pyrl_clear(lst):
    """Clear all items from list."""
    lst.clear()
    return lst


# ===========================================
# Dict Functions
# ===========================================

@builtin('keys')
def pyrl_keys(d):
    """Get keys of dict as list."""
    return list(d.keys())


@builtin('values')
def pyrl_values(d):
    """Get values of dict as list."""
    return list(d.values())


@builtin('items')
def pyrl_items(d):
    """Get items of dict as list of tuples."""
    return list(d.items())


@builtin('get')
def pyrl_get(d, key, default=None):
    """Get value from dict with default."""
    return d.get(key, default)


@builtin('setdefault')
def pyrl_setdefault(d, key, default=None):
    """Set default value for key if not present."""
    return d.setdefault(key, default)


@builtin('update')
def pyrl_update(d, other):
    """Update dict with another dict."""
    d.update(other)
    return d


@builtin('popitem')
def pyrl_popitem(d):
    """Pop an item from dict."""
    return d.popitem()


# ===========================================
# Random Functions
# ===========================================

@builtin('random')
def pyrl_random():
    """Get random float between 0 and 1."""
    return random.random()


@builtin('randint')
def pyrl_randint(a, b):
    """Get random integer between a and b (inclusive)."""
    return random.randint(a, b)


@builtin('choice')
def pyrl_choice(seq):
    """Get random element from sequence."""
    return random.choice(seq)


@builtin('shuffle')
def pyrl_shuffle(lst):
    """Shuffle list in place."""
    random.shuffle(lst)
    return lst


@builtin('seed')
def pyrl_seed(x=None):
    """Set random seed."""
    random.seed(x)


# ===========================================
# Utility Functions
# ===========================================

@builtin('enumerate')
def pyrl_enumerate(iterable, start=0):
    """Enumerate iterable."""
    return list(enumerate(iterable, start))


@builtin('zip')
def pyrl_zip(*iterables):
    """Zip iterables together."""
    return list(zip(*iterables))


@builtin('map')
def pyrl_map(func, iterable):
    """Map function over iterable."""
    return list(map(func, iterable))


@builtin('filter')
def pyrl_filter(func, iterable):
    """Filter iterable by function."""
    return list(filter(func, iterable))


@builtin('sorted')
def pyrl_sorted(iterable, reverse=False, key=None):
    """Get sorted copy of iterable."""
    return sorted(iterable, reverse=reverse, key=key)


@builtin('reversed')
def pyrl_reversed(iterable):
    """Get reversed copy of iterable."""
    return list(reversed(iterable))


@builtin('any')
def pyrl_any(iterable):
    """Check if any element is true."""
    return any(iterable)


@builtin('all')
def pyrl_all(iterable):
    """Check if all elements are true."""
    return all(iterable)


@builtin('hasattr')
def pyrl_hasattr(obj, name):
    """Check if object has attribute."""
    return hasattr(obj, name)


@builtin('getattr')
def pyrl_getattr(obj, name, default=None):
    """Get attribute from object."""
    return getattr(obj, name, default)


@builtin('setattr')
def pyrl_setattr(obj, name, value):
    """Set attribute on object."""
    setattr(obj, name, value)


@builtin('callable')
def pyrl_callable(obj):
    """Check if object is callable."""
    return callable(obj)


@builtin('repr')
def pyrl_repr(obj):
    """Get string representation of object."""
    return repr(obj)


@builtin('id')
def pyrl_id(obj):
    """Get unique id of object."""
    return id(obj)


@builtin('hash')
def pyrl_hash(obj):
    """Get hash of object."""
    return hash(obj)


@builtin('dir')
def pyrl_dir(obj=None):
    """Get list of attributes."""
    if obj is None:
        return list(globals().keys())
    return dir(obj)


@builtin('help')
def pyrl_help(obj=None):
    """Get help on object."""
    if obj is None:
        print("Pyrl Interactive Help")
        return None
    print(f"Help on {obj}")
    return None


@builtin('exit')
def pyrl_exit(code=0):
    """Exit the program."""
    import sys
    sys.exit(code)


# ===========================================
# Regex Functions
# ===========================================

@builtin('re_match')
def pyrl_re_match(pattern, string, flags=0):
    """Match regex pattern at beginning of string."""
    match = re.match(pattern, string, flags)
    if match:
        return match.groups()
    return None


@builtin('re_search')
def pyrl_re_search(pattern, string, flags=0):
    """Search regex pattern in string."""
    match = re.search(pattern, string, flags)
    if match:
        return match.groups()
    return None


@builtin('re_findall')
def pyrl_re_findall(pattern, string, flags=0):
    """Find all matches of regex pattern."""
    return re.findall(pattern, string, flags)


@builtin('re_sub')
def pyrl_re_sub(pattern, repl, string, count=0, flags=0):
    """Replace regex matches in string."""
    return re.sub(pattern, repl, string, count, flags)


@builtin('re_split')
def pyrl_re_split(pattern, string, maxsplit=0, flags=0):
    """Split string by regex pattern."""
    return re.split(pattern, string, maxsplit, flags)


# ===========================================
# I/O Functions
# ===========================================

@builtin('print')
def pyrl_print(*args):
    """Print values to stdout."""
    output = ' '.join(pyrl_str(arg) for arg in args)
    print(output)
    return None


@builtin('input')
def pyrl_input(prompt=None):
    """Read input from stdin."""
    if prompt:
        print(prompt, end='')
    return input()


# ===========================================
# Time Functions
# ===========================================

@builtin('time')
def pyrl_time():
    """Get current time in seconds since epoch."""
    return time_module.time()


@builtin('sleep')
def pyrl_sleep(seconds):
    """Sleep for given seconds."""
    time_module.sleep(seconds)
    return None


# ===========================================
# JSON Functions
# ===========================================

@builtin('json_parse')
def pyrl_json_parse(s):
    """Parse JSON string to value."""
    return json.loads(s)


@builtin('json_stringify')
def pyrl_json_stringify(obj, indent=None):
    """Convert value to JSON string."""
    return json.dumps(obj, indent=indent, default=str)


# ===========================================
# Constants
# ===========================================

CONSTANTS = {
    'True': True,
    'False': False,
    'None': None,
    'PI': math.pi,
    'E': math.e,
    'INF': float('inf'),
    'NAN': float('nan'),
}
