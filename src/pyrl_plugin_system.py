# FILE: pyrl_plugin_system.py
"""
Pyrl Plugin System
Enables extending Pyrl VM with external plugins

Version: 1.0.0
Author: Pyrl Ecosystem Team

Features:
- Plugin discovery and loading
- Plugin lifecycle management
- Hook system for extending functionality
- Plugin isolation and sandboxing
"""

import os
import sys
import json
import importlib.util
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class PluginState(Enum):
    """Plugin lifecycle states"""
    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"
    ACTIVE = "active"
    ERROR = "error"


@dataclass
class PluginInfo:
    """Plugin metadata and information"""
    name: str
    version: str
    description: str
    author: str
    main_file: str
    dependencies: List[str] = field(default_factory=list)
    hooks: List[str] = field(default_factory=list)
    provides_functions: List[str] = field(default_factory=list)
    state: PluginState = PluginState.UNLOADED
    error_message: str = ""


@dataclass
class HookContext:
    """Context passed to hook handlers"""
    hook_name: str
    data: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    cancelled: bool = False
    
    def cancel(self):
        """Cancel the hook propagation"""
        self.cancelled = True


class PluginBase:
    """Base class for Pyrl plugins"""
    
    NAME = "unknown"
    VERSION = "0.0.1"
    DESCRIPTION = "No description"
    AUTHOR = "Unknown"
    
    def __init__(self, plugin_manager: 'PluginManager'):
        self.plugin_manager = plugin_manager
        self.hooks: Dict[str, Callable] = {}
        self.functions: Dict[str, Callable] = {}
    
    def on_load(self):
        """Called when plugin is loaded"""
        pass
    
    def on_activate(self):
        """Called when plugin is activated"""
        pass
    
    def on_deactivate(self):
        """Called when plugin is deactivated"""
        pass
    
    def on_unload(self):
        """Called when plugin is unloaded"""
        pass
    
    def register_hook(self, hook_name: str, handler: Callable):
        """Register a hook handler"""
        self.hooks[hook_name] = handler
        self.plugin_manager.register_hook(hook_name, handler, self)
    
    def register_function(self, name: str, func: Callable):
        """Register a Pyrl function"""
        self.functions[name] = func
        self.plugin_manager.register_plugin_function(name, func, self)
    
    def log(self, message: str, level: str = "info"):
        """Log a message through the plugin manager"""
        self.plugin_manager.log(f"[{self.NAME}] {message}", level)


