"""
Pyrl Lark Parser Module
Parses Pyrl source code using Lark parser with grammar-based parsing.
Enhanced: Detailed error reporting with line numbers, context, and visual markers.
"""
from typing import List, Optional, Any, Dict, Union
from dataclasses import dataclass, field
from lark import Lark, Transformer, Token, Tree
from lark.indenter import Indenter
from lark.exceptions import UnexpectedToken, UnexpectedInput, GrammarError


# ===========================================
# Grammar Definition
# ===========================================

GRAMMAR = r"""
start: (_NL | statement)*

statement: simple_stmt _NL?
         | compound_stmt

simple_stmt: return_statement
           | assignment
           | print_statement
           | assertion_statement
           | expression_statement

assertion_statement: "assert" expression comparison_op expression
                   | "assert" expression

comparison_op: COMP_OP

expression_statement: expression

compound_stmt: function_definition
             | conditional
             | loop
             | test_block
             | vue_component_gen

function_definition: FUNC_VAR "(" [arg_list] ")" ":" _NL INDENT statement+ DEDENT
                   | "def" IDENT "(" [arg_list] ")" ":" _NL INDENT statement+ DEDENT

assignment: assign_target "=" expression

assign_target: SCALAR_VAR
             | ARRAY_VAR
             | HASH_VAR
             | hash_access
             | array_access

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
             | "(" expression ")"
             | regex_literal
             | function_call
             | hash_access
             | array_access
             | var_ref

// FIXED: Added IDENT to support built-in functions (str, len, int, etc.)
?var_ref: SCALAR_VAR
        | ARRAY_VAR
        | HASH_VAR
        | FUNC_VAR
        | IDENT

// Hash access uses {} brackets: %hash{"key"}
hash_access: primary_expr "{" expression "}"
// Array access uses [] brackets: @array[0]
array_access: primary_expr "[" expression "]"

literal: STRING | NUMBER | BOOLEAN | NONE | hash_literal | array_literal

// Hash literal - supports multi-line
hash_literal: "{" [_NL* hash_item ("," _NL* hash_item)* _NL*] [","] "}"
hash_item: (STRING | IDENT) ":" expression

// Array literal - supports multi-line
array_literal: "[" [_NL* expression ("," _NL* expression)* _NL*] [","] "]"

regex_literal: "r" STRING

conditional: "if" expression ":" _NL INDENT statement+ DEDENT else_clause?
else_clause: "elif" expression ":" _NL INDENT statement+ DEDENT else_clause?
           | "else" ":" _NL INDENT statement+ DEDENT

loop: "for" SCALAR_VAR "in" expression ":" _NL INDENT statement+ DEDENT
    | "while" expression ":" _NL INDENT statement+ DEDENT

test_block: "test" STRING? ":" _NL INDENT statement+ DEDENT

print_statement: "print" "(" expression ")"

vue_component_gen: "vue" STRING ":" _NL INDENT vue_property+ DEDENT
vue_property: IDENT ":" expression _NL

function_call: primary_expr "(" [arg_list] ")"

arg_list: expression ("," expression)*

return_statement: "return" expression?

// ===========================================
// Variable Types with Sigils
// ===========================================
// $ - Scalar variables (single values)
// @ - Array variables (lists)
// % - Hash variables (dictionaries)
// & - Function variables (references)
SCALAR_VAR: "$" IDENT
ARRAY_VAR: "@" IDENT
HASH_VAR: "%" IDENT
FUNC_VAR: "&" IDENT

// FIXED: BOOLEAN and NONE before IDENT to prevent misidentification
BOOLEAN: "True" | "False" | "true" | "false"
NONE: "None" | "none" | "null"

// IDENT last (least specific)
IDENT: /[a-zA-Z_][a-zA-Z0-9_]*/

STRING: ESCAPED_STRING
       | SINGLE_QUOTED_STRING

SINGLE_QUOTED_STRING: /'[^']*'/

NUMBER: SIGNED_INT | SIGNED_FLOAT

// ===========================================
// Operators - FIXED: Order matters! Longer operators first
// ===========================================
COMP_OP: "==" | "!=" | "<=" | ">=" | "=~" | "!~" | "<" | ">"
ADD_OP: "+" | "-"
MUL_OP: "*" | "/" | "%" | "//"
NOT_OP: "!"
MINUS_OP: "-"

%import common.ESCAPED_STRING
%import common.SIGNED_INT
%import common.SIGNED_FLOAT
%import common.WS_INLINE

// Proper regex syntax for newlines (no broken \r?\n)
_NL: /(?:\r?\n[\t ]*)+/

// FIXED: Proper regex syntax for comments (no broken newlines)
COMMENT: /#[^\n]*/
       | /\/\/[^\n]*/

%ignore WS_INLINE
%ignore COMMENT
%declare INDENT DEDENT
"""


