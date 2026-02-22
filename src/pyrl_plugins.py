# FILE: pyrl_plugins.py
"""
Pyrl Plugin System
Enables dynamic extension of Pyrl language capabilities

This system allows:
1. Loading external plugins
2. Registering new functions, operators, and syntax extensions
3. Hot-reloading plugins during runtime
4. AI-driven plugin generation
"""

import os
import json
import importlib.util
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass, field
from pathlib import Path
import hashlib


@dataclass
class PluginMetadata:
    """Metadata for a Pyrl plugin"""
    name: str
    version: str
    author: str
    description: str
    dependencies: List[str] = field(default_factory=list)
    provides_functions: List[str] = field(default_factory=list)
    provides_operators: List[str] = field(default_factory=list)
    provides_syntax: List[str] = field(default_factory=list)


@dataclass
class Plugin:
    """A loaded Pyrl plugin"""
    metadata: PluginMetadata
    module: Any
    enabled: bool = True
    load_order: int = 0
    checksum: str = ""


class PluginManager:
    """Manages Pyrl plugins"""
    
    def __init__(self, vm):
        self.vm = vm
        self.plugins: Dict[str, Plugin] = {}
        self.plugin_dirs: List[str] = []
        self.hooks: Dict[str, List[Callable]] = {
            'before_execute': [],
            'after_execute': [],
            'on_error': [],
            'before_parse': [],
            'after_parse': [],
            'on_function_call': [],
            'on_variable_access': [],
        }
        self.operator_handlers: Dict[str, Callable] = {}
        self.syntax_extensions: Dict[str, Any] = {}
        
    def add_plugin_dir(self, path: str) -> None:
        """Add a directory to search for plugins"""
        if os.path.isdir(path):
            self.plugin_dirs.append(path)
    
    def discover_plugins(self) -> List[str]:
        """Discover available plugins in plugin directories"""
        discovered = []
        for plugin_dir in self.plugin_dirs:
            for item in os.listdir(plugin_dir):
                plugin_path = os.path.join(plugin_dir, item)
                if os.path.isdir(plugin_path):
                    manifest_path = os.path.join(plugin_path, 'plugin.json')
                    if os.path.exists(manifest_path):
                        discovered.append(plugin_path)
                elif item.endswith('.py') and not item.startswith('_'):
                    discovered.append(plugin_path)
        return discovered
    
    def load_plugin(self, path: str) -> bool:
        """Load a plugin from path"""
        try:
            if os.path.isdir(path):
                return self._load_plugin_dir(path)
            else:
                return self._load_plugin_file(path)
        except Exception as e:
            print(f"Error loading plugin from {path}: {e}")
            return False
    
    def _load_plugin_dir(self, path: str) -> bool:
        """Load plugin from directory"""
        manifest_path = os.path.join(path, 'plugin.json')
        if not os.path.exists(manifest_path):
            return False
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        metadata = PluginMetadata(
            name=manifest.get('name', 'unknown'),
            version=manifest.get('version', '0.0.0'),
            author=manifest.get('author', 'unknown'),
            description=manifest.get('description', ''),
            dependencies=manifest.get('dependencies', []),
            provides_functions=manifest.get('provides_functions', []),
            provides_operators=manifest.get('provides_operators', []),
            provides_syntax=manifest.get('provides_syntax', [])
        )
        
        # Load main module
        main_file = os.path.join(path, 'main.py')
        if not os.path.exists(main_file):
            main_file = os.path.join(path, f"{metadata.name}.py")
        
        if os.path.exists(main_file):
            spec = importlib.util.spec_from_file_location(metadata.name, main_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Calculate checksum
            with open(main_file, 'rb') as f:
                checksum = hashlib.md5(f.read()).hexdigest()
            
            plugin = Plugin(
                metadata=metadata,
                module=module,
                checksum=checksum
            )
            
            # Register plugin
            self.plugins[metadata.name] = plugin
            
            # Initialize plugin
            if hasattr(module, 'initialize'):
                module.initialize(self.vm, self)
            
            # Register functions
            self._register_plugin_functions(plugin)
            
            return True
        
        return False
    
    def _load_plugin_file(self, path: str) -> bool:
        """Load plugin from single Python file"""
        name = os.path.splitext(os.path.basename(path))[0]
        
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Get metadata from module attributes
        metadata = PluginMetadata(
            name=getattr(module, 'PLUGIN_NAME', name),
            version=getattr(module, 'PLUGIN_VERSION', '0.0.0'),
            author=getattr(module, 'PLUGIN_AUTHOR', 'unknown'),
            description=getattr(module, 'PLUGIN_DESCRIPTION', ''),
        )
        
        with open(path, 'rb') as f:
            checksum = hashlib.md5(f.read()).hexdigest()
        
        plugin = Plugin(
            metadata=metadata,
            module=module,
            checksum=checksum
        )
        
        self.plugins[metadata.name] = plugin
        
        if hasattr(module, 'initialize'):
            module.initialize(self.vm, self)
        
        self._register_plugin_functions(plugin)
        
        return True
    
    def _register_plugin_functions(self, plugin: Plugin) -> None:
        """Register functions provided by plugin"""
        module = plugin.module
        
        for func_name in plugin.metadata.provides_functions:
            if hasattr(module, func_name):
                func = getattr(module, func_name)
                if callable(func):
                    self.vm.register_function(f'&{func_name}', func)
    
    def unload_plugin(self, name: str) -> bool:
        """Unload a plugin by name"""
        if name not in self.plugins:
            return False
        
        plugin = self.plugins[name]
        
        # Call cleanup if available
        if hasattr(plugin.module, 'cleanup'):
            plugin.module.cleanup()
        
        # Unregister functions
        for func_name in plugin.metadata.provides_functions:
            if func_name in self.vm.memory['functions']:
                del self.vm.memory['functions'][func_name]
        
        del self.plugins[name]
        return True
    
    def reload_plugin(self, name: str) -> bool:
        """Reload a plugin"""
        if name not in self.plugins:
            return False
        
        plugin = self.plugins[name]
        
        # Check if file changed
        # For simplicity, always reload
        self.unload_plugin(name)
        
        # Find plugin path and reload
        for plugin_dir in self.plugin_dirs:
            plugin_path = os.path.join(plugin_dir, name)
            if os.path.exists(plugin_path):
                return self.load_plugin(plugin_path)
            single_file = os.path.join(plugin_dir, f"{name}.py")
            if os.path.exists(single_file):
                return self.load_plugin(single_file)
        
        return False
    
    def register_hook(self, hook_name: str, callback: Callable) -> None:
        """Register a hook callback"""
        if hook_name in self.hooks:
            self.hooks[hook_name].append(callback)
    
    def unregister_hook(self, hook_name: str, callback: Callable) -> None:
        """Unregister a hook callback"""
        if hook_name in self.hooks and callback in self.hooks[hook_name]:
            self.hooks[hook_name].remove(callback)
    
    def trigger_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Trigger all callbacks for a hook"""
        results = []
        if hook_name in self.hooks:
            for callback in self.hooks[hook_name]:
                try:
                    result = callback(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"Hook callback error: {e}")
        return results
    
    def register_operator(self, op: str, handler: Callable) -> None:
        """Register a custom operator"""
        self.operator_handlers[op] = handler
    
    def get_operator_handler(self, op: str) -> Optional[Callable]:
        """Get handler for custom operator"""
        return self.operator_handlers.get(op)
    
    def register_syntax_extension(self, name: str, extension: Any) -> None:
        """Register a syntax extension"""
        self.syntax_extensions[name] = extension
    
    def list_plugins(self) -> List[Dict]:
        """List all loaded plugins"""
        return [
            {
                'name': p.metadata.name,
                'version': p.metadata.version,
                'author': p.metadata.author,
                'description': p.metadata.description,
                'enabled': p.enabled,
                'provides_functions': p.metadata.provides_functions,
                'provides_operators': p.metadata.provides_operators,
            }
            for p in self.plugins.values()
        ]
    
    def generate_plugin_template(self, name: str, description: str = "") -> str:
        """Generate a plugin template for AI to extend"""
        template = f'''# Plugin: {name}
# Description: {description}

PLUGIN_NAME = "{name}"
PLUGIN_VERSION = "1.0.0"
PLUGIN_AUTHOR = "AI Generated"
PLUGIN_DESCRIPTION = "{description}"

# Functions provided by this plugin
PROVIDES_FUNCTIONS = []

def initialize(vm, plugin_manager):
    """Initialize the plugin"""
    pass

def cleanup():
    """Cleanup when plugin is unloaded"""
    pass

# Add your plugin functions below
'''
        return template


class AIPluginGenerator:
    """Generates Pyrl plugins using AI assistance"""
    
    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager
        self.templates = {
            'data_processing': self._template_data_processing,
            'string_utils': self._template_string_utils,
            'math_operations': self._template_math_operations,
            'validation': self._template_validation,
            'http_client': self._template_http_client,
            'file_operations': self._template_file_operations,
            'database': self._template_database,
            'crypto': self._template_crypto,
        }
    
    def generate_plugin(self, plugin_type: str, name: str, **kwargs) -> str:
        """Generate a plugin of specified type"""
        if plugin_type in self.templates:
            return self.templates[plugin_type](name, **kwargs)
        return self.plugin_manager.generate_plugin_template(name)
    
    def _template_data_processing(self, name: str, **kwargs) -> str:
        return f'''# Plugin: {name}
# Type: Data Processing

PLUGIN_NAME = "{name}"
PLUGIN_VERSION = "1.0.0"
PLUGIN_AUTHOR = "AI Generated"
PLUGIN_DESCRIPTION = "Data processing utilities for Pyrl"

PROVIDES_FUNCTIONS = ["map_array", "filter_array", "reduce_array", "flatten"]

def initialize(vm, plugin_manager):
    pass

def map_array(arr, func):
    """Apply function to each element"""
    return [func(x) for x in arr]

def filter_array(arr, predicate):
    """Filter array by predicate"""
    return [x for x in arr if predicate(x)]

def reduce_array(arr, func, initial=None):
    """Reduce array to single value"""
    from functools import reduce
    return reduce(func, arr, initial) if initial else reduce(func, arr)

def flatten(arr):
    """Flatten nested arrays"""
    result = []
    for item in arr:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
'''
    
    def _template_string_utils(self, name: str, **kwargs) -> str:
        return f'''# Plugin: {name}
# Type: String Utilities

PLUGIN_NAME = "{name}"
PLUGIN_VERSION = "1.0.0"
PLUGIN_AUTHOR = "AI Generated"
PLUGIN_DESCRIPTION = "String manipulation utilities"

PROVIDES_FUNCTIONS = ["capitalize_words", "reverse_string", "count_occurrences", "is_palindrome"]

def initialize(vm, plugin_manager):
    pass

def capitalize_words(s):
    """Capitalize each word in string"""
    return ' '.join(word.capitalize() for word in s.split())

def reverse_string(s):
    """Reverse a string"""
    return s[::-1]

def count_occurrences(s, substring):
    """Count occurrences of substring"""
    return s.count(substring)

def is_palindrome(s):
    """Check if string is palindrome"""
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
'''
    
    def _template_math_operations(self, name: str, **kwargs) -> str:
        return f'''# Plugin: {name}
# Type: Math Operations

PLUGIN_NAME = "{name}"
PLUGIN_VERSION = "1.0.0"
PLUGIN_AUTHOR = "AI Generated"
PLUGIN_DESCRIPTION = "Advanced math operations"

import math

PROVIDES_FUNCTIONS = ["sqrt", "pow", "log", "sin", "cos", "tan", "factorial", "gcd", "lcm"]

def initialize(vm, plugin_manager):
    pass

def sqrt(x):
    return math.sqrt(x)

def pow(base, exp):
    return base ** exp

def log(x, base=math.e):
    return math.log(x, base)

def sin(x):
    return math.sin(x)

def cos(x):
    return math.cos(x)

def tan(x):
    return math.tan(x)

def factorial(n):
    return math.factorial(int(n))

def gcd(a, b):
    return math.gcd(int(a), int(b))

def lcm(a, b):
    return abs(a * b) // math.gcd(int(a), int(b))
'''
    
    def _template_validation(self, name: str, **kwargs) -> str:
        return f'''# Plugin: {name}
# Type: Validation

PLUGIN_NAME = "{name}"
PLUGIN_VERSION = "1.0.0"
PLUGIN_AUTHOR = "AI Generated"
PLUGIN_DESCRIPTION = "Data validation utilities"

import re

PROVIDES_FUNCTIONS = ["is_email", "is_phone", "is_url", "is_numeric", "is_alpha"]

def initialize(vm, plugin_manager):
    pass

def is_email(s):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{{2,}}$'
    return bool(re.match(pattern, s))

def is_phone(s):
    pattern = r'^\\+?[0-9]{{10,15}}$'
    return bool(re.match(pattern, s))

def is_url(s):
    pattern = r'^https?://[\\w.-]+\\.[a-zA-Z]{{2,}}'
    return bool(re.match(pattern, s))

def is_numeric(s):
    return s.replace('.', '').replace('-', '').isdigit()

def is_alpha(s):
    return s.isalpha()
'''
    
    def _template_http_client(self, name: str, **kwargs) -> str:
        return f'''# Plugin: {name}
# Type: HTTP Client

PLUGIN_NAME = "{name}"
PLUGIN_VERSION = "1.0.0"
PLUGIN_AUTHOR = "AI Generated"
PLUGIN_DESCRIPTION = "HTTP client utilities"

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

PROVIDES_FUNCTIONS = ["http_get", "http_post", "http_put", "http_delete"]

def initialize(vm, plugin_manager):
    if not HAS_REQUESTS:
        print("Warning: requests library not installed")

def http_get(url, headers=None):
    if not HAS_REQUESTS:
        return {{"error": "requests not installed"}}
    resp = requests.get(url, headers=headers or {{}})
    return {{"status": resp.status_code, "body": resp.text}}

def http_post(url, data=None, headers=None):
    if not HAS_REQUESTS:
        return {{"error": "requests not installed"}}
    resp = requests.post(url, json=data, headers=headers or {{}})
    return {{"status": resp.status_code, "body": resp.text}}

def http_put(url, data=None, headers=None):
    if not HAS_REQUESTS:
        return {{"error": "requests not installed"}}
    resp = requests.put(url, json=data, headers=headers or {{}})
    return {{"status": resp.status_code, "body": resp.text}}

def http_delete(url, headers=None):
    if not HAS_REQUESTS:
        return {{"error": "requests not installed"}}
    resp = requests.delete(url, headers=headers or {{}})
    return {{"status": resp.status_code, "body": resp.text}}
'''
    
    def _template_file_operations(self, name: str, **kwargs) -> str:
        return f'''# Plugin: {name}
# Type: File Operations

PLUGIN_NAME = "{name}"
PLUGIN_VERSION = "1.0.0"
PLUGIN_AUTHOR = "AI Generated"
PLUGIN_DESCRIPTION = "File system utilities"

import os
import json

PROVIDES_FUNCTIONS = ["read_file", "write_file", "read_json", "write_json", "list_dir", "file_exists"]

def initialize(vm, plugin_manager):
    pass

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(str(content))
    return True

def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def write_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    return True

def list_dir(path):
    return os.listdir(path)

def file_exists(path):
    return os.path.exists(path)
'''
    
    def _template_database(self, name: str, **kwargs) -> str:
        return f'''# Plugin: {name}
# Type: Database

PLUGIN_NAME = "{name}"
PLUGIN_VERSION = "1.0.0"
PLUGIN_AUTHOR = "AI Generated"
PLUGIN_DESCRIPTION = "SQLite database utilities"

import sqlite3
import json

PROVIDES_FUNCTIONS = ["db_connect", "db_query", "db_insert", "db_close"]

_connections = {{}}

def initialize(vm, plugin_manager):
    pass

def db_connect(db_name, path=":memory:"):
    conn = sqlite3.connect(path)
    _connections[db_name] = conn
    return db_name

def db_query(db_name, sql, params=None):
    conn = _connections.get(db_name)
    if not conn:
        return {{"error": "Connection not found"}}
    cursor = conn.cursor()
    if params:
        cursor.execute(sql, params)
    else:
        cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]

def db_insert(db_name, table, data):
    conn = _connections.get(db_name)
    if not conn:
        return {{"error": "Connection not found"}}
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data])
    sql = f"INSERT INTO {{table}} ({{columns}}) VALUES ({{placeholders}})"
    cursor = conn.cursor()
    cursor.execute(sql, list(data.values()))
    conn.commit()
    return cursor.lastrowid

def db_close(db_name):
    conn = _connections.pop(db_name, None)
    if conn:
        conn.close()
        return True
    return False
'''
    
    def _template_crypto(self, name: str, **kwargs) -> str:
        return f'''# Plugin: {name}
# Type: Cryptography

PLUGIN_NAME = "{name}"
PLUGIN_VERSION = "1.0.0"
PLUGIN_AUTHOR = "AI Generated"
PLUGIN_DESCRIPTION = "Cryptography utilities"

import hashlib
import base64
import secrets
import string

PROVIDES_FUNCTIONS = ["md5", "sha256", "base64_encode", "base64_decode", "generate_token", "hash_password"]

def initialize(vm, plugin_manager):
    pass

def md5(s):
    return hashlib.md5(s.encode()).hexdigest()

def sha256(s):
    return hashlib.sha256(s.encode()).hexdigest()

def base64_encode(s):
    return base64.b64encode(s.encode()).decode()

def base64_decode(s):
    return base64.b64decode(s.encode()).decode()

def generate_token(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    hash_val = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{{salt}}:{{hash_val.hex()}}"
'''


def create_plugin_from_description(description: str, name: str = "custom_plugin") -> str:
    """Create a plugin based on natural language description"""
    # This function would be called by AI to generate plugins
    generator = AIPluginGenerator(None)
    
    # Detect plugin type from description
    desc_lower = description.lower()
    
    if any(word in desc_lower for word in ['http', 'request', 'api', 'web']):
        return generator.generate_plugin('http_client', name)
    elif any(word in desc_lower for word in ['string', 'text', 'format']):
        return generator.generate_plugin('string_utils', name)
    elif any(word in desc_lower for word in ['math', 'calculation', 'number']):
        return generator.generate_plugin('math_operations', name)
    elif any(word in desc_lower for word in ['valid', 'check', 'verify']):
        return generator.generate_plugin('validation', name)
    elif any(word in desc_lower for word in ['file', 'read', 'write', 'disk']):
        return generator.generate_plugin('file_operations', name)
    elif any(word in desc_lower for word in ['database', 'sql', 'db', 'query']):
        return generator.generate_plugin('database', name)
    elif any(word in desc_lower for word in ['encrypt', 'hash', 'crypto', 'secure']):
        return generator.generate_plugin('crypto', name)
    else:
        return generator.generate_plugin('data_processing', name)


# Example built-in plugin for HTTP server extension
BUILTIN_HTTP_PLUGIN = '''
# Plugin: http_server
# Built-in HTTP server extension for Pyrl

PLUGIN_NAME = "http_server"
PLUGIN_VERSION = "1.0.0"
PLUGIN_AUTHOR = "Pyrl Team"
PLUGIN_DESCRIPTION = "HTTP server capabilities for Pyrl"

PROVIDES_FUNCTIONS = ["start_server", "add_route", "stop_server"]

_server = None
_routes = {}

def initialize(vm, plugin_manager):
    """Initialize HTTP server plugin"""
    pass

def start_server(port=8080):
    """Start HTTP server"""
    global _server
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import threading
        
        class PyrlHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path in _routes:
                    handler = _routes[self.path]
                    result = handler()
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(str(result).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def log_message(self, format, *args):
                pass  # Suppress logging
        
        _server = HTTPServer(('0.0.0.0', port), PyrlHandler)
        thread = threading.Thread(target=_server.serve_forever)
        thread.daemon = True
        thread.start()
        return f"Server started on port {port}"
    except Exception as e:
        return f"Error: {str(e)}"

def add_route(path, handler):
    """Add a route handler"""
    _routes[path] = handler
    return f"Route {path} added"

def stop_server():
    """Stop HTTP server"""
    global _server
    if _server:
        _server.shutdown()
        _server = None
        return "Server stopped"
    return "No server running"
'''
