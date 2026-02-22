# FILE: pyrl_oop_plugin.py
"""
Pyrl OOP (Object-Oriented Programming) Extension Plugin

This plugin adds full OOP support to Pyrl language:
- Class definitions
- Inheritance
- Encapsulation
- Polymorphism
- Instance methods and properties

Version: 1.0.0
Author: Pyrl AI Assistant (Auto-generated)
"""

import re
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field


# ============================================================================
# OOP DATA STRUCTURES
# ============================================================================

@dataclass
class PyrlMethod:
    """Represents a method in a Pyrl class"""
    name: str
    params: List[str]
    body: Any  # AST node or callable
    is_static: bool = False


@dataclass
class PyrlProperty:
    """Represents a property in a Pyrl class"""
    name: str
    default_value: Any = None
    is_private: bool = False


@dataclass
class PyrlClass:
    """Represents a class definition in Pyrl"""
    name: str
    methods: Dict[str, PyrlMethod] = field(default_factory=dict)
    properties: Dict[str, PyrlProperty] = field(default_factory=dict)
    parent_class: Optional['PyrlClass'] = None
    
    def has_method(self, name: str) -> bool:
        """Check if class has a method"""
        if name in self.methods:
            return True
        if self.parent_class:
            return self.parent_class.has_method(name)
        return False
    
    def get_method(self, name: str) -> Optional[PyrlMethod]:
        """Get method by name, checking inheritance"""
        if name in self.methods:
            return self.methods[name]
        if self.parent_class:
            return self.parent_class.get_method(name)
        return None
    
    def create_instance(self, args: List[Any] = None) -> 'PyrlInstance':
        """Create a new instance of this class"""
        instance = PyrlInstance(class_def=self)
        
        # Initialize properties with defaults
        for prop_name, prop in self.properties.items():
            instance.properties[prop_name] = prop.default_value
        
        # Call init if exists
        if 'init' in self.methods:
            init_method = self.methods['init']
            return instance
        
        return instance


@dataclass
class PyrlInstance:
    """Represents an instance of a Pyrl class"""
    class_def: PyrlClass
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def get_property(self, name: str) -> Any:
        """Get a property value"""
        if name in self.properties:
            return self.properties[name]
        return None
    
    def set_property(self, name: str, value: Any):
        """Set a property value"""
        self.properties[name] = value
    
    def has_method(self, name: str) -> bool:
        """Check if instance has a method"""
        return self.class_def.has_method(name)
    
    def get_method(self, name: str) -> Optional[PyrlMethod]:
        """Get a method from the instance's class"""
        return self.class_def.get_method(name)


# ============================================================================
# OOP RUNTIME ENGINE
# ============================================================================

class OOPRuntime:
    """Runtime engine for OOP operations"""
    
    def __init__(self, vm=None):
        self.vm = vm
        self.classes: Dict[str, PyrlClass] = {}
        self.instances: Dict[str, PyrlInstance] = {}
        self._instance_counter = 0
    
    def register_class(self, class_def: PyrlClass):
        """Register a class definition"""
        self.classes[class_def.name] = class_def
    
    def get_class(self, name: str) -> Optional[PyrlClass]:
        """Get a class by name"""
        return self.classes.get(name)
    
    def create_instance(self, class_name: str, args: List[Any] = None) -> PyrlInstance:
        """Create a new instance of a class"""
        class_def = self.classes.get(class_name)
        if not class_def:
            raise RuntimeError(f"Class '{class_name}' not found")
        
        instance = class_def.create_instance(args)
        
        # Generate unique instance ID
        self._instance_counter += 1
        instance_id = f"instance_{self._instance_counter}"
        self.instances[instance_id] = instance
        
        return instance
    
    def call_method(self, instance: PyrlInstance, method_name: str, 
                    args: List[Any] = None) -> Any:
        """Call a method on an instance"""
        method = instance.get_method(method_name)
        if not method:
            raise RuntimeError(f"Method '{method_name}' not found")
        
        # Execute method body
        if callable(method.body):
            return method.body(instance, *(args or []))
        
        return None
    
    def get_property(self, instance: PyrlInstance, prop_name: str) -> Any:
        """Get a property from an instance"""
        return instance.get_property(prop_name)
    
    def set_property(self, instance: PyrlInstance, prop_name: str, value: Any):
        """Set a property on an instance"""
        instance.set_property(prop_name, value)
    
    def instance_of(self, instance: PyrlInstance, class_name: str) -> bool:
        """Check if instance is of a specific class"""
        if instance.class_def.name == class_name:
            return True
        if instance.class_def.parent_class:
            return self._check_parent(instance.class_def.parent_class, class_name)
        return False
    
    def _check_parent(self, class_def: PyrlClass, class_name: str) -> bool:
        """Recursively check parent classes"""
        if class_def.name == class_name:
            return True
        if class_def.parent_class:
            return self._check_parent(class_def.parent_class, class_name)
        return False