# ===========================================
# AST Node Classes
# ===========================================

@dataclass
class Program:
    """Root AST node containing all statements."""
    statements: List[Any] = field(default_factory=list)


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


@dataclass(frozen=True)
class IdentRef:
    """Identifier reference (for built-in functions)."""
    name: str


@dataclass
class NumberLiteral:
    """Numeric literal."""
    value: Union[int, float]


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
    elements: List[Any] = field(default_factory=list)


@dataclass
class HashLiteral:
    """Hash literal {key: value}."""
    pairs: Dict[str, Any] = field(default_factory=dict)


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
    """Hash access with {} brackets: %hash{"key"}"""
    obj: Any
    key: Any


@dataclass
class ArrayAccess:
    """Array access with [] brackets: @array[0]"""
    obj: Any
    index: Any


@dataclass
class FunctionCall:
    """Function call expression."""
    name: str
    args: List[Any] = field(default_factory=list)


@dataclass
class FunctionDef:
    """Function definition."""
    name: str
    params: List[str] = field(default_factory=list)
    body: List[Any] = field(default_factory=list)


@dataclass
class IfStatement:
    """If/elif/else statement."""
    condition: Any
    then_body: List[Any] = field(default_factory=list)
    elif_clauses: List[tuple] = field(default_factory=list)
    else_body: Optional[List[Any]] = None


@dataclass
class ForLoop:
    """For loop statement."""
    var: str
    iterable: Any
    body: List[Any] = field(default_factory=list)


@dataclass
class WhileLoop:
    """While loop statement."""
    condition: Any
    body: List[Any] = field(default_factory=list)


@dataclass
class ReturnStatement:
    """Return statement."""
    value: Optional[Any] = None


@dataclass
class PrintStatement:
    """Print statement."""
    value: Any


@dataclass
class AssertStatement:
    """Assert statement."""
    left: Any
    operator: Optional[str] = None
    right: Optional[Any] = None


@dataclass
class TestBlock:
    """Test block."""
    name: Optional[str] = None
    body: List[Any] = field(default_factory=list)


@dataclass
class VueComponent:
    """Vue component generation."""
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)


# ===========================================
# Indenter for Python-like indentation
# ===========================================

class PyrlIndenter(Indenter):
    """Handle Python-like indentation for Lark parser."""

    NL_type = '_NL'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = 'INDENT'
    DEDENT_type = 'DEDENT'
    tab_len = 4


# ===========================================
# Error Reporting
# ===========================================

