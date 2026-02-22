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

# Import from core module
from .core import (
    # Main VM class
    PyrlVM,
    run,
    run_file,
    create_vm,
    
    # Lexer
    tokenize,
    Lexer,
    
    # Parser
    parse,
    Parser,
    
    # Interpreter
    Interpreter,
    Environment,
    interpret,
    
    # Exceptions
    PyrlError,
    LexerError,
    ParseError,
    RuntimeError,
    VariableError,
    FunctionError,
    TypeError_,
    IndexError_,
    KeyError_,
    ImportError_,
    
    # AST Nodes (most commonly used)
    Token,
    TokenType,
    ASTNode,
    ProgramNode,
)


__version__ = '1.0.0'
__author__ = 'Pyrl Team'

__all__ = [
    # Main API
    'PyrlVM',
    'run',
    'run_file',
    'create_vm',
    
    # Lower-level API
    'tokenize',
    'Lexer',
    'parse',
    'Parser',
    'Interpreter',
    'Environment',
    'interpret',
    
    # Exceptions
    'PyrlError',
    'LexerError',
    'ParseError',
    'RuntimeError',
    'VariableError',
    'FunctionError',
    'TypeError_',
    'IndexError_',
    'KeyError_',
    'ImportError_',
    
    # AST
    'Token',
    'TokenType',
    'ASTNode',
    'ProgramNode',
]