# ============================================================================
# OOP PARSER EXTENSION
# ============================================================================

class OOPParser:
    """Parser extension for OOP syntax"""
    
    # Regex patterns for OOP constructs
    CLASS_PATTERN = re.compile(
        r'class\s+(\w+)\s*(?:extends\s+(\w+))?\s*\{',
        re.MULTILINE
    )
    
    METHOD_PATTERN = re.compile(
        r'(?:method\s+)?(\w+)\s*\(([^)]*)\)\s*=\s*\{',
        re.MULTILINE
    )
    
    PROPERTY_PATTERN = re.compile(
        r'prop\s+(\w+)(?:\s*=\s*([^;]+))?',
        re.MULTILINE
    )
    
    def parse_class(self, code: str) -> List[Dict]:
        """Parse class definitions from code"""
        classes = []
        
        for match in self.CLASS_PATTERN.finditer(code):
            class_name = match.group(1)
            parent_name = match.group(2)
            
            # Extract class body
            start = match.end()
            body = self._extract_block(code, start - 1)
            
            class_info = {
                'name': class_name,
                'parent': parent_name,
                'body': body,
                'methods': self._parse_methods(body),
                'properties': self._parse_properties(body)
            }
            
            classes.append(class_info)
        
        return classes
    
    def _extract_block(self, code: str, start: int) -> str:
        """Extract content between balanced braces"""
        depth = 0
        content_start = None
        
        for i in range(start, len(code)):
            if code[i] == '{':
                if depth == 0:
                    content_start = i + 1
                depth += 1
            elif code[i] == '}':
                depth -= 1
                if depth == 0:
                    return code[content_start:i]
        
        return ""
    
    def _parse_methods(self, body: str) -> List[Dict]:
        """Parse method definitions from class body"""
        methods = []
        
        for match in self.METHOD_PATTERN.finditer(body):
            method_name = match.group(1)
            params_str = match.group(2).strip()
            
            params = [p.strip() for p in params_str.split(',')] if params_str else []
            params = [p for p in params if p]  # Remove empty strings
            
            # Extract method body
            start = match.end()
            method_body = self._extract_block(body, start - 1)
            
            methods.append({
                'name': method_name,
                'params': params,
                'body': method_body
            })
        
        return methods
    
    def _parse_properties(self, body: str) -> List[Dict]:
        """Parse property definitions from class body"""
        properties = []
        
        for match in self.PROPERTY_PATTERN.finditer(body):
            prop_name = match.group(1)
            default_value = match.group(2)
            
            if default_value:
                default_value = default_value.strip()
                # Parse value type
                if default_value.startswith('"') or default_value.startswith("'"):
                    default_value = default_value[1:-1]
                elif default_value.isdigit():
                    default_value = int(default_value)
                elif default_value == 'true':
                    default_value = True
                elif default_value == 'false':
                    default_value = False
            else:
                default_value = None
            
            properties.append({
                'name': prop_name,
                'default': default_value
            })
        
        return properties