class ParseErrorInfo:
    """Detailed parse error information."""

    def __init__(self, source: str, exception: Exception):
        self.source = source
        self.exception = exception
        self.lines = source.split('\n')  # Proper newline
        self.line_num = 1
        self.col_num = 1
        self.context_lines = 3
        self._parse_exception()

    def _parse_exception(self):
        if isinstance(self.exception, UnexpectedToken):
            self.line_num = self.exception.line
            self.col_num = self.exception.column
            self.token = self.exception.token
            self.expected = self.exception.accepts or []
        elif isinstance(self.exception, UnexpectedInput):
            self.line_num = getattr(self.exception, 'line', 1)
            self.col_num = getattr(self.exception, 'column', 1)
            self.token = getattr(self.exception, 'token', None)
            self.expected = []
        else:
            self.token = None
            self.expected = []

    def get_context(self) -> str:
        start_line = max(0, self.line_num - self.context_lines - 1)
        end_line = min(len(self.lines), self.line_num + self.context_lines)
        context = []
        line_num_width = len(str(end_line))
        for i in range(start_line, end_line):
            line_no = i + 1
            line_content = self.lines[i] if i < len(self.lines) else ''
            prefix = f"{line_no:>{line_num_width}} | "
            context.append(f"{prefix}{line_content}")
            if i + 1 == self.line_num:
                marker = ' ' * len(prefix) + ' ' * (self.col_num - 1) + '^' * max(1, len(str(self.token.value)) if self.token else 1)
                context.append(f"\033[91m{marker}\033[0m")
        return '\n'.join(context)  # Proper newline

    def format_expected(self) -> str:
        if not self.expected:
            return "Unknown"
        # Handle both set and list types for expected tokens
        expected_items = list(self.expected) if isinstance(self.expected, (set, frozenset)) else self.expected
        token_map = {
            'SCALAR_VAR': '$variable', 'ARRAY_VAR': '@variable', 'HASH_VAR': '%variable',
            'FUNC_VAR': '&variable', 'IDENT': 'identifier', 'STRING': 'string',
            'NUMBER': 'number', 'BOOLEAN': 'boolean', 'NONE': 'None',
            'LPAR': '(', 'RPAR': ')', 'LSQB': '[', 'RSQB': ']', 'LBRACE': '{', 'RBRACE': '}',
            'COLON': ':', 'COMMA': ',', 'COMP_OP': 'comparison', 'ADD_OP': '+/-',
            'MUL_OP': '*/%', 'IF': 'if', 'ELSE': 'else', 'ELIF': 'elif',
            'FOR': 'for', 'WHILE': 'while', 'DEF': 'def', 'RETURN': 'return',
            'PRINT': 'print', '_NL': 'newline',
        }
        readable = [token_map.get(str(t), str(t)) for t in expected_items[:10]]
        if len(expected_items) > 10:
            readable.append(f"... and {len(expected_items) - 10} more")
        return ', '.join(readable)

    def __str__(self) -> str:
        error_msg = [
            "\033[91m" + "=" * 60 + "\033[0m",
            "\033[91mPARSE ERROR\033[0m",
            "\033[91m" + "=" * 60 + "\033[0m",
            f"\033[93mLocation:\033[0m Line {self.line_num}, Column {self.col_num}",
        ]
        if self.token:
            error_msg.append(f"\033[93mUnexpected token:\033[0m {self.token.value!r} (type: {self.token.type})")
        error_msg.append(f"\033[93mExpected one of:\033[0m {self.format_expected()}")
        error_msg.append("")
        error_msg.append("\033[93mContext:\033[0m")
        error_msg.append(self.get_context())
        error_msg.append("")
        error_msg.append("\033[91m" + "=" * 60 + "\033[0m")
        return '\n'.join(error_msg)


# ===========================================
# AST Transformer
# ===========================================

