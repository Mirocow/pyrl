# FILE: pyrl_vm.py
"""
Pyrl Virtual Machine Implementation
A hybrid Python-Perl inspired language interpreter

Version: 2.0.0
Author: Pyrl Ecosystem Team

Features:
- Sigil-based variables ($scalar, @array, %hash, &function)
- Regex operators (=~, !~)
- Vue.js 3 component generation
- Built-in test framework
- HTTP API server
"""

import re
import sys
import json
import warnings
from typing import Dict, List, Any, Union, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from lark import Lark, Transformer, Visitor, Token, Tree
from lark.exceptions import UnexpectedCharacters, UnexpectedToken

# Suppress escape sequence warnings for regex patterns
warnings.filterwarnings('ignore', category=DeprecationWarning, 
                       message='.*invalid escape sequence.*')
warnings.filterwarnings('ignore', category=SyntaxWarning,
                       message='.*invalid escape sequence.*')


# ============================================================================
# EXCEPTIONS
# ============================================================================

class PyrlSyntaxError(Exception):
    """Raised when there's a syntax error in Pyrl code"""
    def __init__(self, message: str, line: int = None, column: int = None):
        self.line = line
        self.column = column
        super().__init__(f"Syntax Error at line {line}, column {column}: {message}" if line else message)


class PyrlRuntimeError(Exception):
    """Raised when there's a runtime error during execution"""
    def __init__(self, message: str, line: int = None):
        self.line = line
        super().__init__(f"Runtime Error at line {line}: {message}" if line else message)


class PyrlTypeError(Exception):
    """Raised when there's a type mismatch"""
    def __init__(self, expected: str, got: str, variable: str = None):
        self.expected = expected
        self.got = got
        self.variable = variable
        msg = f"Type Error: expected {expected}, got {got}"
        if variable:
            msg = f"Type Error for '{variable}': expected {expected}, got {got}"
        super().__init__(msg)


class ReturnException(Exception):
    """Used to implement return statements in functions"""
    def __init__(self, value):
        self.value = value


# ============================================================================
# AST NODES
# ============================================================================

@dataclass
class ASTNode:
    """Base class for AST nodes"""
    pass


@dataclass
class AssignmentNode(ASTNode):
    target: str  # Variable name or special marker for hash/array access
    value: ASTNode
    target_type: str = "scalar"  # scalar, hash_access, array_access
    key: ASTNode = None  # For hash/array access


@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    op: str
    right: ASTNode


@dataclass
class UnaryOpNode(ASTNode):
    op: str
    operand: ASTNode


@dataclass
class VariableNode(ASTNode):
    name: str


@dataclass
class LiteralNode(ASTNode):
    value: Any


@dataclass
class HashLiteralNode(ASTNode):
    items: List[tuple]  # List of (key, value) pairs


@dataclass
class ArrayLiteralNode(ASTNode):
    items: List[ASTNode]


@dataclass
class HashAccessNode(ASTNode):
    var_name: str
    key: ASTNode


@dataclass
class ArrayAccessNode(ASTNode):
    var_name: str
    index: ASTNode


@dataclass
class ConditionalNode(ASTNode):
    condition: ASTNode
    if_block: List[ASTNode]
    else_block: Optional[List[ASTNode]] = None


@dataclass
class LoopNode(ASTNode):
    loop_type: str  # "for" or "while"
    var_name: Optional[str] = None  # For for-loops
    iterable: Optional[ASTNode] = None  # For for-loops
    condition: Optional[ASTNode] = None  # For while-loops
    body: List[ASTNode] = None


@dataclass
class FunctionDefNode(ASTNode):
    name: str
    params: List[str]
    body: List[ASTNode]


@dataclass
class FunctionCallNode(ASTNode):
    name: str
    args: List[ASTNode]


@dataclass
class PrintNode(ASTNode):
    value: ASTNode


@dataclass
class ReturnNode(ASTNode):
    value: Optional[ASTNode] = None


@dataclass
class AssertionNode(ASTNode):
    left: ASTNode
    op: Optional[str] = None
    right: Optional[ASTNode] = None


@dataclass
class TestBlockNode(ASTNode):
    name: str
    statements: List[ASTNode]


@dataclass
class VueGenNode(ASTNode):
    name: str
    props: Dict[str, ASTNode]