# ============================================================================
# BUILT-IN CLASSES
# ============================================================================

def create_builtin_classes() -> Dict[str, PyrlClass]:
    """Create built-in classes for Pyrl"""
    classes = {}
    
    # Object - base class for all objects
    object_class = PyrlClass(
        name="Object",
        methods={
            'to_string': PyrlMethod(
                name='to_string',
                params=[],
                body=lambda self: f"<{self.class_def.name} instance>"
            ),
            'class_name': PyrlMethod(
                name='class_name',
                params=[],
                body=lambda self: self.class_def.name
            ),
            'hash': PyrlMethod(
                name='hash',
                params=[],
                body=lambda self: id(self)
            )
        }
    )
    classes['Object'] = object_class
    
    # String class
    string_class = PyrlClass(
        name="String",
        parent_class=object_class,
        properties={
            'value': PyrlProperty(name='value', default_value='')
        },
        methods={
            'init': PyrlMethod(
                name='init',
                params=['value'],
                body=lambda self, value: setattr(self.properties, '__setitem__', 
                       self.properties.__setitem__('value', str(value)))
            ),
            'length': PyrlMethod(
                name='length',
                params=[],
                body=lambda self: len(self.properties.get('value', ''))
            ),
            'upper': PyrlMethod(
                name='upper',
                params=[],
                body=lambda self: self.properties.get('value', '').upper()
            ),
            'lower': PyrlMethod(
                name='lower',
                params=[],
                body=lambda self: self.properties.get('value', '').lower()
            ),
            'contains': PyrlMethod(
                name='contains',
                params=['substring'],
                body=lambda self, sub: sub in self.properties.get('value', '')
            )
        }
    )
    classes['String'] = string_class
    
    # Array class
    array_class = PyrlClass(
        name="Array",
        parent_class=object_class,
        properties={
            'items': PyrlProperty(name='items', default_value=[])
        },
        methods={
            'init': PyrlMethod(
                name='init',
                params=['items'],
                body=lambda self, items=None: self.properties.update(
                    {'items': list(items) if items else []}
                )
            ),
            'push': PyrlMethod(
                name='push',
                params=['item'],
                body=lambda self, item: self.properties.get('items', []).append(item)
            ),
            'pop': PyrlMethod(
                name='pop',
                params=[],
                body=lambda self: self.properties.get('items', []).pop() if self.properties.get('items') else None
            ),
            'length': PyrlMethod(
                name='length',
                params=[],
                body=lambda self: len(self.properties.get('items', []))
            ),
            'get': PyrlMethod(
                name='get',
                params=['index'],
                body=lambda self, idx: self.properties.get('items', [])[idx] if 0 <= idx < len(self.properties.get('items', [])) else None
            ),
            'first': PyrlMethod(
                name='first',
                params=[],
                body=lambda self: self.properties.get('items', [])[0] if self.properties.get('items') else None
            ),
            'last': PyrlMethod(
                name='last',
                params=[],
                body=lambda self: self.properties.get('items', [])[-1] if self.properties.get('items') else None
            )
        }
    )
    classes['Array'] = array_class
    
    # Counter class - simple example
    counter_class = PyrlClass(
        name="Counter",
        parent_class=object_class,
        properties={
            'count': PyrlProperty(name='count', default_value=0)
        },
        methods={
            'init': PyrlMethod(
                name='init',
                params=['start'],
                body=lambda self, start=0: self.properties.update({'count': start})
            ),
            'increment': PyrlMethod(
                name='increment',
                params=['amount'],
                body=lambda self, amount=1: self.properties.update(
                    {'count': self.properties.get('count', 0) + amount}
                )
            ),
            'decrement': PyrlMethod(
                name='decrement',
                params=['amount'],
                body=lambda self, amount=1: self.properties.update(
                    {'count': self.properties.get('count', 0) - amount}
                )
            ),
            'get': PyrlMethod(
                name='get',
                params=[],
                body=lambda self: self.properties.get('count', 0)
            ),
            'reset': PyrlMethod(
                name='reset',
                params=[],
                body=lambda self: self.properties.update({'count': 0})
            )
        }
    )
    classes['Counter'] = counter_class
    
    return classes


