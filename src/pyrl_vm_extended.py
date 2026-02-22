# FILE: pyrl_vm_extended.py
"""
Pyrl Virtual Machine with OOP Extension
Extended version supporting classes, inheritance, and objects

Version: 3.0.0 - OOP Edition
Author: Pyrl AI Assistant
"""

import re
import sys
import json
from typing import Dict, List, Any, Union, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from lark import Lark, Transformer, Token, Tree
from lark.exceptions import UnexpectedCharacters, UnexpectedToken

# Import base components
from pyrl_vm import (
    PyrlSyntaxError, PyrlRuntimeError, PyrlTypeError, ReturnException,
    ASTNode, AssignmentNode, BinaryOpNode, UnaryOpNode, VariableNode,
    LiteralNode, HashLiteralNode, ArrayLiteralNode, HashAccessNode,
    ArrayAccessNode, ConditionalNode, LoopNode, FunctionDefNode,
    FunctionCallNode, PrintNode, ReturnNode, AssertionNode, TestBlockNode,
    VueGenNode, BlockNode, ProgramNode, TestResult, PyrlInterpreter, PyrlVM
)
from pyrl_oop_plugin import (
    PyrlClass, PyrlInstance, PyrlMethod, PyrlProperty, OOPRuntime,
    create_builtin_classes
)


# ============================================================================
# NEW AST NODES FOR OOP
# ============================================================================

@dataclass
class ClassDefNode(ASTNode):
    """AST node for class definition"""
    name: str
    parent: Optional[str] = None
    methods: Dict[str, 'FunctionDefNode'] = field(default_factory=dict)
    properties: Dict[str, ASTNode] = field(default_factory=dict)


@dataclass
class InstanceCreationNode(ASTNode):
    """AST node for creating class instance"""
    class_name: str
    args: List[ASTNode] = field(default_factory=list)


@dataclass
class MethodCallNode(ASTNode):
    """AST node for method call on instance"""
    instance: ASTNode
    method_name: str
    args: List[ASTNode] = field(default_factory=list)


@dataclass
class PropertyAccessNode(ASTNode):
    """AST node for accessing instance property"""
    instance: ASTNode
    property_name: str


@dataclass
class PropertySetNode(ASTNode):
    """AST node for setting instance property"""
    instance: ASTNode
    property_name: str
    value: ASTNode


# ============================================================================
# EXTENDED GRAMMAR
# ============================================================================

