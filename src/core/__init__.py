"""
Pyrl Core Module
Core components of the Pyrl language interpreter.
Based on Lark parser with integrated lexer.
"""

# Main VM (Lark-based)
from .vm import (
    PyrlVM,
    run,
    run_file,
    create_vm,
    PyrlFunction,
    Environment,
    PyrlRuntimeError,
    ReturnValue,
    BreakException,
    ContinueException,
    BUILTINS,
    CONSTANTS,
)

# Lark parser (primary parser)
from .lark_parser import (
    PyrlLarkParser,
    parse_lark,
    parse_file_lark,
    print_ast,
    GRAMMAR,
    # AST nodes from Lark parser
    Program,
    ScalarVar,
    ArrayVar,
    HashVar,
    FuncVar,
    IdentRef,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    NoneLiteral,
    ArrayLiteral,
    HashLiteral,
    RegexLiteral,
    BinaryOp,
    UnaryOp,
    Assignment,
    HashAccess,
    ArrayAccess,
    FunctionCall,
    FunctionDef,
    IfStatement,
    ForLoop,
    WhileLoop,
    ReturnStatement,
    PrintStatement,
    AssertStatement,
    TestBlock,
    VueComponent,
)

# Exceptions
from .exceptions import (
    PyrlError,
    ParseError,
    RuntimeError,
    VariableError,
    FunctionError,
    TypeError_,
    IndexError_,
    KeyError_,
    ImportError_,
    ReturnException,
    BreakException,
    ContinueException,
)


__all__ = [
    # VM
    'PyrlVM',
    'run',
    'run_file',
    'create_vm',
    'PyrlFunction',
    'Environment',
    'PyrlRuntimeError',
    'ReturnValue',
    'BreakException',
    'ContinueException',

    # Parser (Lark-based)
    'PyrlLarkParser',
    'parse_lark',
    'parse_file_lark',
    'print_ast',
    'GRAMMAR',

    # AST Nodes (Lark-based)
    'Program',
    'ScalarVar',
    'ArrayVar',
    'HashVar',
    'FuncVar',
    'IdentRef',
    'NumberLiteral',
    'StringLiteral',
    'BooleanLiteral',
    'NoneLiteral',
    'ArrayLiteral',
    'HashLiteral',
    'RegexLiteral',
    'BinaryOp',
    'UnaryOp',
    'Assignment',
    'HashAccess',
    'ArrayAccess',
    'FunctionCall',
    'FunctionDef',
    'IfStatement',
    'ForLoop',
    'WhileLoop',
    'ReturnStatement',
    'PrintStatement',
    'AssertStatement',
    'TestBlock',
    'VueComponent',

    # Exceptions
    'PyrlError',
    'ParseError',
    'RuntimeError',
    'VariableError',
    'FunctionError',
    'TypeError_',
    'IndexError_',
    'KeyError_',
    'ImportError_',
    'ReturnException',

    # Builtins
    'BUILTINS',
    'CONSTANTS',
]