@dataclass
class BlockNode(ASTNode):
    statements: List[ASTNode]


@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode]


# ============================================================================
# TEST RESULT
# ============================================================================

@dataclass
class TestResult:
    """Represents the result of a single test assertion"""
    name: str = ""
    success: bool = False
    message: str = ""
    line: int = 0
    expected: Any = None
    actual: Any = None
    test_type: str = "equality"


# ============================================================================
# PARSER
# ============================================================================

class PyrlParser:
    """Parser for Pyrl language using Lark parser generator"""
    
    GRAMMAR = r"""
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
    
    def __init__(self):
        self.parser = Lark(self.GRAMMAR, parser='earley', propagate_positions=True)
    
    def _preprocess(self, code: str) -> str:
        """Remove comments from code before parsing"""
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
    
    def parse(self, code: str) -> Tree:
        """Parse Pyrl code and return AST"""
        try:
            clean_code = self._preprocess(code)
            return self.parser.parse(clean_code)
        except UnexpectedCharacters as e:
            raise PyrlSyntaxError(
                f"Unexpected character: {e.char!r}",
                line=e.line,
                column=e.column
            )
        except UnexpectedToken as e:
            raise PyrlSyntaxError(
                f"Unexpected token: {e.token!r}, expected one of: {e.expected}",
                line=e.line,
                column=e.column
            )
        except Exception as e:
            # Catch UnexpectedEOF and other parsing errors
            raise PyrlSyntaxError(str(e))


# ============================================================================
# AST BUILDER
# ============================================================================

class ASTBuilder(Transformer):
    """Transforms Lark parse tree into AST nodes"""
    
    def start(self, items):
        return ProgramNode(statements=[i for i in items if i is not None])
    
    def statement(self, items):
        return items[0] if items else None
    
    def assignment(self, items):
        target = items[0]
        value = items[1]
        
        if isinstance(target, (HashAccessNode, ArrayAccessNode)):
            if isinstance(target, HashAccessNode):
                return AssignmentNode(
                    target=target.var_name,
                    value=value,
                    target_type="hash_access",
                    key=target.key
                )
            else:
                return AssignmentNode(
                    target=target.var_name,
                    value=value,
                    target_type="array_access",
                    key=target.index
                )
        else:
            return AssignmentNode(target=str(target), value=value)
    
    def expression(self, items):
        if len(items) == 1:
            return items[0]
        return items
    
    def or_expr(self, items):
        if len(items) == 1:
            return items[0]
        result = items[0]
        for i in range(1, len(items), 2):
            result = BinaryOpNode(left=result, op=items[i], right=items[i+1])
        return result
    
    def and_expr(self, items):
        if len(items) == 1:
            return items[0]
        result = items[0]
        for i in range(1, len(items), 2):
            result = BinaryOpNode(left=result, op=items[i], right=items[i+1])
        return result
    
    def comparison_expr(self, items):
        if len(items) == 1:
            return items[0]
        result = items[0]
        for i in range(1, len(items), 2):
            result = BinaryOpNode(left=result, op=items[i], right=items[i+1])
        return result
    
    def additive_expr(self, items):
        if len(items) == 1:
            return items[0]
        result = items[0]
        for i in range(1, len(items), 2):
            result = BinaryOpNode(left=result, op=items[i], right=items[i+1])
        return result
    
    def multiplicative_expr(self, items):
        if len(items) == 1:
            return items[0]
        result = items[0]
        for i in range(1, len(items), 2):
            result = BinaryOpNode(left=result, op=items[i], right=items[i+1])
        return result
    
    def unary_expr(self, items):
        if len(items) == 1:
            return items[0]
        return UnaryOpNode(op=items[0], operand=items[1])
    
    def primary_expr(self, items):
        return items[0]
    
    def literal(self, items):
        # Don't wrap already-processed nodes
        if items and isinstance(items[0], (HashLiteralNode, ArrayLiteralNode)):
            return items[0]
        return LiteralNode(value=items[0])
    
    def STRING(self, token):
        s = str(token)
        if s.startswith('"') and s.endswith('"'):
            # Use codecs.decode for proper unicode handling
            import codecs
            try:
                return codecs.decode(s[1:-1], 'unicode_escape')
            except (UnicodeDecodeError, UnicodeEncodeError):
                # Fallback for strings with invalid escape sequences
                return s[1:-1]
        elif s.startswith("'") and s.endswith("'"):
            return s[1:-1]
        return s
    
    def NUMBER(self, token):
        s = str(token)
        if '.' in s or 'e' in s.lower():
            return float(s)
        return int(s)
    
    def BOOLEAN(self, token):
        return str(token) == 'true'
    
    def NONE(self, token):
        return None
    
    def IDENT(self, token):
        return str(token)
    
    def VARIABLE(self, token):
        return VariableNode(name=str(token))
    
    def SCALAR_VAR(self, token):
        return str(token)
    
    def ARRAY_VAR(self, token):
        return str(token)
    
    def HASH_VAR(self, token):
        return str(token)
    
    def FUNC_VAR(self, token):
        return str(token)
    
    def OR_OP(self, token):
        return str(token)
    
    def AND_OP(self, token):
        return str(token)
    
    def COMP_OP(self, token):
        return str(token)
    
    def ADD_OP(self, token):
        return str(token)
    
    def MUL_OP(self, token):
        return str(token)
    
    def NOT_OP(self, token):
        return str(token)
    
    def MINUS_OP(self, token):
        return str(token)
    
    def hash_literal(self, items):
        result = []
        for item in items:
            if isinstance(item, tuple) and len(item) == 2:
                result.append(item)
        return HashLiteralNode(items=result)
    
    def hash_item(self, items):
        key = items[0]
        if isinstance(key, str) and key.startswith('"'):
            key = key[1:-1]
        value = items[1]
        return (key, value)
    
    def array_literal(self, items):
        return ArrayLiteralNode(items=items)
    
    def regex_literal(self, items):
        if len(items) >= 1:
            return LiteralNode(value=str(items[0]))
        return LiteralNode(value="")
    
    def hash_access(self, items):
        return HashAccessNode(var_name=str(items[0]), key=items[1])
    
    def array_access(self, items):
        return ArrayAccessNode(var_name=str(items[0]), index=items[1])
    
    def conditional(self, items):
        condition = items[0]
        if_block = items[1]
        else_block = items[2] if len(items) > 2 else None
        return ConditionalNode(condition=condition, if_block=if_block, else_block=else_block)
    
    def loop(self, items):
        if len(items) >= 3:
            var_name = str(items[0])
            iterable = items[1]
            body = items[2]
            return LoopNode(loop_type="for", var_name=var_name, iterable=iterable, body=body)
        elif len(items) == 2:
            condition = items[0]
            body = items[1]
            return LoopNode(loop_type="while", condition=condition, body=body)
    
    def block(self, items):
        return [i for i in items if i is not None]
    
    def test_block(self, items):
        test_name = ""
        statements = []
        for item in items:
            if isinstance(item, str) and not statements:
                test_name = item
            elif isinstance(item, list):
                statements = item
        return TestBlockNode(name=test_name, statements=statements)
    
    def assertion_statement(self, items):
        if len(items) == 1:
            return AssertionNode(left=items[0])
        elif len(items) == 3:
            return AssertionNode(left=items[0], op=items[1], right=items[2])
    
    def comparison_op(self, items):
        return str(items[0]) if items else '=='
    
    def print_statement(self, items):
        return PrintNode(value=items[0])
    
    def vue_component_gen(self, items):
        component_name = str(items[0])
        if component_name.startswith('"') and component_name.endswith('"'):
            component_name = component_name[1:-1]
        
        properties = {}
        if len(items) > 1:
            prop_items = items[1] if isinstance(items[1], list) else []
            for prop_item in prop_items:
                if isinstance(prop_item, tuple) and len(prop_item) == 2:
                    prop_name, prop_value = prop_item
                    properties[prop_name] = prop_value
        
        return VueGenNode(name=component_name, props=properties)
    
    def vue_prop_list(self, items):
        return items
    
    def vue_property(self, items):
        if len(items) >= 2:
            prop_name = str(items[0])
            prop_value = items[1]
            return (prop_name, prop_value)
        return None
    
    def function_definition(self, items):
        func_name = str(items[0])
        params = []
        body_idx = 1
        
        if len(items) > 1 and isinstance(items[1], list):
            params = items[1]
            body_idx = 2
        elif len(items) > 2:
            body_idx = 2
        
        body = items[body_idx] if body_idx < len(items) else []
        return FunctionDefNode(name=func_name, params=params, body=body)
    
    def param_list(self, items):
        return [str(item) for item in items]
    
    def function_call(self, items):
        func_name = str(items[0])
        args = []
        if len(items) > 1:
            arg_items = items[1] if isinstance(items[1], list) else items[1:]
            args = arg_items
        return FunctionCallNode(name=func_name, args=args)
    
    def arg_list(self, items):
        return items
    
    def return_statement(self, items):
        return ReturnNode(value=items[0] if items else None)


# ============================================================================
# INTERPRETER
# ============================================================================

class PyrlInterpreter:
    """Executes AST nodes"""
    
    def __init__(self, vm: 'PyrlVM'):
        self.vm = vm
        self.current_test_name = ""
    
    def execute(self, node: ASTNode) -> Any:
        """Execute an AST node and return result"""
        if node is None:
            return None
        
        method_name = f'execute_{type(node).__name__}'
        method = getattr(self, method_name, self.execute_default)
        return method(node)
    
    def execute_default(self, node: ASTNode) -> Any:
        return None
    
    def execute_ProgramNode(self, node: ProgramNode) -> Any:
        result = None
        for stmt in node.statements:
            result = self.execute(stmt)
        return result
    
    def execute_AssignmentNode(self, node: AssignmentNode) -> Any:
        value = self.execute(node.value)
        
        if node.target_type == "hash_access":
            key = self.execute(node.key)
            hash_obj = self.vm.get_variable(node.target)
            if hash_obj is None:
                hash_obj = {}
            elif not isinstance(hash_obj, dict):
                raise PyrlTypeError("hash", type(hash_obj).__name__, node.target)
            hash_obj[key] = value
            self.vm.set_variable(node.target, hash_obj)
        elif node.target_type == "array_access":
            index = int(self.execute(node.key))
            arr_obj = self.vm.get_variable(node.target)
            if arr_obj is None:
                arr_obj = []
            elif not isinstance(arr_obj, list):
                raise PyrlTypeError("array", type(arr_obj).__name__, node.target)
            while len(arr_obj) <= index:
                arr_obj.append(None)
            arr_obj[index] = value
            self.vm.set_variable(node.target, arr_obj)
        else:
            self.vm.set_variable(node.target, value)
        
        return f"Assigned {repr(value)} to {node.target}"
    
    def execute_BinaryOpNode(self, node: BinaryOpNode) -> Any:
        left = self.execute(node.left)
        right = self.execute(node.right)
        
        if node.op == '+':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            if right == 0:
                raise PyrlRuntimeError("Division by zero")
            return left / right
        elif node.op == '%':
            if right == 0:
                raise PyrlRuntimeError("Modulo by zero")
            return left % right
        elif node.op == '==':
            return left == right
        elif node.op == '!=':
            return left != right
        elif node.op == '<':
            return left < right
        elif node.op == '>':
            return left > right
        elif node.op == '<=':
            return left <= right
        elif node.op == '>=':
            return left >= right
        elif node.op == '=~':
            if isinstance(left, str) and isinstance(right, str):
                try:
                    return bool(re.search(right, left))
                except re.error:
                    raise PyrlRuntimeError(f"Invalid regex pattern: {right}")
            return False
        elif node.op == '!~':
            if isinstance(left, str) and isinstance(right, str):
                try:
                    return not bool(re.search(right, left))
                except re.error:
                    raise PyrlRuntimeError(f"Invalid regex pattern: {right}")
            return True
        elif node.op == '&&':
            return bool(left) and bool(right)
        elif node.op == '||':
            return bool(left) or bool(right)
        
        return None
    
    def execute_UnaryOpNode(self, node: UnaryOpNode) -> Any:
        operand = self.execute(node.operand)
        
        if node.op == '!':
            return not bool(operand)
        elif node.op == '-':
            return -operand
        
        return operand
    
    def execute_VariableNode(self, node: VariableNode) -> Any:
        return self.vm.get_variable(node.name)
    
    def execute_LiteralNode(self, node: LiteralNode) -> Any:
        return node.value
    
    def execute_HashLiteralNode(self, node: HashLiteralNode) -> Any:
        result = {}
        for key, value_node in node.items:
            value = self.execute(value_node)
            result[key] = value
        return result
    
    def execute_ArrayLiteralNode(self, node: ArrayLiteralNode) -> Any:
        return [self.execute(item) for item in node.items]
    
    def execute_HashAccessNode(self, node: HashAccessNode) -> Any:
        hash_obj = self.vm.get_variable(node.var_name)
        if hash_obj is None:
            return None
        if not isinstance(hash_obj, dict):
            raise PyrlTypeError("hash", type(hash_obj).__name__, node.var_name)
        key = self.execute(node.key)
        return hash_obj.get(str(key))
    
    def execute_ArrayAccessNode(self, node: ArrayAccessNode) -> Any:
        arr_obj = self.vm.get_variable(node.var_name)
        if arr_obj is None:
            return None
        if not isinstance(arr_obj, list):
            raise PyrlTypeError("array", type(arr_obj).__name__, node.var_name)
        index = int(self.execute(node.index))
        if 0 <= index < len(arr_obj):
            return arr_obj[index]
        return None
    
    def execute_ConditionalNode(self, node: ConditionalNode) -> Any:
        condition = self.execute(node.condition)
        
        if condition:
            result = None
            for stmt in node.if_block:
                result = self.execute(stmt)
            return result
        elif node.else_block:
            result = None
            for stmt in node.else_block:
                result = self.execute(stmt)
            return result
        
        return None
    
    def execute_LoopNode(self, node: LoopNode) -> Any:
        results = []
        
        if node.loop_type == "for":
            iterable = self.execute(node.iterable)
            if iterable is None:
                raise PyrlRuntimeError("Cannot iterate over None")
            if not hasattr(iterable, '__iter__'):
                raise PyrlTypeError("iterable", type(iterable).__name__)
            
            for item in iterable:
                self.vm.set_variable(node.var_name, item)
                for stmt in node.body:
                    results.append(self.execute(stmt))
        
        elif node.loop_type == "while":
            max_iterations = 10000
            iterations = 0
            
            while iterations < max_iterations:
                condition = self.execute(node.condition)
                if not condition:
                    break
                for stmt in node.body:
                    results.append(self.execute(stmt))
                iterations += 1
            
            if iterations >= max_iterations:
                raise PyrlRuntimeError("Maximum iterations exceeded")
        
        return results
    
    def execute_FunctionDefNode(self, node: FunctionDefNode) -> Any:
        def function_impl(*args):
            # Save original variable values
            original_values = {}
            for i, param_name in enumerate(node.params):
                original_values[param_name] = self.vm.get_variable(param_name)
                if i < len(args):
                    self.vm.set_variable(param_name, args[i])
            
            try:
                for stmt in node.body:
                    self.execute(stmt)
                return None
            except ReturnException as e:
                return e.value
            finally:
                # Restore original values
                for param_name in node.params:
                    if original_values[param_name] is not None:
                        self.vm.set_variable(param_name, original_values[param_name])
        
        self.vm.register_function(node.name, function_impl)
        return f"Defined function {node.name}"
    
    def execute_FunctionCallNode(self, node: FunctionCallNode) -> Any:
        args = [self.execute(arg) for arg in node.args]
        func = self.vm.get_variable(node.name)
        if func is None:
            raise PyrlRuntimeError(f"Function {node.name} not found")
        if not callable(func):
            raise PyrlTypeError("function", type(func).__name__, node.name)
        return func(*args)
    
    def execute_PrintNode(self, node: PrintNode) -> Any:
        value = self.execute(node.value)
        print(value)
        return f"Printed: {value}"
    
    def execute_ReturnNode(self, node: ReturnNode) -> Any:
        if node.value:
            value = self.execute(node.value)
            raise ReturnException(value)
        raise ReturnException(None)
    
    def execute_AssertionNode(self, node: AssertionNode) -> Any:
        left = self.execute(node.left)
        
        if node.op is None:
            success = bool(left)
            result = TestResult(
                name=self.current_test_name,
                success=success,
                message=f"Assertion {'PASSED' if success else 'FAILED'}: {left} is {'truthy' if success else 'falsy'}",
                test_type="truthiness",
                actual=left
            )
            self.vm.test_results.append(result)
            return result.message
        
        right = self.execute(node.right)
        
        if node.op == '==':
            success = left == right
        elif node.op == '!=':
            success = left != right
        elif node.op == '<':
            success = left < right
        elif node.op == '>':
            success = left > right
        elif node.op == '<=':
            success = left <= right
        elif node.op == '>=':
            success = left >= right
        else:
            success = False
        
        result = TestResult(
            name=self.current_test_name,
            success=success,
            message=f"Assertion {'PASSED' if success else 'FAILED'}: {left} {node.op} {right}",
            test_type="comparison",
            expected=right,
            actual=left
        )
        self.vm.test_results.append(result)
        return result.message
    
    def execute_TestBlockNode(self, node: TestBlockNode) -> Any:
        self.current_test_name = node.name
        self.vm.current_test_name = node.name
        
        results = []
        for stmt in node.statements:
            results.append(self.execute(stmt))
        
        return f"Test '{node.name}' completed"
    
    def execute_VueGenNode(self, node: VueGenNode) -> Any:
        props = {}
        for prop_name, prop_value_node in node.props.items():
            props[prop_name] = self.execute(prop_value_node)
        
        vue_code = generate_vue_component(node.name, props)
        return vue_code
    
    def execute_BlockNode(self, node: BlockNode) -> Any:
        result = None
        for stmt in node.statements:
            result = self.execute(stmt)
        return result


# ============================================================================
# VUE GENERATOR
# ============================================================================

def generate_vue_component(name: str, props: Dict[str, Any]) -> str:
    """Generate a Vue 3 Single File Component"""
    
    template = f"""<template>
  <div class="{name.lower()}-component">
    <h2>{{{{ title }}}}</h2>"""
    
    for prop_name, prop_value in props.items():
        if isinstance(prop_value, str):
            template += f"""
    <div class="prop">
      <label>{prop_name}:</label>
      <span>{{{{ {prop_name} }}}}</span>
    </div>"""
        elif isinstance(prop_value, (int, float)):
            template += f"""
    <div class="prop">
      <label>{prop_name}:</label>
      <span>{{{{ {prop_name} }}}}</span>
    </div>"""
        elif isinstance(prop_value, bool):
            template += f"""
    <div class="prop">
      <label>{prop_name}:</label>
      <span>{{{{ {prop_name} ? 'Yes' : 'No' }}}}</span>
    </div>"""
        elif isinstance(prop_value, list):
            template += f"""
    <div class="prop">
      <label>{prop_name}:</label>
      <ul>
        <li v-for="(item, index) in {prop_name}" :key="index">
          {{{{ item }}}}
        </li>
      </ul>
    </div>"""
        elif isinstance(prop_value, dict):
            template += f"""
    <div class="prop">
      <label>{prop_name}:</label>
      <dl>
        <template v-for="(value, key) in {prop_name}" :key="key">
          <dt>{{{{ key }}}}</dt>
          <dd>{{{{ value }}}}</dd>
        </template>
      </dl>
    </div>"""
    
    template += """
  </div>