EXTENDED_GRAMMAR = r"""
start: statement*

statement: assignment 
         | function_definition
         | conditional 
         | loop 
         | block 
         | test_block 
         | expression_statement
         | vue_component_gen
         | print_statement
         | return_statement
         | assertion_statement
         | class_definition
         | property_assignment
         
# OOP Extensions
class_definition: "class" IDENT ["extends" IDENT] class_body
class_body: "{" class_member* "}"
class_member: method_def | property_def
method_def: "method" IDENT "(" [param_list] ")" "=" block
          | "init" "(" [param_list] ")" "=" block
property_def: "prop" IDENT ["=" expression]

property_assignment: primary_expr "." IDENT "=" expression

assertion_statement: "assert" expression comparison_op expression
                   | "assert" expression

comparison_op: "==" | "!=" | "<" | ">" | "<=" | ">="
         
expression_statement: expression
             
function_definition: FUNC_VAR "(" [param_list] ")" "=" block

param_list: SCALAR_VAR ("," SCALAR_VAR)*

assignment: (SCALAR_VAR | ARRAY_VAR | HASH_VAR | hash_access | array_access) "=" expression

?expression: or_expr

?or_expr: and_expr (OR_OP and_expr)*

?and_expr: comparison_expr (AND_OP comparison_expr)*

?comparison_expr: additive_expr (COMP_OP additive_expr)*

additive_expr: multiplicative_expr (ADD_OP multiplicative_expr)*

multiplicative_expr: unary_expr (MUL_OP unary_expr)*

?unary_expr: NOT_OP unary_expr
           | MINUS_OP unary_expr
           | primary_expr

?primary_expr: literal 
             | VARIABLE 
             | hash_access
             | array_access
             | "(" expression ")"
             | regex_literal
             | function_call
             | instance_creation
             | method_call
             | property_access
             
instance_creation: IDENT "(" [arg_list] ")"
method_call: primary_expr "." IDENT "(" [arg_list] ")"
property_access: primary_expr "." IDENT

hash_access: HASH_VAR "[" expression "]" | SCALAR_VAR "[" expression "]"

array_access: ARRAY_VAR "[" expression "]"

literal: STRING | NUMBER | BOOLEAN | NONE | hash_literal | array_literal

hash_literal: "{" [hash_item ("," hash_item)*] [","] "}"
hash_item: (STRING | IDENT) ":" expression

array_literal: "[" [expression ("," expression)*] [","] "]"

regex_literal: "r" STRING

conditional: "if" expression block 
           | "if" expression block "else" block

loop: "for" SCALAR_VAR "in" expression block
    | "while" expression block

block: "{" statement* "}"

test_block: "test" STRING? block

print_statement: "print" "(" expression ")"

vue_component_gen: "vue" STRING "{" vue_prop_list? "}"
vue_prop_list: vue_property ("," vue_property)*
vue_property: IDENT ":" expression
     
function_call: FUNC_VAR "(" [arg_list] ")"

arg_list: expression ("," expression)*

return_statement: "return" expression?

VARIABLE: SCALAR_VAR | ARRAY_VAR | HASH_VAR | FUNC_VAR
SCALAR_VAR: "$" IDENT
ARRAY_VAR: "@" IDENT
HASH_VAR: "%" IDENT
FUNC_VAR: "&" IDENT

IDENT: /[a-zA-Z_][a-zA-Z0-9_]*/

STRING: ESCAPED_STRING
       | SINGLE_QUOTED_STRING

SINGLE_QUOTED_STRING: /'[^']*'/

NUMBER: SIGNED_INT | SIGNED_FLOAT
BOOLEAN: "true" | "false"
NONE: "none" | "null"

OR_OP: "||"
AND_OP: "&&"
COMP_OP: "==" | "!=" | "<" | ">" | "<=" | ">=" | "=~" | "!~"
ADD_OP: "+" | "-"
MUL_OP: "*" | "/" | "%"
NOT_OP: "!"
MINUS_OP: "-"

%import common.ESCAPED_STRING
%import common.SIGNED_INT
%import common.SIGNED_FLOAT
%import common.WS

%ignore WS
"""


# ============================================================================
# EXTENDED AST BUILDER
# ============================================================================

class ExtendedASTBuilder(Transformer):
    """Extended AST builder with OOP support"""
    
    def __init__(self, base_builder):
        self.base = base_builder
    
    # Delegate to base methods
    def __getattr__(self, name):
        return getattr(self.base, name)
    
    # OOP-specific methods
    def class_definition(self, items):
        class_name = str(items[0])
        parent_name = None
        methods = {}
        properties = {}
        
        for item in items[1:]:
            if isinstance(item, str) and item not in ['class', 'extends']:
                parent_name = item
            elif isinstance(item, dict):
                if 'methods' in item:
                    methods.update(item['methods'])
                if 'properties' in item:
                    properties.update(item['properties'])
            elif isinstance(item, list):
                for member in item:
                    if isinstance(member, dict):
                        if 'method' in member:
                            methods[member['method'].name] = member['method']
                        if 'property' in member:
                            properties[member['property'][0]] = member['property'][1]
        
        return ClassDefNode(
            name=class_name,
            parent=parent_name,
            methods=methods,
            properties=properties
        )
    
    def class_body(self, items):
        return list(items)
    
    def class_member(self, items):
        return items[0] if items else None
    
    def method_def(self, items):
        # items: [name/INIT, params?, body]
        if items[0] == 'init':
            method_name = 'init'
            params = items[1] if len(items) > 2 and isinstance(items[1], list) else []
            body = items[-1] if isinstance(items[-1], list) else []
        else:
            method_name = str(items[0])
            params = items[1] if len(items) > 2 and isinstance(items[1], list) else []
            body = items[-1] if isinstance(items[-1], list) else []
        
        return {
            'method': FunctionDefNode(
                name=method_name,
                params=params,
                body=body
            )
        }
    
    def property_def(self, items):
        prop_name = str(items[0])
        default_value = items[1] if len(items) > 1 else LiteralNode(value=None)
        return {'property': (prop_name, default_value)}
    
    def instance_creation(self, items):
        class_name = str(items[0])
        args = items[1] if len(items) > 1 and isinstance(items[1], list) else []
        return InstanceCreationNode(class_name=class_name, args=args)
    
    def method_call(self, items):
        instance = items[0]
        method_name = str(items[1])
        args = items[2] if len(items) > 2 and isinstance(items[2], list) else []
        return MethodCallNode(instance=instance, method_name=method_name, args=args)
    
    def property_access(self, items):
        instance = items[0]
        prop_name = str(items[1])
        return PropertyAccessNode(instance=instance, property_name=prop_name)
    
    def property_assignment(self, items):
        instance = items[0]
        prop_name = str(items[1])
        value = items[2]
        return PropertySetNode(instance=instance, property_name=prop_name, value=value)


