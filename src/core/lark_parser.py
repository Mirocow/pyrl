"""
Pyrl Lark Parser Module
Parses Pyrl source code using Lark parser with grammar-based parsing.
"""
from typing import List, Optional, Any, Dict
from dataclasses import dataclass
from lark import Lark, Transformer, Token, Tree
from lark.indenter import Indenter


# ===========================================
# Grammar Definition
# ===========================================

GRAMMAR = r"""
start: _NL* statement (_NL+ statement)* _NL*

statement: return_statement
         | assignment 
         | function_definition
         | conditional 
         | loop 
         | test_block 
         | vue_component_gen
         | print_statement
         | assertion_statement
         | expression_statement
         
assertion_statement: "assert" expression comparison_op expression
                   | "assert" expression
                   
comparison_op: "==" | "!=" | "<" | ">" | "<=" | ">="
         
expression_statement: expression
             
function_definition: FUNC_VAR "(" [param_list] ")" ":" _NL INDENT statement+ DEDENT

param_list: SCALAR_VAR ("," SCALAR_VAR)*

assignment: (SCALAR_VAR | ARRAY_VAR | HASH_VAR | hash_access | array_access) "=" expression

?expression: or_expr

?or_expr: and_expr ("or" and_expr)*

?and_expr: comparison_expr ("and" comparison_expr)*

?comparison_expr: additive_expr (COMP_OP additive_expr)*

additive_expr: multiplicative_expr (ADD_OP multiplicative_expr)*

multiplicative_expr: unary_expr (MUL_OP unary_expr)*

?unary_expr: NOT_OP unary_expr
           | MINUS_OP unary_expr
           | primary_expr

?primary_expr: literal 
             | function_call
             | VARIABLE 
             | hash_access
             | array_access
             | "(" expression ")"
             | regex_literal
             
hash_access: HASH_VAR "[" expression "]" | SCALAR_VAR "[" expression "]"

array_access: ARRAY_VAR "[" expression "]"

literal: STRING | NUMBER | BOOLEAN | NONE | hash_literal | array_literal

hash_literal: "{" [hash_item ("," hash_item)*] [","] "}"
hash_item: (STRING | IDENT) ":" expression

array_literal: "[" [expression ("," expression)*] [","] "]"

regex_literal: "r" STRING

conditional: "if" expression ":" _NL INDENT statement+ DEDENT
           | "if" expression ":" _NL INDENT statement+ DEDENT "else" ":" _NL INDENT statement+ DEDENT
           | "if" expression ":" _NL INDENT statement+ DEDENT "elif" expression ":" _NL INDENT statement+ DEDENT
           | "if" expression ":" _NL INDENT statement+ DEDENT "elif" expression ":" _NL INDENT statement+ DEDENT "else" ":" _NL INDENT statement+ DEDENT

loop: "for" SCALAR_VAR "in" expression ":" _NL INDENT statement+ DEDENT
    | "while" expression ":" _NL INDENT statement+ DEDENT

test_block: "test" STRING? ":" _NL INDENT statement+ DEDENT

print_statement: "print" "(" expression ")"

vue_component_gen: "vue" STRING ":" _NL INDENT vue_property+ DEDENT
vue_property: INDENT IDENT ":" expression _NL

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
BOOLEAN: "True" | "False" | "true" | "false"
NONE: "None" | "none" | "null"

OR_OP: "||"
AND_OP: "&&"
COMP_OP: "==" | "!=" | "<" | ">" | "<=" | ">=" | "=~" | "!~"
ADD_OP: "+" | "-"
MUL_OP: "*" | "/" | "%" | "//"
NOT_OP: "!"
MINUS_OP: "-"

%import common.ESCAPED_STRING
%import common.SIGNED_INT
%import common.SIGNED_FLOAT
%import common.WS_INLINE

_NL: /(?:\r?\n[\t ]*)+/

%ignore WS_INLINE
%declare INDENT DEDENT
"""


