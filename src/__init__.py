"""
Pyrl Language Interpreter
A hybrid Python-Perl inspired language with sigil-based variables.

Features:
    - Sigil variables: $scalar, @array, %hash, &function
    - Python-style indentation syntax
    - Dynamic typing
    - Rich built-in functions
    - Classes and objects
    - Exception handling

Quick Start:
    from src import PyrlVM
    
    vm = PyrlVM()
    result = vm.run('$x = 10 + 5')
    print(result)  # 15
"""

# Import from core module (Lark-based)
from .core import (
    # Main VM class
    PyrlVM,
    run,
    run_file,
    create_vm,
    Environment,
    
    # Parser (Lark-based)
    PyrlLarkParser,
    parse_lark,
    parse_file_lark,
    
    # Exceptions
    PyrlError,
    ParseError,
    RuntimeError,
    VariableError,
    FunctionError,
    
    # AST Nodes (Lark-based)
    Program,
    ScalarVar,
    ArrayVar,
    HashVar,
    FuncVar,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    ArrayLiteral,
    HashLiteral,
    BinaryOp,
    UnaryOp,
    Assignment,
    FunctionCall,
    FunctionDef,
    IfStatement,
    ForLoop,
    WhileLoop,
    ReturnStatement,
)


__version__ = '1.1.0'
__author__ = 'Pyrl Team'

__all__ = [
    # Main API
    'PyrlVM',
    'run',
    'run_file',
    'create_vm',
    'Environment',
    
    # Parser
    'PyrlLarkParser',
    'parse_lark',
    'parse_file_lark',
    
    # Exceptions
    'PyrlError',
    'ParseError',
    'RuntimeError',
    'VariableError',
    'FunctionError',
    
    # AST Nodes
    'Program',
    'ScalarVar',
    'ArrayVar',
    'HashVar',
    'FuncVar',
    'NumberLiteral',
    'StringLiteral',
    'BooleanLiteral',
    'ArrayLiteral',
    'HashLiteral',
    'BinaryOp',
    'UnaryOp',
    'Assignment',
    'FunctionCall',
    'FunctionDef',
    'IfStatement',
    'ForLoop',
    'WhileLoop',
    'ReturnStatement',
]