# ============================================================================
# EXTENDED INTERPRETER
# ============================================================================

class ExtendedInterpreter(PyrlInterpreter):
    """Extended interpreter with OOP support"""
    
    def __init__(self, vm):
        super().__init__(vm)
        self.oop_runtime = OOPRuntime(vm)
        
        # Register built-in classes
        for name, class_def in create_builtin_classes().items():
            self.oop_runtime.register_class(class_def)
    
    def execute_ClassDefNode(self, node: ClassDefNode) -> Any:
        """Execute class definition"""
        parent_class = None
        if node.parent:
            parent_class = self.oop_runtime.get_class(node.parent)
        
        # Create PyrlClass
        methods = {}
        for method_name, method_node in node.methods.items():
            methods[method_name] = PyrlMethod(
                name=method_name,
                params=method_node.params,
                body=method_node
            )
        
        properties = {}
        for prop_name, value_node in node.properties.items():
            default_value = self.execute(value_node)
            properties[prop_name] = PyrlProperty(
                name=prop_name,
                default_value=default_value
            )
        
        class_def = PyrlClass(
            name=node.name,
            parent_class=parent_class,
            methods=methods,
            properties=properties
        )
        
        self.oop_runtime.register_class(class_def)
        return f"Defined class {node.name}"
    
    def execute_InstanceCreationNode(self, node: InstanceCreationNode) -> Any:
        """Create instance of a class"""
        args = [self.execute(arg) for arg in node.args]
        instance = self.oop_runtime.create_instance(node.class_name, args)
        
        # Call init if exists
        init_method = instance.get_method('init')
        if init_method:
            self._execute_method(instance, 'init', args)
        
        return instance
    
    def execute_MethodCallNode(self, node: MethodCallNode) -> Any:
        """Execute method call on instance"""
        # Special handling for @self
        if isinstance(node.instance, VariableNode) and node.instance.name == '@self':
            instance = self.vm.get_variable('@self')
        else:
            instance = self.execute(node.instance)
        
        if not isinstance(instance, PyrlInstance):
            raise PyrlRuntimeError(f"Cannot call method on non-instance")
        
        args = [self.execute(arg) for arg in node.args]
        return self._execute_method(instance, node.method_name, args)
    
    def execute_PropertyAccessNode(self, node: PropertyAccessNode) -> Any:
        """Access property on instance"""
        # Special handling for @self
        if isinstance(node.instance, VariableNode) and node.instance.name == '@self':
            instance = self.vm.get_variable('@self')
        else:
            instance = self.execute(node.instance)
        
        if isinstance(instance, PyrlInstance):
            return instance.get_property(node.property_name)
        
        # Try dict access for hashes
        if isinstance(instance, dict):
            return instance.get(node.property_name)
        
        # List access - check if instance is stored as special @self variable
        if isinstance(instance, list):
            # This shouldn't happen for proper @self handling
            return None
        
        raise PyrlRuntimeError(f"Cannot access property on {type(instance).__name__}")
    
    def execute_PropertySetNode(self, node: PropertySetNode) -> Any:
        """Set property on instance"""
        # Special handling for @self
        if isinstance(node.instance, VariableNode) and node.instance.name == '@self':
            instance = self.vm.get_variable('@self')
        else:
            instance = self.execute(node.instance)
        value = self.execute(node.value)
        
        if isinstance(instance, PyrlInstance):
            instance.set_property(node.property_name, value)
            return value
        
        if isinstance(instance, dict):
            instance[node.property_name] = value
            return value
        
        raise PyrlRuntimeError(f"Cannot set property on {type(instance).__name__}")
    
    def _execute_method(self, instance: PyrlInstance, method_name: str, args: List[Any]) -> Any:
        """Execute a method on an instance"""
        method = instance.get_method(method_name)
        if not method:
            raise PyrlRuntimeError(f"Method '{method_name}' not found")
        
        # If method body is a FunctionDefNode, execute it
        if hasattr(method.body, 'body'):
            # Save current variables
            original_values = {}
            for i, param_name in enumerate(method.params):
                original_values[param_name] = self.vm.get_variable(param_name)
                if i < len(args):
                    self.vm.set_variable(param_name, args[i])
            
            # Set @self variable
            self.vm.set_variable('@self', instance)
            
            try:
                result = None
                for stmt in method.body.body:
                    result = self.execute(stmt)
                return result
            except ReturnException as e:
                return e.value
            finally:
                # Restore variables
                for param_name in method.params:
                    if original_values[param_name] is not None:
                        self.vm.set_variable(param_name, original_values[param_name])
        
        # If method body is callable, call it
        elif callable(method.body):
            return method.body(instance, *args)
        
        return None