</template>"""
    
    script = f"""
<script setup>
import {{ ref, computed }} from 'vue'

const title = ref('{name} Component')
"""
    
    for prop_name, prop_value in props.items():
        if isinstance(prop_value, str):
            script += f"const {prop_name} = ref('{prop_value}')\n"
        elif isinstance(prop_value, bool):
            script += f"const {prop_name} = ref({str(prop_value).lower()})\n"
        elif prop_value is None:
            script += f"const {prop_name} = ref(null)\n"
        else:
            script += f"const {prop_name} = ref({json.dumps(prop_value)})\n"
    
    script += """
</script>"""
    
    style = f"""
<style scoped>
.{name.lower()}-component {{
  padding: 20px;
  margin: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #fafafa;
}}

.{name.lower()}-component h2 {{
  margin-top: 0;
  color: #333;
  border-bottom: 2px solid #4a90d9;
  padding-bottom: 10px;
}}

.{name.lower()}-component .prop {{
  margin: 10px 0;
  padding: 8px;
  background-color: #fff;
  border-radius: 4px;
}}

.{name.lower()}-component label {{
  font-weight: bold;
  color: #666;
  margin-right: 10px;
}}
</style>"""
    
    return template + script + style


# ============================================================================
# VIRTUAL MACHINE
# ============================================================================

class PyrlVM:
    """Virtual machine for executing Pyrl code"""
    
    def __init__(self):
        self.memory = {
            'scalars': {},
            'arrays': {},
            'hashes': {},
            'functions': {}
        }
        self.parser = PyrlParser()
        self.ast_builder = ASTBuilder()
        self.interpreter = PyrlInterpreter(self)
        self.test_results: List[TestResult] = []
        self.current_test_name = ""
        
        self._register_builtins()
    
    def _register_builtins(self):
        """Register built-in functions"""
        self.register_function('&print', lambda x: print(x))
        self.register_function('&len', lambda x: len(x) if hasattr(x, '__len__') else 1)
        self.register_function('&str', lambda x: str(x))
        self.register_function('&int', lambda x: int(x) if x else 0)
        self.register_function('&float', lambda x: float(x) if x else 0.0)
        self.register_function('&type', lambda x: type(x).__name__)
        self.register_function('&upper', lambda x: str(x).upper())
        self.register_function('&lower', lambda x: str(x).lower())
        self.register_function('&trim', lambda x: str(x).strip())
        self.register_function('&split', lambda s, d=None: str(s).split(d))
        self.register_function('&join', lambda arr, d='': d.join(str(x) for x in arr))
        self.register_function('&keys', lambda d: list(d.keys()) if isinstance(d, dict) else [])
        self.register_function('&values', lambda d: list(d.values()) if isinstance(d, dict) else [])
        self.register_function('&push', self._builtin_push)
        self.register_function('&pop', self._builtin_pop)
        self.register_function('&range', lambda n: list(range(n)))
        self.register_function('&min', lambda arr: min(arr) if arr else None)
        self.register_function('&max', lambda arr: max(arr) if arr else None)
        self.register_function('&sum', lambda arr: sum(arr) if arr else 0)
        self.register_function('&sorted', lambda arr: sorted(arr))
        self.register_function('&reversed', lambda arr: list(reversed(arr)))
        self.register_function('&abs', lambda x: abs(x))
        self.register_function('&round', lambda x, n=0: round(x, n))
    
    def _builtin_push(self, arr, item):
        if not isinstance(arr, list):
            raise PyrlTypeError("array", type(arr).__name__)
        arr.append(item)
        return arr
    
    def _builtin_pop(self, arr):
        if not isinstance(arr, list):
            raise PyrlTypeError("array", type(arr).__name__)
        return arr.pop() if arr else None
    
    def execute(self, code: str) -> Any:
        """Execute Pyrl code and return result"""
        try:
            tree = self.parser.parse(code)
            ast = self.ast_builder.transform(tree)
            result = self.interpreter.execute(ast)
            return result
        except PyrlSyntaxError:
            raise
        except PyrlRuntimeError:
            raise
        except Exception as e:
            raise PyrlRuntimeError(str(e))
    
    def register_function(self, name: str, func: Callable) -> None:
        if not name.startswith('&'):
            raise ValueError("Function name must start with &")
        func_name = name[1:]
        self.memory['functions'][func_name] = func
    
    def get_variable(self, var_name: str) -> Any:
        if not var_name.startswith(('$', '@', '%', '&')):
            raise ValueError(f"Variable name must start with a sigil: {var_name}")
        
        sigil = var_name[0]
        name = var_name[1:]
        
        if sigil == '$':
            return self.memory['scalars'].get(name)
        elif sigil == '@':
            return self.memory['arrays'].get(name, [])
        elif sigil == '%':
            return self.memory['hashes'].get(name, {})
        elif sigil == '&':
            return self.memory['functions'].get(name)
        
        return None
    
    def set_variable(self, var_name: str, value: Any) -> None:
        if not var_name.startswith(('$', '@', '%', '&')):
            raise ValueError(f"Variable name must start with a sigil: {var_name}")
        
        sigil = var_name[0]
        name = var_name[1:]
        
        if sigil == '$':
            self.memory['scalars'][name] = value
        elif sigil == '@':
            self.memory['arrays'][name] = value if isinstance(value, list) else [value]
        elif sigil == '%':
            self.memory['hashes'][name] = value if isinstance(value, dict) else {}
        elif sigil == '&':
            self.memory['functions'][name] = value
    
    def run_tests(self, code: str) -> List[TestResult]:
        self.test_results = []
        self.execute(code)
        return self.test_results
    
    def get_test_summary(self) -> Dict[str, Any]:
        passed = sum(1 for r in self.test_results if r.success)
        failed = len(self.test_results) - passed
        return {
            'total': len(self.test_results),
            'passed': passed,
            'failed': failed,
            'success_rate': passed / len(self.test_results) * 100 if self.test_results else 0
        }
    
    def reset(self) -> None:
        self.memory = {
            'scalars': {},
            'arrays': {},
            'hashes': {},
            'functions': {}
        }
        self.test_results = []
        self._register_builtins()


# ============================================================================
# HTTP SERVER
# ============================================================================

class PyrlHTTPServer:
    """HTTP server for Pyrl ecosystem using FastAPI"""
    
    def __init__(self, vm: PyrlVM = None):
        self.vm = vm or PyrlVM()
        
        try:
            from fastapi import FastAPI, HTTPException
            from fastapi.middleware.cors import CORSMiddleware
            import uvicorn
            
            self.FastAPI = FastAPI
            self.HTTPException = HTTPException
            self.uvicorn = uvicorn
            
            self.app = self.FastAPI(
                title="Pyrl Ecosystem API",
                description="API for Pyrl language interpreter and Vue generator",
                version="2.0.0"
            )
            
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            
            self._setup_routes()
            
        except ImportError as e:
            raise ImportError(f"FastAPI or uvicorn not installed: {e}")
    
    def _setup_routes(self):
        @self.app.post("/execute")
        async def execute_code(request: dict):
            try:
                code = request.get('source', '')
                result = self.vm.execute(code)
                return {
                    "success": True,
                    "result": result,
                    "memory": self.vm.memory
                }
            except PyrlSyntaxError as e:
                raise self.HTTPException(status_code=400, detail=str(e))
            except PyrlRuntimeError as e:
                raise self.HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                raise self.HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/run_tests")
        async def run_tests(request: dict):
            try:
                code = request.get('source', '')
                results = self.vm.run_tests(code)
                summary = self.vm.get_test_summary()
                
                return {
                    "success": True,
                    "results": [
                        {
                            "name": r.name,
                            "success": r.success,
                            "message": r.message,
                            "expected": r.expected,
                            "actual": r.actual,
                            "type": r.test_type
                        }
                        for r in results
                    ],
                    "summary": summary
                }
            except Exception as e:
                raise self.HTTPException(status_code=400, detail=str(e))
        
        @self.app.post("/generate_vue")
        async def generate_vue(request: dict):
            try:
                name = request.get('name', 'Component')
                props = request.get('props', {})
                
                vue_code = generate_vue_component(name, props)
                
                return {
                    "success": True,
                    "component": vue_code,
                    "name": name
                }
            except Exception as e:
                raise self.HTTPException(status_code=400, detail=str(e))
        
        @self.app.get("/memory")
        async def get_memory():
            return {
                "success": True,
                "memory": self.vm.memory
            }
        
        @self.app.post("/reset")
        async def reset_vm():
            self.vm.reset()
            return {
                "success": True,
                "message": "VM reset successfully"
            }
        
        @self.app.get("/health")
        async def health_check():
            return {
                "status": "healthy",
                "version": "2.0.0"
            }
    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        print(f"Starting Pyrl HTTP Server on http://{host}:{port}")
        self.uvicorn.run(self.app, host=host, port=port)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    vm = PyrlVM()
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {filepath}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
        
        if filepath.endswith('.pyrl'):
            try:
                result = vm.execute(code)
                print("\n=== Execution Result ===")
                print(result)
                print("\n=== Memory State ===")
                print(json.dumps(vm.memory, indent=2, default=str))
            except PyrlSyntaxError as e:
                print(f"Syntax Error: {e}")
                sys.exit(1)
            except PyrlRuntimeError as e:
                print(f"Runtime Error: {e}")
                sys.exit(1)
        else:
            print("Please provide a .pyrl file")
            sys.exit(1)
    else:
        try:
            server = PyrlHTTPServer(vm)
            server.run()
        except ImportError:
            print("Error: FastAPI and uvicorn are required for HTTP server mode")
            print("Install with: pip install fastapi uvicorn")
            sys.exit(1)


if __name__ == "__main__":
    main()