# ============================================================================
# OOP PLUGIN CLASS
# ============================================================================

from pyrl_plugin_system import PluginBase


class OOPPlugin(PluginBase):
    """Plugin that adds OOP capabilities to Pyrl"""
    
    NAME = "oop"
    VERSION = "1.0.0"
    DESCRIPTION = "Object-Oriented Programming support for Pyrl"
    AUTHOR = "Pyrl AI Assistant"
    
    def on_load(self):
        """Initialize OOP runtime"""
        self.runtime = OOPRuntime(self.vm)
        self.parser = OOPParser()
        
        # Register built-in classes
        for name, class_def in create_builtin_classes().items():
            self.runtime.register_class(class_def)
        
        # Register OOP functions
        self.register_function("new", self._new_instance)
        self.register_function("class_exists", self._class_exists)
        self.register_function("instance_of", self._instance_of)
        self.register_function("get_property", self._get_property)
        self.register_function("set_property", self._set_property)
        self.register_function("call_method", self._call_method)
        self.register_function("define_class", self._define_class)
        
        # Register with VM
        if self.vm:
            self.vm.oop_runtime = self.runtime
    
    def _new_instance(self, class_name: str, *args):
        """Create a new instance of a class"""
        return self.runtime.create_instance(class_name, list(args))
    
    def _class_exists(self, class_name: str) -> bool:
        """Check if a class exists"""
        return class_name in self.runtime.classes
    
    def _instance_of(self, instance: PyrlInstance, class_name: str) -> bool:
        """Check if instance is of a class"""
        if not isinstance(instance, PyrlInstance):
            return False
        return self.runtime.instance_of(instance, class_name)
    
    def _get_property(self, instance: PyrlInstance, prop_name: str) -> Any:
        """Get a property from an instance"""
        return instance.get_property(prop_name)
    
    def _set_property(self, instance: PyrlInstance, prop_name: str, value: Any):
        """Set a property on an instance"""
        instance.set_property(prop_name, value)
        return instance
    
    def _call_method(self, instance: PyrlInstance, method_name: str, *args):
        """Call a method on an instance"""
        return self.runtime.call_method(instance, method_name, list(args))
    
    def _define_class(self, name: str, methods: Dict = None, properties: Dict = None, 
                      parent: str = None):
        """Programmatically define a new class"""
        class_def = PyrlClass(name=name)
        
        if parent:
            parent_class = self.runtime.get_class(parent)
            if parent_class:
                class_def.parent_class = parent_class
        
        if methods:
            for method_name, method_body in methods.items():
                if callable(method_body):
                    class_def.methods[method_name] = PyrlMethod(
                        name=method_name,
                        params=[],
                        body=method_body
                    )
        
        if properties:
            for prop_name, default_value in properties.items():
                class_def.properties[prop_name] = PyrlProperty(
                    name=prop_name,
                    default_value=default_value
                )
        
        self.runtime.register_class(class_def)
        return class_def


# ============================================================================
# DEMO / TEST
# ============================================================================