# ============================================================================
# EXTENDED VM
# ============================================================================

class ExtendedPyrlVM(PyrlVM):
    """Extended Pyrl VM with OOP support"""
    
    def __init__(self):
        # Don't call super().__init__() to avoid re-registering builtins
        self.memory = {
            'scalars': {},
            'arrays': {},
            'hashes': {},
            'functions': {}
        }
        
        # Use extended grammar
        self.parser = Lark(EXTENDED_GRAMMAR, parser='earley', propagate_positions=True)
        
        # Create base AST builder
        from pyrl_vm import ASTBuilder
        self.base_ast_builder = ASTBuilder()
        self.ast_builder = ExtendedASTBuilder(self.base_ast_builder)
        
        # Use extended interpreter
        self.interpreter = ExtendedInterpreter(self)
        self.test_results: List[TestResult] = []
        self.current_test_name = ""
        
        # OOP runtime reference
        self.oop_runtime = self.interpreter.oop_runtime
        
        self._register_builtins()
    
    def _preprocess(self, code: str) -> str:
        """Remove comments from code"""
        lines = code.split('\n')
        result = []
        for line in lines:
            in_string = False
            string_char = None
            escaped = False
            clean_line = []
            
            for i, char in enumerate(line):
                if escaped:
                    clean_line.append(char)
                    escaped = False
                    continue
                    
                if char == '\\' and in_string:
                    clean_line.append(char)
                    escaped = True
                    continue
                    
                if char in ('"', "'") and not in_string:
                    in_string = True
                    string_char = char
                    clean_line.append(char)
                elif char == string_char and in_string:
                    in_string = False
                    string_char = None
                    clean_line.append(char)
                elif char == '#' and not in_string:
                    break
                else:
                    clean_line.append(char)
            
            result.append(''.join(clean_line))
        
        return '\n'.join(result)
    
    def execute(self, code: str) -> Any:
        """Execute Pyrl code with OOP support"""
        try:
            clean_code = self._preprocess(code)
            tree = self.parser.parse(clean_code)
            ast = self.ast_builder.transform(tree)
            result = self.interpreter.execute(ast)
            return result
        except PyrlSyntaxError:
            raise
        except PyrlRuntimeError:
            raise
        except Exception as e:
            raise PyrlRuntimeError(str(e))
    
    def get_variable(self, var_name: str) -> Any:
        """Get variable - with special handling for @self"""
        if var_name == '@self':
            # Return the current instance context
            return self.memory.get('__instance__', None)
        return super().get_variable(var_name)
    
    def set_variable(self, var_name: str, value: Any) -> None:
        """Set variable - with special handling for @self"""
        if var_name == '@self':
            # Store instance in special location
            self.memory['__instance__'] = value
            return
        super().set_variable(var_name, value)
    
    def get_class(self, name: str) -> Optional[PyrlClass]:
        """Get a class definition"""
        return self.oop_runtime.get_class(name)
    
    def create_instance(self, class_name: str, args: List[Any] = None) -> PyrlInstance:
        """Create an instance of a class"""
        return self.oop_runtime.create_instance(class_name, args)