# ===========================================
# AST Node Classes
# ===========================================

@dataclass
class Program:
    """Root AST node containing all statements."""
    statements: List[Any]


@dataclass
class ScalarVar:
    """Scalar variable ($name)."""
    name: str


@dataclass
class ArrayVar:
    """Array variable (@name)."""
    name: str


@dataclass
class HashVar:
    """Hash variable (%name)."""
    name: str


@dataclass
class FuncVar:
    """Function variable (&name)."""
    name: str


@dataclass
class NumberLiteral:
    """Numeric literal."""
    value: float


@dataclass
class StringLiteral:
    """String literal."""
    value: str


@dataclass
class BooleanLiteral:
    """Boolean literal."""
    value: bool


@dataclass
class NoneLiteral:
    """None/null literal."""
    pass


@dataclass
class ArrayLiteral:
    """Array literal [a, b, c]."""
    elements: List[Any]


@dataclass
class HashLiteral:
    """Hash literal {key: value}."""
    pairs: Dict[str, Any]


@dataclass
class RegexLiteral:
    """Regex literal r"pattern"."""
    pattern: str


@dataclass
class BinaryOp:
    """Binary operation."""
    left: Any
    operator: str
    right: Any


@dataclass
class UnaryOp:
    """Unary operation."""
    operator: str
    operand: Any


@dataclass
class Assignment:
    """Variable assignment."""
    target: Any
    value: Any


@dataclass
class HashAccess:
    """Hash access expression."""
    obj: Any
    key: Any


@dataclass
class ArrayAccess:
    """Array access expression."""
    obj: Any
    index: Any


@dataclass
class FunctionCall:
    """Function call expression."""
    name: str
    args: List[Any]


@dataclass
class FunctionDef:
    """Function definition."""
    name: str
    params: List[str]
    body: List[Any]


@dataclass
class IfStatement:
    """If/elif/else statement."""
    condition: Any
    then_body: List[Any]
    elif_clauses: List[tuple]  # List of (condition, body)
    else_body: Optional[List[Any]]


@dataclass
class ForLoop:
    """For loop statement."""
    var: str
    iterable: Any
    body: List[Any]


@dataclass
class WhileLoop:
    """While loop statement."""
    condition: Any
    body: List[Any]


@dataclass
class ReturnStatement:
    """Return statement."""
    value: Optional[Any]


@dataclass
class PrintStatement:
    """Print statement."""
    value: Any


@dataclass
class AssertStatement:
    """Assert statement."""
    left: Any
    operator: Optional[str]
    right: Optional[Any]


@dataclass
class TestBlock:
    """Test block."""
    name: Optional[str]
    body: List[Any]


@dataclass
class VueComponent:
    """Vue component generation."""
    name: str
    properties: Dict[str, Any]


# ===========================================
# Indenter for Python-like indentation
# ===========================================

class PyrlIndenter(Indenter):
    """Handle Python-like indentation for Lark parser."""
    
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = 'INDENT'
    DEDENT_type = 'DEDENT'
    tab_len = 4


# ===========================================
# AST Transformer
# ===========================================

