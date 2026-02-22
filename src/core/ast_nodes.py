"""
Pyrl AST Nodes Module
Abstract Syntax Tree node definitions for the Pyrl language.
"""
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional, Union
from enum import Enum


class TokenType(Enum):
    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    
    # Sigil variables
    SCALAR = "SCALAR"      # $var
    ARRAY = "ARRAY"        # @var
    HASH = "HASH"          # %var
    FUNCTION = "FUNCTION"  # &var
    
    # Keywords
    IF = "IF"
    ELIF = "ELIF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    IN = "IN"
    DEF = "DEF"
    RETURN = "RETURN"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    PRINT = "PRINT"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NONE = "NONE"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    IMPORT = "IMPORT"
    FROM = "FROM"
    AS = "AS"
    CLASS = "CLASS"
    TRY = "TRY"
    EXCEPT = "EXCEPT"
    FINALLY = "FINALLY"
    RAISE = "RAISE"
    WITH = "WITH"
    LAMBDA = "LAMBDA"
    YIELD = "YIELD"
    GLOBAL = "GLOBAL"
    NONLOCAL = "NONLOCAL"
    PASS = "PASS"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    PERCENT = "PERCENT"
    STARSTAR = "STARSTAR"
    DOUBLESLASH = "DOUBLESLASH"
    
    # Comparison
    EQ = "EQ"
    NE = "NE"
    LT = "LT"
    LE = "LE"
    GT = "GT"
    GE = "GE"
    
    # Assignment
    ASSIGN = "ASSIGN"
    PLUS_ASSIGN = "PLUS_ASSIGN"
    MINUS_ASSIGN = "MINUS_ASSIGN"
    STAR_ASSIGN = "STAR_ASSIGN"
    SLASH_ASSIGN = "SLASH_ASSIGN"
    
    # Delimiters
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    COMMA = "COMMA"
    COLON = "COLON"
    DOT = "DOT"
    ARROW = "ARROW"
    
    # Special
    NEWLINE = "NEWLINE"
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    EOF = "EOF"


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int = 0
    column: int = 0


# AST Node base class - no default fields to avoid inheritance issues
@dataclass
class ASTNode:
    pass


# Literals
@dataclass
class NumberNode(ASTNode):
    value: float
    line: int = 0
    column: int = 0


@dataclass
class StringNode(ASTNode):
    value: str
    line: int = 0
    column: int = 0


@dataclass
class BooleanNode(ASTNode):
    value: bool
    line: int = 0
    column: int = 0


@dataclass
class NoneNode(ASTNode):
    line: int = 0
    column: int = 0


# Variables with sigils
@dataclass
class ScalarNode(ASTNode):
    name: str  # $scalar variable
    line: int = 0
    column: int = 0


@dataclass
class ArrayNode(ASTNode):
    name: str  # @array variable
    line: int = 0
    column: int = 0


@dataclass
class HashNode(ASTNode):
    name: str  # %hash variable
    line: int = 0
    column: int = 0


@dataclass
class FunctionRefNode(ASTNode):
    name: str  # &function reference
    line: int = 0
    column: int = 0


# Expressions
@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode
    line: int = 0
    column: int = 0


@dataclass
class UnaryOpNode(ASTNode):
    operator: str
    operand: ASTNode
    line: int = 0
    column: int = 0


@dataclass
class ArrayLiteralNode(ASTNode):
    elements: List[ASTNode] = field(default_factory=list)
    line: int = 0
    column: int = 0


@dataclass
class HashLiteralNode(ASTNode):
    pairs: Dict[str, ASTNode] = field(default_factory=dict)
    line: int = 0
    column: int = 0


@dataclass
class IndexNode(ASTNode):
    obj: ASTNode = None
    index: ASTNode = None
    line: int = 0
    column: int = 0


@dataclass
class AttributeNode(ASTNode):
    obj: ASTNode = None
    attr: str = ""
    line: int = 0
    column: int = 0


@dataclass
class CallNode(ASTNode):
    callee: ASTNode = None
    args: List[ASTNode] = field(default_factory=list)
    line: int = 0
    column: int = 0


@dataclass
class LambdaNode(ASTNode):
    params: List[str] = field(default_factory=list)
    body: ASTNode = None
    line: int = 0
    column: int = 0


# Statements
@dataclass
class AssignNode(ASTNode):
    target: ASTNode = None
    value: ASTNode = None
    operator: str = "="
    line: int = 0
    column: int = 0


@dataclass
class PrintNode(ASTNode):
    value: ASTNode = None
    line: int = 0
    column: int = 0


@dataclass
class IfNode(ASTNode):
    condition: ASTNode = None
    then_body: List[ASTNode] = field(default_factory=list)
    elif_clauses: List[tuple] = field(default_factory=list)  # List of (condition, body)
    else_body: Optional[List[ASTNode]] = None
    line: int = 0
    column: int = 0


@dataclass
class WhileNode(ASTNode):
    condition: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)
    line: int = 0
    column: int = 0


@dataclass
class ForNode(ASTNode):
    var: str = ""
    iterable: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)
    line: int = 0
    column: int = 0


@dataclass
class ForRangeNode(ASTNode):
    var: str = ""
    start: ASTNode = None
    end: ASTNode = None
    step: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)
    line: int = 0
    column: int = 0


@dataclass
class DefNode(ASTNode):
    name: str = ""
    params: List[str] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    line: int = 0
    column: int = 0


@dataclass
class ReturnNode(ASTNode):
    value: Optional[ASTNode] = None
    line: int = 0
    column: int = 0


@dataclass
class BreakNode(ASTNode):
    line: int = 0
    column: int = 0


@dataclass
class ContinueNode(ASTNode):
    line: int = 0
    column: int = 0


@dataclass
class PassNode(ASTNode):
    line: int = 0
    column: int = 0


@dataclass
class ImportNode(ASTNode):
    module: str = ""
    alias: Optional[str] = None
    line: int = 0
    column: int = 0


@dataclass
class FromImportNode(ASTNode):
    module: str = ""
    names: List[str] = field(default_factory=list)
    aliases: Optional[List[str]] = None
    line: int = 0
    column: int = 0


@dataclass
class ClassNode(ASTNode):
    name: str = ""
    bases: List[str] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    line: int = 0
    column: int = 0


@dataclass
class TryNode(ASTNode):
    try_body: List[ASTNode] = field(default_factory=list)
    except_clauses: List[tuple] = field(default_factory=list)  # (exception_type, var, body)
    finally_body: Optional[List[ASTNode]] = None
    line: int = 0
    column: int = 0


@dataclass
class RaiseNode(ASTNode):
    exception: ASTNode = None
    line: int = 0
    column: int = 0


@dataclass
class WithNode(ASTNode):
    expr: ASTNode = None
    var: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)
    line: int = 0
    column: int = 0


@dataclass
class GlobalNode(ASTNode):
    names: List[str] = field(default_factory=list)
    line: int = 0
    column: int = 0


@dataclass
class NonlocalNode(ASTNode):
    names: List[str] = field(default_factory=list)
    line: int = 0
    column: int = 0


@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)
    line: int = 0
    column: int = 0