# ============================================================================
# OOP SYNTAX DEMO
# ============================================================================

def demo_oop_syntax():
    """Demonstrate OOP syntax in Pyrl"""
    print("=" * 70)
    print("PYRL OOP EXTENSION - LIVE DEMONSTRATION")
    print("=" * 70)
    
    vm = ExtendedPyrlVM()
    
    # Example 1: Simple Counter Class
    print("\n" + "-" * 70)
    print("1. DEFINING A SIMPLE CLASS: Counter")
    print("-" * 70)
    
    counter_code = '''
class Counter {
    prop count = 0
    
    init($start) = {
        @self.count = $start
    }
    
    method increment($amount) = {
        @self.count = @self.count + $amount
        return @self.count
    }
    
    method decrement($amount) = {
        @self.count = @self.count - $amount
        return @self.count
    }
    
    method get() = {
        return @self.count
    }
    
    method reset() = {
        @self.count = 0
        return @self.count
    }
}
'''
    
    print("Code:")
    print(counter_code)
    
    result = vm.execute(counter_code)
    print(f"Result: {result}")
    
    # Example 2: Creating instances
    print("\n" + "-" * 70)
    print("2. CREATING INSTANCES AND CALLING METHODS")
    print("-" * 70)
    
    instance_code = '''
$counter = Counter(10)
print($counter.get())
$result1 = $counter.increment(5)
print($result1)
$result2 = $counter.decrement(3)
print($result2)
'''
    
    print("Code:")
    print(instance_code)
    print("\nExecution:")
    result = vm.execute(instance_code)
    
    # Example 3: Inheritance
    print("\n" + "-" * 70)
    print("3. CLASS INHERITANCE: User -> Admin")
    print("-" * 70)
    
    inheritance_code = '''
class User {
    prop name = ""
    prop email = ""
    
    init($name, $email) = {
        @self.name = $name
        @self.email = $email
    }
    
    method greet() = {
        return "Hello, I'm " + @self.name
    }
    
    method get_email() = {
        return @self.email
    }
}

class Admin extends User {
    prop role = "admin"
    prop permissions = []
    
    init($name, $email, $role) = {
        @self.name = $name
        @self.email = $email
        @self.role = $role
    }
    
    method get_info() = {
        return @self.name + " (" + @self.role + ")"
    }
    
    method add_permission($perm) = {
        &push(@self.permissions, $perm)
        return @self.permissions
    }
}
'''
    
    print("Code:")
    print(inheritance_code)
    
    result = vm.execute(inheritance_code)
    print(f"Result: {result}")
    
    # Example 4: Using inherited methods
    print("\n" + "-" * 70)
    print("4. USING INHERITED METHODS")
    print("-" * 70)
    
    admin_code = '''
$admin = Admin("Alice", "alice@admin.com", "superadmin")
print($admin.greet())
print($admin.get_info())
$perms = $admin.add_permission("delete_users")
print($perms)
'''
    
    print("Code:")
    print(admin_code)
    print("\nExecution:")
    result = vm.execute(admin_code)
    
    # Example 5: Testing OOP
    print("\n" + "-" * 70)
    print("5. TESTING OOP FEATURES")
    print("-" * 70)
    
    test_code = '''
test "Counter Class Tests" {
    $c = Counter(0)
    assert $c.get() == 0
    
    $c.increment(10)
    assert $c.get() == 10
    
    $c.decrement(5)
    assert $c.get() == 5
}

test "User Class Tests" {
    $user = User("Bob", "bob@example.com")
    assert $user.greet() == "Hello, I'm Bob"
    assert $user.get_email() == "bob@example.com"
}
'''
    
    print("Code:")
    print(test_code)
    print("\nExecution:")
    results = vm.run_tests(test_code)
    
    summary = vm.get_test_summary()
    print(f"\nTest Summary: {summary['passed']}/{summary['total']} passed")
    
    print("\n" + "=" * 70)
    print("OOP EXTENSION DEMO COMPLETE!")
    print("=" * 70)
    
    return vm


if __name__ == "__main__":
    vm = demo_oop_syntax()