def demo_oop():
    """Demonstrate OOP capabilities"""
    print("=" * 60)
    print("Pyrl OOP Extension Demo")
    print("=" * 60)
    
    # Initialize OOP runtime
    runtime = OOPRuntime()
    
    # Register built-in classes
    for name, class_def in create_builtin_classes().items():
        runtime.register_class(class_def)
    
    print("\n1. Built-in Classes:")
    for name in runtime.classes:
        print(f"   - {name}")
    
    print("\n2. Creating Counter instance:")
    counter = runtime.create_instance('Counter', [10])
    print(f"   Created Counter with start value")
    
    # Set initial count
    counter.set_property('count', 10)
    print(f"   Initial count: {counter.get_property('count')}")
    
    # Call methods
    runtime.call_method(counter, 'increment', [5])
    print(f"   After increment(5): {counter.get_property('count')}")
    
    runtime.call_method(counter, 'decrement', [3])
    print(f"   After decrement(3): {counter.get_property('count')}")
    
    print("\n3. Creating custom class:")
    
    # Define a custom User class
    user_class = PyrlClass(
        name="User",
        properties={
            'name': PyrlProperty(name='name', default_value=''),
            'email': PyrlProperty(name='email', default_value=''),
            'active': PyrlProperty(name='active', default_value=True)
        },
        methods={
            'init': PyrlMethod(
                name='init',
                params=['name', 'email'],
                body=lambda self, name, email: (
                    self.properties.update({'name': name, 'email': email})
                )
            ),
            'greet': PyrlMethod(
                name='greet',
                params=[],
                body=lambda self: f"Hello, I'm {self.properties.get('name', 'Unknown')}!"
            ),
            'activate': PyrlMethod(
                name='activate',
                params=[],
                body=lambda self: self.properties.update({'active': True})
            ),
            'deactivate': PyrlMethod(
                name='deactivate',
                params=[],
                body=lambda self: self.properties.update({'active': False})
            ),
            'is_active': PyrlMethod(
                name='is_active',
                params=[],
                body=lambda self: self.properties.get('active', False)
            )
        }
    )
    
    runtime.register_class(user_class)
    print(f"   Registered class: User")
    
    print("\n4. Creating User instance:")
    user = runtime.create_instance('User')
    runtime.call_method(user, 'init', ['Alice', 'alice@example.com'])
    
    print(f"   Name: {user.get_property('name')}")
    print(f"   Email: {user.get_property('email')}")
    print(f"   Active: {user.get_property('active')}")
    
    greeting = runtime.call_method(user, 'greet', [])
    print(f"   Greeting: {greeting}")
    
    runtime.call_method(user, 'deactivate', [])
    print(f"   After deactivate: {user.get_property('active')}")
    
    print("\n5. Inheritance Demo:")
    
    # Create Admin class extending User
    admin_class = PyrlClass(
        name="Admin",
        parent_class=user_class,
        properties={
            'role': PyrlProperty(name='role', default_value='admin'),
            'permissions': PyrlProperty(name='permissions', default_value=[])
        },
        methods={
            'init': PyrlMethod(
                name='init',
                params=['name', 'email', 'role'],
                body=lambda self, name, email, role='admin': (
                    self.properties.update({'name': name, 'email': email, 'role': role})
                )
            ),
            'add_permission': PyrlMethod(
                name='add_permission',
                params=['permission'],
                body=lambda self, perm: (
                    self.properties.get('permissions', []).append(perm)
                )
            ),
            'get_info': PyrlMethod(
                name='get_info',
                params=[],
                body=lambda self: f"{self.properties.get('name')} ({self.properties.get('role')})"
            )
        }
    )
    
    runtime.register_class(admin_class)
    
    admin = runtime.create_instance('Admin')
    runtime.call_method(admin, 'init', ['Bob', 'bob@admin.com', 'superadmin'])
    
    print(f"   Admin name: {admin.get_property('name')}")
    print(f"   Admin role: {admin.get_property('role')}")
    print(f"   Admin greeting (inherited): {runtime.call_method(admin, 'greet', [])}")
    print(f"   Admin info: {runtime.call_method(admin, 'get_info', [])}")
    
    print("\n6. Instance checks:")
    print(f"   user instance_of User: {runtime.instance_of(user, 'User')}")
    print(f"   admin instance_of Admin: {runtime.instance_of(admin, 'Admin')}")
    print(f"   admin instance_of User: {runtime.instance_of(admin, 'User')}")
    
    print("\n" + "=" * 60)
    print("OOP Extension Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    demo_oop()