class PyrlTransformer(Transformer):
    """Transform Lark parse tree into Pyrl AST."""
    
    def start(self, children):
        """Transform start rule."""
        statements = []
        for child in children:
            if isinstance(child, list):
                statements.extend(child)
            else:
                statements.append(child)
        return Program(statements=statements)
    
    def statement(self, children):
        """Transform statement rule."""
        return children[0] if children else None
    
    def expression_statement(self, children):
        """Transform expression statement."""
        return children[0] if children else None
    
    # Variables
    def SCALAR_VAR(self, token):
        """Transform scalar variable."""
        return ScalarVar(name=token.value[1:])  # Remove $ prefix
    
    def ARRAY_VAR(self, token):
        """Transform array variable."""
        return ArrayVar(name=token.value[1:])  # Remove @ prefix
    
    def HASH_VAR(self, token):
        """Transform hash variable."""
        return HashVar(name=token.value[1:])  # Remove % prefix
    
    def FUNC_VAR(self, token):
        """Transform function variable."""
        return FuncVar(name=token.value[1:])  # Remove & prefix
    
    def VARIABLE(self, token):
        """Transform generic variable."""
        return token  # Return as token, will be handled by parent rule
    
    # Literals
    def NUMBER(self, token):
        """Transform number literal."""
        value = token.value
        if '.' in value or 'e' in value.lower():
            return NumberLiteral(value=float(value))
        return NumberLiteral(value=int(value))
    
    def STRING(self, token):
        """Transform string literal."""
        value = token.value
        # Handle escape sequences
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
            value = value.replace('\\n', '\n')
            value = value.replace('\\t', '\t')
            value = value.replace('\\"', '"')
            value = value.replace('\\\\', '\\')
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        return StringLiteral(value=value)
    
    def BOOLEAN(self, token):
        """Transform boolean literal."""
        return BooleanLiteral(value=token.value.lower() in ('true', 'True'))
    
    def NONE(self, token):
        """Transform none literal."""
        return NoneLiteral()
    
    def array_literal(self, children):
        """Transform array literal."""
        elements = [c for c in children if c is not None]
        return ArrayLiteral(elements=elements)
    
    def hash_literal(self, children):
        """Transform hash literal."""
        pairs = {}
        for child in children:
            if isinstance(child, tuple):
                pairs[child[0]] = child[1]
        return HashLiteral(pairs=pairs)
    
    def hash_item(self, children):
        """Transform hash item."""
        key = children[0]
        if isinstance(key, Token):
            key = key.value
            if key.startswith('"') and key.endswith('"'):
                key = key[1:-1]
            elif key.startswith("'") and key.endswith("'"):
                key = key[1:-1]
        value = children[1]
        return (key, value)
    
    def regex_literal(self, children):
        """Transform regex literal."""
        pattern = children[0]
        if isinstance(pattern, StringLiteral):
            return RegexLiteral(pattern=pattern.value)
        return RegexLiteral(pattern=str(pattern))
    
    # Expressions
    def or_expr(self, children):
        """Transform or expression."""
        result = children[0]
        i = 1
        while i < len(children):
            if isinstance(children[i], Token):
                result = BinaryOp(left=result, operator='or', right=children[i + 1])
                i += 2
            else:
                i += 1
        return result
    
    def and_expr(self, children):
        """Transform and expression."""
        result = children[0]
        i = 1
        while i < len(children):
            if isinstance(children[i], Token):
                result = BinaryOp(left=result, operator='and', right=children[i + 1])
                i += 2
            else:
                i += 1
        return result
    
    def comparison_expr(self, children):
        """Transform comparison expression."""
        result = children[0]
        i = 1
        while i < len(children):
            if isinstance(children[i], Token):
                op = children[i].value
                result = BinaryOp(left=result, operator=op, right=children[i + 1])
                i += 2
            else:
                i += 1
        return result
    
    def additive_expr(self, children):
        """Transform additive expression."""
        result = children[0]
        i = 1
        while i < len(children):
            if isinstance(children[i], Token):
                op = children[i].value
                result = BinaryOp(left=result, operator=op, right=children[i + 1])
                i += 2
            else:
                i += 1
        return result
    
    def multiplicative_expr(self, children):
        """Transform multiplicative expression."""
        result = children[0]
        i = 1
        while i < len(children):
            if isinstance(children[i], Token):
                op = children[i].value
                result = BinaryOp(left=result, operator=op, right=children[i + 1])
                i += 2
            else:
                i += 1
        return result
    
    def unary_expr(self, children):
        """Transform unary expression."""
        if len(children) == 1:
            return children[0]
        if isinstance(children[0], Token):
            return UnaryOp(operator=children[0].value, operand=children[1])
        return children[0]
    
    def primary_expr(self, children):
        """Transform primary expression."""
        return children[0]
    
    def literal(self, children):
        """Transform literal."""
        return children[0]
    
    # Access expressions
    def hash_access(self, children):
        """Transform hash access."""
        obj = children[0]
        key = children[1]
        return HashAccess(obj=obj, key=key)
    
    def array_access(self, children):
        """Transform array access."""
        obj = children[0]
        index = children[1]
        return ArrayAccess(obj=obj, index=index)
    
    # Assignment
    def assignment(self, children):
        """Transform assignment."""
        target = children[0]
        value = children[1]
        return Assignment(target=target, value=value)
    
    # Function definition
    def function_definition(self, children):
        """Transform function definition."""
        name = children[0].name if isinstance(children[0], FuncVar) else str(children[0])
        params = []
        body = []
        
        for child in children[1:]:
            if isinstance(child, list):
                # Check if it's params or body
                if all(isinstance(c, str) for c in child):
                    params = child
                else:
                    body = child
            elif isinstance(child, ScalarVar):
                params.append(child.name)
            elif isinstance(child, str):
                params.append(child)
        
        return FunctionDef(name=name, params=params, body=body)
    
    def param_list(self, children):
        """Transform parameter list."""
        params = []
        for child in children:
            if isinstance(child, ScalarVar):
                params.append(child.name)
            elif isinstance(child, str):
                params.append(child)
        return params
    
    # Function call
    def function_call(self, children):
        """Transform function call."""
        name = children[0].name if isinstance(children[0], FuncVar) else str(children[0])
        args = []
        for child in children[1:]:
            if isinstance(child, list):
                args = child
            else:
                args.append(child)
        return FunctionCall(name=name, args=args)
    
    def arg_list(self, children):
        """Transform argument list."""
        return list(children)
    
    # Control flow
    def conditional(self, children):
        """Transform conditional statement."""
        condition = None
        then_body = []
        elif_clauses = []
        else_body = None
        
        i = 0
        while i < len(children):
            child = children[i]
            
            if condition is None and not isinstance(child, list):
                condition = child
            elif isinstance(child, list) and not then_body:
                then_body = child
            elif isinstance(child, Token) and child.value == 'elif':
                # Parse elif clause
                i += 1
                elif_cond = children[i]
                i += 1
                elif_body = children[i]
                elif_clauses.append((elif_cond, elif_body))
            elif isinstance(child, Token) and child.value == 'else':
                # Parse else clause
                i += 1
                else_body = children[i]
            
            i += 1
        
        return IfStatement(
            condition=condition,
            then_body=then_body,
            elif_clauses=elif_clauses,
            else_body=else_body
        )
    
    def loop(self, children):
        """Transform loop statement."""
        # Check if it's for or while
        first_child = children[0]
        
        if isinstance(first_child, Token) and first_child.value == 'for':
            # For loop
            var = children[1].name if isinstance(children[1], ScalarVar) else str(children[1])
            iterable = children[2]
            body = children[3] if len(children) > 3 else []
            return ForLoop(var=var, iterable=iterable, body=body)
        else:
            # While loop
            condition = children[0]
            body = children[1] if len(children) > 1 else []
            return WhileLoop(condition=condition, body=body)
    
    def return_statement(self, children):
        """Transform return statement."""
        value = children[0] if children else None
        return ReturnStatement(value=value)
    
    def print_statement(self, children):
        """Transform print statement."""
        return PrintStatement(value=children[0])
    
    def assertion_statement(self, children):
        """Transform assert statement."""
        if len(children) == 1:
            return AssertStatement(left=children[0], operator=None, right=None)
        return AssertStatement(left=children[0], operator=str(children[1]), right=children[2])
    
    def comparison_op(self, children):
        """Transform comparison operator."""
        return children[0]
    
    def test_block(self, children):
        """Transform test block."""
        name = None
        body = []
        for child in children:
            if isinstance(child, StringLiteral):
                name = child.value
            elif isinstance(child, list):
                body = child
        return TestBlock(name=name, body=body)
    
    def vue_component_gen(self, children):
        """Transform Vue component generation."""
        name = children[0].value if isinstance(children[0], StringLiteral) else str(children[0])
        properties = {}
        for child in children[1:]:
            if isinstance(child, dict):
                properties.update(child)
            elif isinstance(child, tuple):
                properties[child[0]] = child[1]
        return VueComponent(name=name, properties=properties)
    
    def vue_property(self, children):
        """Transform Vue property."""
        key = None
        value = None
        for child in children:
            if isinstance(child, Token):
                key = child.value
            elif not isinstance(child, Token):
                value = child
        return (key, value)