class PyrlTransformer(Transformer):
    """Transform Lark parse tree into Pyrl AST."""

    def _filter_tokens(self, items):
        return [c for c in items if c is not None and not isinstance(c, Token)]

    def start(self, children):
        statements = []
        for child in children:
            if isinstance(child, list):
                statements.extend(self._filter_tokens(child))
            elif child is not None and not isinstance(child, Token):
                statements.append(child)
        return Program(statements=statements)

    def statement(self, children):
        return children[0] if children and not isinstance(children[0], Token) else None

    def simple_stmt(self, children):
        return children[0] if children and not isinstance(children[0], Token) else None

    def compound_stmt(self, children):
        return children[0] if children and not isinstance(children[0], Token) else None

    def expression_statement(self, children):
        return children[0] if children and not isinstance(children[0], Token) else None

    def SCALAR_VAR(self, t): return ScalarVar(name=t.value[1:])
    def ARRAY_VAR(self, t): return ArrayVar(name=t.value[1:])
    def HASH_VAR(self, t): return HashVar(name=t.value[1:])
    def FUNC_VAR(self, t): return FuncVar(name=t.value[1:])
    def IDENT(self, t): return IdentRef(name=t.value)

    def NUMBER(self, t):
        v = t.value
        return NumberLiteral(value=float(v) if '.' in v or 'e' in v.lower() or 'E' in v else int(v))

    def STRING(self, t):
        v = t.value
        if len(v) >= 2:
            if v.startswith('"') and v.endswith('"'):
                v = v[1:-1].replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r').replace('\\"', '"').replace('\\\\', '\\')
            elif v.startswith("'") and v.endswith("'"):
                v = v[1:-1]
        return StringLiteral(value=v)

    def BOOLEAN(self, t): return BooleanLiteral(value=t.value.lower() == 'true')
    def NONE(self, t): return NoneLiteral()

    def array_literal(self, children):
        return ArrayLiteral(elements=[c for c in children if c is not None and not (isinstance(c, Token) and c.value == ',')])

    def hash_literal(self, children):
        pairs = {}
        for c in children:
            if isinstance(c, tuple) and len(c) == 2:
                key, value = c
                if isinstance(key, IdentRef): key = key.name
                pairs[key] = value
        return HashLiteral(pairs=pairs)

    def hash_item(self, children):
        if len(children) < 2: return None
        key = children[0]
        if isinstance(key, Token):
            key = key.value
            if (key.startswith('"') and key.endswith('"')) or (key.startswith("'") and key.endswith("'")):
                key = key[1:-1]
        # Handle IdentRef for hash keys
        elif isinstance(key, IdentRef):
            key = key.name
        return (key, children[1])

    def regex_literal(self, children):
        p = children[0]
        return RegexLiteral(pattern=p.value if isinstance(p, StringLiteral) else str(p))

    def or_expr(self, children): return self._build_binary_ops(children, 'or')
    def and_expr(self, children): return self._build_binary_ops(children, 'and')
    def comparison_expr(self, children): return self._build_binary_ops(children, None)
    def additive_expr(self, children): return self._build_binary_ops(children, None)
    def multiplicative_expr(self, children): return self._build_binary_ops(children, None)

    def _build_binary_ops(self, children, specific_op=None):
        if len(children) == 1: return children[0]
        result = children[0]
        for i in range(1, len(children), 2):
            if isinstance(children[i], Token):
                op = children[i].value
                if specific_op is None or op == specific_op:
                    result = BinaryOp(left=result, operator=op, right=children[i + 1])
        return result

    def unary_expr(self, children):
        if len(children) == 1: return children[0]
        if isinstance(children[0], Token):
            return UnaryOp(operator=children[0].value, operand=children[1])
        return children[0]

    def primary_expr(self, children): return children[0] if children else None
    def literal(self, children): return children[0] if children else None

    def hash_access(self, children):
        return HashAccess(obj=children[0], key=children[1]) if len(children) >= 2 else (children[0] if children else None)

    def array_access(self, children):
        return ArrayAccess(obj=children[0], index=children[1]) if len(children) >= 2 else (children[0] if children else None)

    def assign_target(self, children): return children[0] if children else None

    def assignment(self, children):
        return Assignment(target=children[0], value=children[1]) if len(children) >= 2 else None

    # Handle IdentRef for function names
    def function_definition(self, children):
        """Transform function definition."""
        name = None
        params = []
        body = []
        i = 0
        if i < len(children) and isinstance(children[i], Token) and children[i].value in ('def', '&'):
            i += 1
        if i < len(children):
            if isinstance(children[i], FuncVar):
                name = children[i].name
                i += 1
            elif isinstance(children[i], Token) and children[i].type == 'IDENT':
                name = children[i].value
                i += 1
            # FIXED: Also check for IdentRef
            elif isinstance(children[i], IdentRef):
                name = children[i].name
                i += 1
        while i < len(children) and (isinstance(children[i], Token) and children[i].value in '():' or str(children[i]) in ('_NL', 'INDENT')):
            i += 1
        if i < len(children) and isinstance(children[i], list):
            potential_params = children[i]
            if all(isinstance(p, ScalarVar) for p in potential_params):
                params = [p.name for p in potential_params]
                i += 1
        while i < len(children) and (isinstance(children[i], Token) and children[i].value in '():' or str(children[i]) in ('INDENT', 'DEDENT', '_NL')):
            i += 1
        if i < len(children) and isinstance(children[i], list):
            body = self._filter_tokens(children[i])
        return FunctionDef(name=name or '<anonymous>', params=params, body=body)

    def function_call(self, children):
        if not children: return None
        name_node = children[0]
        if isinstance(name_node, (FuncVar, ScalarVar, ArrayVar, HashVar)):
            name = name_node.name
        elif isinstance(name_node, IdentRef):
            name = name_node.name
        elif isinstance(name_node, Token) and name_node.type == 'IDENT':
            name = name_node.value
        elif hasattr(name_node, 'name'):
            name = name_node.name
        else:
            name = str(name_node)
        args = []
        for child in children[1:]:
            if isinstance(child, list):
                args.extend([c for c in child if c is not None and not (isinstance(c, Token) and c.value == ',')])
            elif child is not None and not isinstance(child, Token):
                args.append(child)
        return FunctionCall(name=name, args=args)

    def arg_list(self, children):
        return [c for c in children if c is not None and not (isinstance(c, Token) and c.value == ',')]

    def conditional(self, children):
        condition = None
        then_body = []
        elif_clauses = []
        else_body = None
        state = 'condition'
        current_elif_cond = None
        for child in children:
            if isinstance(child, Token):
                if child.value == 'if': state = 'condition'
                elif child.value == 'elif': state = 'elif_condition'
                elif child.value == 'else': state = 'else'
                continue
            if state == 'condition' and condition is None:
                condition = child
                state = 'then_body'
            elif state == 'then_body' and isinstance(child, list) and not then_body:
                then_body = self._filter_tokens(child)
            elif state == 'elif_condition':
                current_elif_cond = child
                state = 'elif_body'
            elif state == 'elif_body' and isinstance(child, list):
                elif_clauses.append((current_elif_cond, self._filter_tokens(child)))
                state = 'condition'
            elif state == 'else' and isinstance(child, list):
                else_body = self._filter_tokens(child)
        return IfStatement(condition=condition, then_body=then_body, elif_clauses=elif_clauses, else_body=else_body)

    def else_clause(self, children): return children if children else None

    def loop(self, children):
        if not children: return None
        for child in children:
            if isinstance(child, Token):
                if child.value == 'for':
                    var = None
                    iterable = None
                    body = []
                    for c in children:
                        if isinstance(c, ScalarVar) and var is None:
                            var = c.name
                        elif var and iterable is None and not isinstance(c, Token) and c.value not in ('for', 'in', ':'):
                            iterable = c
                        elif isinstance(c, list) and iterable:
                            body = self._filter_tokens(c)
                    return ForLoop(var=var or '$i', iterable=iterable, body=body)
                elif child.value == 'while':
                    condition = None
                    body = []
                    for c in children:
                        if not isinstance(c, Token) and c.value not in ('while', ':') and condition is None:
                            condition = c
                        elif isinstance(c, list) and condition:
                            body = self._filter_tokens(c)
                    return WhileLoop(condition=condition, body=body)
        return WhileLoop(condition=children[0] if children else None, body=[])

    def return_statement(self, children):
        return ReturnStatement(value=children[0] if children and children[0] is not None else None)

    def print_statement(self, children):
        return PrintStatement(value=children[0] if children else None)

    def assertion_statement(self, children):
        if len(children) == 1:
            return AssertStatement(left=children[0], operator=None, right=None)
        elif len(children) >= 3:
            op = children[1].value if isinstance(children[1], Token) else str(children[1])
            return AssertStatement(left=children[0], operator=op, right=children[2])
        return AssertStatement(left=children[0] if children else None, operator=None, right=None)

    def comparison_op(self, children): return children[0] if children else None

    def test_block(self, children):
        name = None
        body = []
        for child in children:
            if isinstance(child, StringLiteral): name = child.value
            elif isinstance(child, list): body = self._filter_tokens(child)
        return TestBlock(name=name, body=body)

    def vue_component_gen(self, children):
        if not children: return None
        name = children[0].value if isinstance(children[0], StringLiteral) else str(children[0])
        properties = {}
        for child in children[1:]:
            if isinstance(child, tuple) and len(child) == 2:
                properties[child[0]] = child[1]
        return VueComponent(name=name, properties=properties)

    def vue_property(self, children):
        if len(children) >= 2:
            key = children[0].value if isinstance(children[0], Token) else str(children[0])
            return (key, children[1])
        return None