class PluginManager:
    """Manages plugin lifecycle and integration with Pyrl VM"""
    
    def __init__(self, vm=None):
        self.vm = vm
        self.plugins: Dict[str, PluginInfo] = {}
        self.plugin_instances: Dict[str, PluginBase] = {}
        self.hooks: Dict[str, List[tuple]] = {}  # hook_name -> [(handler, plugin)]
        self.plugin_functions: Dict[str, tuple] = {}  # func_name -> (func, plugin)
        self.plugin_directories: List[str] = []
        self.log_handlers: List[Callable] = []
        
        # Built-in hooks
        self._builtin_hooks = [
            "before_execute",
            "after_execute",
            "before_parse",
            "after_parse",
            "on_function_call",
            "on_variable_access",
            "on_error",
            "on_test_start",
            "on_test_end",
            "on_vue_generate",
        ]
        
        for hook in self._builtin_hooks:
            self.hooks[hook] = []
    
    def add_plugin_directory(self, path: str):
        """Add a directory to search for plugins"""
        if os.path.isdir(path):
            self.plugin_directories.append(path)
    
    def discover_plugins(self) -> List[PluginInfo]:
        """Discover all available plugins in plugin directories"""
        discovered = []
        
        for directory in self.plugin_directories:
            if not os.path.isdir(directory):
                continue
            
            for item in os.listdir(directory):
                plugin_path = os.path.join(directory, item)
                
                # Check for plugin manifest
                manifest_path = os.path.join(plugin_path, "plugin.json")
                if os.path.isfile(manifest_path):
                    try:
                        with open(manifest_path, 'r') as f:
                            manifest = json.load(f)
                        
                        info = PluginInfo(
                            name=manifest.get('name', item),
                            version=manifest.get('version', '0.0.1'),
                            description=manifest.get('description', ''),
                            author=manifest.get('author', 'Unknown'),
                            main_file=manifest.get('main', 'plugin.py'),
                            dependencies=manifest.get('dependencies', []),
                            hooks=manifest.get('hooks', []),
                            provides_functions=manifest.get('functions', [])
                        )
                        
                        self.plugins[info.name] = info
                        discovered.append(info)
                        
                    except Exception as e:
                        self.log(f"Error loading plugin manifest {manifest_path}: {e}", "error")
        
        return discovered
    
    def load_plugin(self, name: str) -> bool:
        """Load a plugin by name"""
        if name not in self.plugins:
            self.log(f"Plugin {name} not found", "error")
            return False
        
        info = self.plugins[name]
        if info.state in (PluginState.LOADED, PluginState.ACTIVE):
            return True
        
        info.state = PluginState.LOADING
        
        try:
            # Find plugin directory
            plugin_dir = None
            for directory in self.plugin_directories:
                candidate = os.path.join(directory, name)
                if os.path.isdir(candidate):
                    plugin_dir = candidate
                    break
            
            if not plugin_dir:
                raise FileNotFoundError(f"Plugin directory not found for {name}")
            
            # Load plugin module
            main_file = os.path.join(plugin_dir, info.main_file)
            if not os.path.isfile(main_file):
                raise FileNotFoundError(f"Plugin main file not found: {main_file}")
            
            spec = importlib.util.spec_from_file_location(f"pyrl_plugin_{name}", main_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"pyrl_plugin_{name}"] = module
            spec.loader.exec_module(module)
            
            # Find plugin class
            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, PluginBase) and attr is not PluginBase:
                    plugin_class = attr
                    break
            
            if not plugin_class:
                raise ValueError(f"No PluginBase subclass found in {main_file}")
            
            # Instantiate plugin
            instance = plugin_class(self)
            self.plugin_instances[name] = instance
            
            # Call on_load
            instance.on_load()
            
            # Register with VM if available
            if self.vm:
                for func_name, func in instance.functions.items():
                    self.vm.register_function(f"&{func_name}", func)
            
            info.state = PluginState.LOADED
            self.log(f"Plugin {name} v{info.version} loaded successfully")
            return True
            
        except Exception as e:
            info.state = PluginState.ERROR
            info.error_message = str(e)
            self.log(f"Error loading plugin {name}: {e}", "error")
            return False
    
    def activate_plugin(self, name: str) -> bool:
        """Activate a loaded plugin"""
        if name not in self.plugins:
            return False
        
        info = self.plugins[name]
        if info.state != PluginState.LOADED:
            if not self.load_plugin(name):
                return False
        
        try:
            instance = self.plugin_instances.get(name)
            if instance:
                instance.on_activate()
            
            info.state = PluginState.ACTIVE
            self.log(f"Plugin {name} activated")
            return True
            
        except Exception as e:
            info.state = PluginState.ERROR
            info.error_message = str(e)
            self.log(f"Error activating plugin {name}: {e}", "error")
            return False
    
    def deactivate_plugin(self, name: str) -> bool:
        """Deactivate an active plugin"""
        if name not in self.plugins:
            return False
        
        info = self.plugins[name]
        
        try:
            instance = self.plugin_instances.get(name)
            if instance:
                instance.on_deactivate()
            
            info.state = PluginState.LOADED
            self.log(f"Plugin {name} deactivated")
            return True
            
        except Exception as e:
            self.log(f"Error deactivating plugin {name}: {e}", "error")
            return False
    
    def unload_plugin(self, name: str) -> bool:
        """Unload a plugin completely"""
        if name not in self.plugins:
            return False
        
        info = self.plugins[name]
        
        try:
            # Deactivate if active
            if info.state == PluginState.ACTIVE:
                self.deactivate_plugin(name)
            
            # Call on_unload
            instance = self.plugin_instances.get(name)
            if instance:
                instance.on_unload()
                
                # Unregister hooks
                for hook_name, handler in instance.hooks.items():
                    if hook_name in self.hooks:
                        self.hooks[hook_name] = [
                            (h, p) for h, p in self.hooks[hook_name]
                            if p != instance
                        ]
                
                # Unregister functions
                for func_name in instance.functions:
                    if func_name in self.plugin_functions:
                        del self.plugin_functions[func_name]
            
            # Remove instance
            if name in self.plugin_instances:
                del self.plugin_instances[name]
            
            # Remove from sys.modules
            module_name = f"pyrl_plugin_{name}"
            if module_name in sys.modules:
                del sys.modules[module_name]
            
            info.state = PluginState.UNLOADED
            self.log(f"Plugin {name} unloaded")
            return True
            
        except Exception as e:
            self.log(f"Error unloading plugin {name}: {e}", "error")
            return False
    
    def register_hook(self, hook_name: str, handler: Callable, plugin: PluginBase):
        """Register a hook handler from a plugin"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        
        self.hooks[hook_name].append((handler, plugin))
    
    def register_plugin_function(self, name: str, func: Callable, plugin: PluginBase):
        """Register a function from a plugin"""
        self.plugin_functions[name] = (func, plugin)
    
    def execute_hook(self, hook_name: str, data: Any = None, metadata: Dict = None) -> HookContext:
        """Execute all handlers for a hook"""
        context = HookContext(
            hook_name=hook_name,
            data=data,
            metadata=metadata or {}
        )
        
        handlers = self.hooks.get(hook_name, [])
        for handler, plugin in handlers:
            if context.cancelled:
                break
            
            try:
                result = handler(context)
                if result is not None:
                    context.data = result
            except Exception as e:
                self.log(f"Error in hook {hook_name} from plugin {plugin.NAME}: {e}", "error")
        
        return context
    
    def get_plugin_info(self, name: str) -> Optional[PluginInfo]:
        """Get information about a plugin"""
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[PluginInfo]:
        """List all discovered plugins"""
        return list(self.plugins.values())
    
    def log(self, message: str, level: str = "info"):
        """Log a message"""
        for handler in self.log_handlers:
            try:
                handler(message, level)
            except:
                pass
        
        # Default to print
        print(f"[PluginManager:{level.upper()}] {message}")
    
    def add_log_handler(self, handler: Callable):
        """Add a custom log handler"""
        self.log_handlers.append(handler)


# ============================================================================
# EXAMPLE PLUGINS
# ============================================================================

class MathPlugin(PluginBase):
    """Extended math functions for Pyrl"""
    
    NAME = "math_extended"
    VERSION = "1.0.0"
    DESCRIPTION = "Extended mathematical functions"
    AUTHOR = "Pyrl Team"
    
    def on_load(self):
        # Register math functions
        self.register_function("sqrt", self._sqrt)
        self.register_function("pow", self._pow)
        self.register_function("log", self._log)
        self.register_function("sin", self._sin)
        self.register_function("cos", self._cos)
        self.register_function("tan", self._tan)
        self.register_function("pi", self._pi)
        self.register_function("e", self._e)
        self.register_function("floor", self._floor)
        self.register_function("ceil", self._ceil)
    
    def _sqrt(self, x):
        import math
        return math.sqrt(x)
    
    def _pow(self, base, exp):
        return base ** exp
    
    def _log(self, x, base=None):
        import math
        if base:
            return math.log(x, base)
        return math.log(x)
    
    def _sin(self, x):
        import math
        return math.sin(x)
    
    def _cos(self, x):
        import math
        return math.cos(x)
    
    def _tan(self, x):
        import math
        return math.tan(x)
    
    def _pi(self):
        import math
        return math.pi
    
    def _e(self):
        import math
        return math.e
    
    def _floor(self, x):
        import math
        return math.floor(x)
    
    def _ceil(self, x):
        import math
        return math.ceil(x)


class DateTimePlugin(PluginBase):
    """Date and time functions for Pyrl"""
    
    NAME = "datetime"
    VERSION = "1.0.0"
    DESCRIPTION = "Date and time manipulation functions"
    AUTHOR = "Pyrl Team"
    
    def on_load(self):
        self.register_function("now", self._now)
        self.register_function("today", self._today)
        self.register_function("format_date", self._format_date)
        self.register_function("parse_date", self._parse_date)
        self.register_function("date_add", self._date_add)
        self.register_function("date_diff", self._date_diff)
        self.register_function("timestamp", self._timestamp)
    
    def _now(self):
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _today(self):
        from datetime import date
        return date.today().isoformat()
    
    def _format_date(self, date_str, fmt="%Y-%m-%d"):
        from datetime import datetime
        dt = datetime.fromisoformat(date_str)
        return dt.strftime(fmt)
    
    def _parse_date(self, date_str, fmt="%Y-%m-%d"):
        from datetime import datetime
        dt = datetime.strptime(date_str, fmt)
        return dt.isoformat()
    
    def _date_add(self, date_str, days=0, hours=0, minutes=0):
        from datetime import datetime, timedelta
        dt = datetime.fromisoformat(date_str)
        delta = timedelta(days=days, hours=hours, minutes=minutes)
        return (dt + delta).isoformat()
    
    def _date_diff(self, date1_str, date2_str):
        from datetime import datetime
        dt1 = datetime.fromisoformat(date1_str)
        dt2 = datetime.fromisoformat(date2_str)
        return (dt2 - dt1).total_seconds()
    
    def _timestamp(self):
        import time
        return int(time.time())


class HTTPPlugin(PluginBase):
    """HTTP client functions for Pyrl"""
    
    NAME = "http_client"
    VERSION = "1.0.0"
    DESCRIPTION = "HTTP client functions for API calls"
    AUTHOR = "Pyrl Team"
    
    def on_load(self):
        self.register_function("http_get", self._get)
        self.register_function("http_post", self._post)
        self.register_function("http_put", self._put)
        self.register_function("http_delete", self._delete)
        self.register_function("json_parse", self._json_parse)
        self.register_function("json_stringify", self._json_stringify)
    
    def _get(self, url, headers=None):
        import urllib.request
        import json
        req = urllib.request.Request(url, method='GET')
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    
    def _post(self, url, data, headers=None):
        import urllib.request
        import json
        if isinstance(data, dict):
            data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    
    def _put(self, url, data, headers=None):
        import urllib.request
        import json
        if isinstance(data, dict):
            data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='PUT')
        req.add_header('Content-Type', 'application/json')
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    
    def _delete(self, url, headers=None):
        import urllib.request
        req = urllib.request.Request(url, method='DELETE')
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    
    def _json_parse(self, s):
        import json
        return json.loads(s)
    
    def _json_stringify(self, obj):
        import json
        return json.dumps(obj)


class CryptoPlugin(PluginBase):
    """Cryptographic functions for Pyrl"""
    
    NAME = "crypto"
    VERSION = "1.0.0"
    DESCRIPTION = "Cryptographic and hashing functions"
    AUTHOR = "Pyrl Team"
    
    def on_load(self):
        self.register_function("md5", self._md5)
        self.register_function("sha1", self._sha1)
        self.register_function("sha256", self._sha256)
        self.register_function("base64_encode", self._base64_encode)
        self.register_function("base64_decode", self._base64_decode)
        self.register_function("uuid", self._uuid)
        self.register_function("random_string", self._random_string)
    
    def _md5(self, s):
        import hashlib
        return hashlib.md5(s.encode()).hexdigest()
    
    def _sha1(self, s):
        import hashlib
        return hashlib.sha1(s.encode()).hexdigest()
    
    def _sha256(self, s):
        import hashlib
        return hashlib.sha256(s.encode()).hexdigest()
    
    def _base64_encode(self, s):
        import base64
        return base64.b64encode(s.encode()).decode()
    
    def _base64_decode(self, s):
        import base64
        return base64.b64decode(s).decode()
    
    def _uuid(self):
        import uuid
        return str(uuid.uuid4())
    
    def _random_string(self, length=16):
        import secrets
        import string
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))


# ============================================================================
# PLUGIN FACTORY
# ============================================================================

def create_plugin_manager(vm=None, plugin_dirs: List[str] = None) -> PluginManager:
    """Create and configure a plugin manager"""
    manager = PluginManager(vm)
    
    # Add default plugin directories
    if plugin_dirs:
        for d in plugin_dirs:
            manager.add_plugin_directory(d)
    
    # Built-in plugins directory
    builtin_dir = os.path.join(os.path.dirname(__file__), 'plugins')
    if os.path.isdir(builtin_dir):
        manager.add_plugin_directory(builtin_dir)
    
    return manager


def load_builtin_plugins(manager: PluginManager):
    """Load built-in plugins directly"""
    # Create instances of built-in plugins
    builtin_plugins = [MathPlugin, DateTimePlugin, HTTPPlugin, CryptoPlugin]
    
    for plugin_class in builtin_plugins:
        instance = plugin_class(manager)
        
        # Store info
        info = PluginInfo(
            name=instance.NAME,
            version=instance.VERSION,
            description=instance.DESCRIPTION,
            author=instance.AUTHOR,
            main_file="<builtin>",
            state=PluginState.LOADED
        )
        manager.plugins[instance.NAME] = info
        manager.plugin_instances[instance.NAME] = instance
        
        # Load plugin
        instance.on_load()
        
        # Register with VM
        if manager.vm:
            for func_name, func in instance.functions.items():
                manager.vm.register_function(f"&{func_name}", func)
        
        info.state = PluginState.ACTIVE


if __name__ == "__main__":
    # Test plugin system
    print("=" * 60)
    print("Pyrl Plugin System Test")
    print("=" * 60)
    
    manager = create_plugin_manager()
    load_builtin_plugins(manager)
    
    print("\nLoaded plugins:")
    for plugin in manager.list_plugins():
        print(f"  - {plugin.name} v{plugin.version}: {plugin.description}")
        print(f"    State: {plugin.state.value}")
    
    print("\nRegistered functions:")
    for name in sorted(manager.plugin_functions.keys()):
        func, plugin = manager.plugin_functions[name]
        print(f"  - &{name} (from {plugin.NAME})")