# ===========================================
# Parser Class
# ===========================================

class PyrlLarkParser:
    """Lark-based parser for Pyrl language."""
    
    def __init__(self):
        self.parser = Lark(
            GRAMMAR,
            parser='lalr',
            transformer=PyrlTransformer(),
            postlex=PyrlIndenter(),
            start='start'
        )
    
    def parse(self, source: str) -> Program:
        """Parse source code into AST."""
        try:
            return self.parser.parse(source)
        except Exception as e:
            raise SyntaxError(f"Parse error: {e}")
    
    def parse_file(self, filepath: str) -> Program:
        """Parse a file into AST."""
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        return self.parse(source)


# ===========================================
# Convenience Functions
# ===========================================

# Global parser instance
_parser = None


def get_parser() -> PyrlLarkParser:
    """Get or create the global parser instance."""
    global _parser
    if _parser is None:
        _parser = PyrlLarkParser()
    return _parser


def parse_lark(source: str) -> Program:
    """Parse source code using Lark parser."""
    return get_parser().parse(source)


def parse_file_lark(filepath: str) -> Program:
    """Parse a file using Lark parser."""
    return get_parser().parse_file(filepath)


# ===========================================
# Tree Printer for Debugging
# ===========================================

def print_ast(node, indent: int = 0) -> None:
    """Pretty print AST for debugging."""
    prefix = "  " * indent
    
    if isinstance(node, Program):
        print(f"{prefix}Program:")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)
    
    elif isinstance(node, ScalarVar):
        print(f"{prefix}ScalarVar: ${node.name}")
    
    elif isinstance(node, ArrayVar):
        print(f"{prefix}ArrayVar: @{node.name}")
    
    elif isinstance(node, HashVar):
        print(f"{prefix}HashVar: %{node.name}")
    
    elif isinstance(node, FuncVar):
        print(f"{prefix}FuncVar: &{node.name}")
    
    elif isinstance(node, NumberLiteral):
        print(f"{prefix}Number: {node.value}")
    
    elif isinstance(node, StringLiteral):
        print(f"{prefix}String: {repr(node.value)}")
    
    elif isinstance(node, BooleanLiteral):
        print(f"{prefix}Boolean: {node.value}")
    
    elif isinstance(node, NoneLiteral):
        print(f"{prefix}None")
    
    elif isinstance(node, ArrayLiteral):
        print(f"{prefix}Array:")
        for elem in node.elements:
            print_ast(elem, indent + 1)
    
    elif isinstance(node, HashLiteral):
        print(f"{prefix}Hash:")
        for key, value in node.pairs.items():
            print(f"{prefix}  {key}:")
            print_ast(value, indent + 2)
    
    elif isinstance(node, BinaryOp):
        print(f"{prefix}BinaryOp: {node.operator}")
        print(f"{prefix}  left:")
        print_ast(node.left, indent + 2)
        print(f"{prefix}  right:")
        print_ast(node.right, indent + 2)
    
    elif isinstance(node, UnaryOp):
        print(f"{prefix}UnaryOp: {node.operator}")
        print_ast(node.operand, indent + 1)
    
    elif isinstance(node, Assignment):
        print(f"{prefix}Assignment:")
        print(f"{prefix}  target:")
        print_ast(node.target, indent + 2)
        print(f"{prefix}  value:")
        print_ast(node.value, indent + 2)
    
    elif isinstance(node, HashAccess):
        print(f"{prefix}HashAccess:")
        print(f"{prefix}  object:")
        print_ast(node.obj, indent + 2)
        print(f"{prefix}  key:")
        print_ast(node.key, indent + 2)
    
    elif isinstance(node, ArrayAccess):
        print(f"{prefix}ArrayAccess:")
        print(f"{prefix}  object:")
        print_ast(node.obj, indent + 2)
        print(f"{prefix}  index:")
        print_ast(node.index, indent + 2)
    
    elif isinstance(node, FunctionCall):
        print(f"{prefix}FunctionCall: {node.name}")
        for arg in node.args:
            print_ast(arg, indent + 1)
    
    elif isinstance(node, FunctionDef):
        print(f"{prefix}FunctionDef: {node.name}({', '.join(node.params)})")
        for stmt in node.body:
            print_ast(stmt, indent + 1)
    
    elif isinstance(node, IfStatement):
        print(f"{prefix}If:")
        print(f"{prefix}  condition:")
        print_ast(node.condition, indent + 2)
        print(f"{prefix}  then:")
        for stmt in node.then_body:
            print_ast(stmt, indent + 2)
        if node.elif_clauses:
            for cond, body in node.elif_clauses:
                print(f"{prefix}  elif:")
                print_ast(cond, indent + 2)
                for stmt in body:
                    print_ast(stmt, indent + 2)
        if node.else_body:
            print(f"{prefix}  else:")
            for stmt in node.else_body:
                print_ast(stmt, indent + 2)
    
    elif isinstance(node, ForLoop):
        print(f"{prefix}For: {node.var}")
        print(f"{prefix}  iterable:")
        print_ast(node.iterable, indent + 2)
        print(f"{prefix}  body:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)
    
    elif isinstance(node, WhileLoop):
        print(f"{prefix}While:")
        print(f"{prefix}  condition:")
        print_ast(node.condition, indent + 2)
        print(f"{prefix}  body:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)
    
    elif isinstance(node, ReturnStatement):
        print(f"{prefix}Return:")
        if node.value:
            print_ast(node.value, indent + 1)
    
    elif isinstance(node, PrintStatement):
        print(f"{prefix}Print:")
        print_ast(node.value, indent + 1)
    
    elif isinstance(node, AssertStatement):
        print(f"{prefix}Assert:")
        print_ast(node.left, indent + 1)
        if node.right:
            print(f"{prefix}  {node.operator}")
            print_ast(node.right, indent + 1)
    
    elif isinstance(node, TestBlock):
        print(f"{prefix}Test: {node.name or ''}")
        for stmt in node.body:
            print_ast(stmt, indent + 1)
    
    elif isinstance(node, VueComponent):
        print(f"{prefix}VueComponent: {node.name}")
        for key, value in node.properties.items():
            print(f"{prefix}  {key}:")
            print_ast(value, indent + 2)
    
    else:
        print(f"{prefix}{type(node).__name__}: {node}")


if __name__ == '__main__':
    # Test parser
    test_code = '''
$name = "Alice"
$age = 30

@numbers = [1, 2, 3, 4, 5]

%person = {name: "Bob", age: 25}

def &greet($name):
    print("Hello, " + $name + "!")

&greet($name)

if $age > 18:
    print("Adult")
else:
    print("Minor")

for $i in @numbers:
    print($i)
'''
    
    parser = PyrlLarkParser()
    ast = parser.parse(test_code)
    print_ast(ast)