# ===========================================
# Parser Class
# ===========================================

class PyrlLarkParser:
    """Lark-based parser for Pyrl language."""

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.parser = Lark(
            GRAMMAR,
            parser='lalr',
            transformer=PyrlTransformer(),
            postlex=PyrlIndenter(),
            start='start',
            debug=debug
        )

    def parse(self, source: str) -> Program:
        try:
            return self.parser.parse(source)
        except UnexpectedToken as e:
            error_info = ParseErrorInfo(source, e)
            if self.debug:
                print(f"\n\033[93mDebug info:\033[0m")
                print(f"  Token type: {e.token.type}")
                print(f"  Token value: {e.token.value!r}")
                print(f"  Line: {e.line}, Column: {e.column}")
                print(f"  Expected tokens: {e.accepts}")
            raise SyntaxError(str(error_info))
        except UnexpectedInput as e:
            raise SyntaxError(str(ParseErrorInfo(source, e)))
        except GrammarError as e:
            raise SyntaxError(f"Grammar error: {e}")
        except Exception as e:
            raise SyntaxError(f"Parse error: {e}")

    def parse_file(self, filepath: str) -> Program:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return self.parse(f.read())
        except FileNotFoundError:
            raise SyntaxError(f"File not found: {filepath}")
        except UnicodeDecodeError as e:
            raise SyntaxError(f"Encoding error in file {filepath}: {e}")


# ===========================================
# Convenience Functions
# ===========================================

_parser = None

def get_parser(debug: bool = False) -> PyrlLarkParser:
    global _parser
    if _parser is None or debug:
        _parser = PyrlLarkParser(debug=debug)
    return _parser

def parse_lark(source: str, debug: bool = False) -> Program:
    return get_parser(debug).parse(source)

def parse_file_lark(filepath: str, debug: bool = False) -> Program:
    return get_parser(debug).parse_file(filepath)


# ===========================================
# Tree Printer for Debugging
# ===========================================

def print_ast(node, indent: int = 0) -> None:
    pfx = "  " * indent
    if isinstance(node, Program):
        print(f"{pfx}Program:")
        for stmt in node.statements: print_ast(stmt, indent + 1)
    elif isinstance(node, ScalarVar): print(f"{pfx}ScalarVar: ${node.name}")
    elif isinstance(node, ArrayVar): print(f"{pfx}ArrayVar: @{node.name}")
    elif isinstance(node, HashVar): print(f"{pfx}HashVar: %{node.name}")
    elif isinstance(node, FuncVar): print(f"{pfx}FuncVar: &{node.name}")
    elif isinstance(node, IdentRef): print(f"{pfx}IdentRef: {node.name}")
    elif isinstance(node, NumberLiteral): print(f"{pfx}Number: {node.value}")
    elif isinstance(node, StringLiteral): print(f"{pfx}String: {repr(node.value)}")
    elif isinstance(node, BooleanLiteral): print(f"{pfx}Boolean: {node.value}")
    elif isinstance(node, NoneLiteral): print(f"{pfx}None")
    elif isinstance(node, ArrayLiteral):
        print(f"{pfx}Array:")
        for elem in node.elements: print_ast(elem, indent + 1)
    elif isinstance(node, HashLiteral):
        print(f"{pfx}Hash:")
        for k, v in node.pairs.items(): print(f"{pfx}  {k}:"); print_ast(v, indent + 2)
    elif isinstance(node, BinaryOp):
        print(f"{pfx}BinaryOp: {node.operator}"); print_ast(node.left, indent + 2); print_ast(node.right, indent + 2)
    elif isinstance(node, UnaryOp): print(f"{pfx}UnaryOp: {node.operator}"); print_ast(node.operand, indent + 1)
    elif isinstance(node, Assignment):
        print(f"{pfx}Assignment:"); print_ast(node.target, indent + 2); print_ast(node.value, indent + 2)
    elif isinstance(node, HashAccess): print(f"{pfx}HashAccess {{}}:"); print_ast(node.obj, indent + 2); print_ast(node.key, indent + 2)
    elif isinstance(node, ArrayAccess): print(f"{pfx}ArrayAccess []:"); print_ast(node.obj, indent + 2); print_ast(node.index, indent + 2)
    elif isinstance(node, FunctionCall):
        print(f"{pfx}FunctionCall: {node.name}")
        for arg in node.args: print_ast(arg, indent + 1)
    elif isinstance(node, FunctionDef):
        print(f"{pfx}FunctionDef: {node.name}({', '.join(node.params)})")
        for stmt in node.body: print_ast(stmt, indent + 1)
    elif isinstance(node, IfStatement):
        print(f"{pfx}If:"); print_ast(node.condition, indent + 2)
        print(f"{pfx}  then:"); [print_ast(s, indent + 2) for s in node.then_body]
        for cond, body in node.elif_clauses: print(f"{pfx}  elif:"); print_ast(cond, indent + 2); [print_ast(s, indent + 2) for s in body]
        if node.else_body: print(f"{pfx}  else:"); [print_ast(s, indent + 2) for s in node.else_body]
    elif isinstance(node, ForLoop):
        print(f"{pfx}For: {node.var}"); print_ast(node.iterable, indent + 2); print(f"{pfx}  body:"); [print_ast(s, indent + 2) for s in node.body]
    elif isinstance(node, WhileLoop):
        print(f"{pfx}While:"); print_ast(node.condition, indent + 2); print(f"{pfx}  body:"); [print_ast(s, indent + 2) for s in node.body]
    elif isinstance(node, ReturnStatement):
        print(f"{pfx}Return:"); print_ast(node.value, indent + 1) if node.value else None
    elif isinstance(node, PrintStatement): print(f"{pfx}Print:"); print_ast(node.value, indent + 1)
    elif isinstance(node, AssertStatement):
        print(f"{pfx}Assert:"); print_ast(node.left, indent + 1)
        if node.right: print(f"{pfx}  {node.operator}"); print_ast(node.right, indent + 1)
    elif isinstance(node, TestBlock): print(f"{pfx}Test: {node.name or ''}"); [print_ast(s, indent + 1) for s in node.body]
    elif isinstance(node, VueComponent):
        print(f"{pfx}VueComponent: {node.name}")
        for k, v in node.properties.items(): print(f"{pfx}  {k}:"); print_ast(v, indent + 2)
    elif isinstance(node, Token): print(f"{pfx}Token: {node.type} = {node.value!r}")
    else: print(f"{pfx}{type(node).__name__}: {node}")


if __name__ == '__main__':
    test_code = '''
$integer = 42
$name = "Alice"
@numbers = [1, 2, 3, 4, 5]
%person = {name: "John", age: 30}

def greet($name):
    return "Hello, " + $name + "!"

$greeter = &greet
print($greeter("World"))
print("Integer: " + str($integer))
print("Person name: " + %person{"name"})

if $integer > 10:
    print("Large")
else:
    print("Small")

for $i in @numbers:
    print($i)
'''
    parser = PyrlLarkParser(debug=True)
    ast = parser.parse(test_code)
    print_ast(ast)