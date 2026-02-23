"""
Pyrl Core Module
Core components of the Pyrl language interpreter.
"""

# Legacy parser (still available for backward compatibility)
from .vm import PyrlVM, run, run_file, create_vm
from .lexer import tokenize, Lexer
from .parser import parse, Parser
from .interpreter import Interpreter, Environment, interpret
from .exceptions import (
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
    ReturnException,
    BreakException,
    ContinueException,
)
from .ast_nodes import (
    Token,
    TokenType,
    ASTNode,
    ProgramNode,
    NumberNode,
    StringNode,
    BooleanNode,
    NoneNode,
    ScalarNode,
    ArrayNode,
    HashNode,
    FunctionRefNode,
    BinaryOpNode,
    UnaryOpNode,
    ArrayLiteralNode,
    HashLiteralNode,
    IndexNode,
    AttributeNode,
    CallNode,
    LambdaNode,
    AssignNode,
    PrintNode,
    IfNode,
    WhileNode,
    ForNode,
    ForRangeNode,
    DefNode,
    ReturnNode,
    BreakNode,
    ContinueNode,
    PassNode,
    ImportNode,
    FromImportNode,
    ClassNode,
    TryNode,
    RaiseNode,
    WithNode,
    GlobalNode,
    NonlocalNode,
)
from .builtins import get_builtins, BUILTIN_CONSTANTS, PyrlBuiltin

# Lark parser and VM (primary)
try:
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
    from .vm_lark import (
        PyrlLarkVM,
        run_lark,
        run_file_lark_vm,
        create_lark_vm,
        PyrlFunction,
        Environment as LarkEnvironment,
        PyrlRuntimeError,
        ReturnValue,
        BUILTINS,
        CONSTANTS,
    )
    LARK_AVAILABLE = True
except ImportError as e:
    LARK_AVAILABLE = False
    _import_error = str(e)


__all__ = [
    # VM
    'PyrlVM',
    'run',
    'run_file',
    'create_vm',
    
    # Lexer
    'tokenize',
    'Lexer',
    
    # Parser
    'parse',
    'Parser',
    
    # Interpreter
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
    'ReturnException',
    'BreakException',
    'ContinueException',
    
    # AST Nodes
    'Token',
    'TokenType',
    'ASTNode',
    'ProgramNode',
    'NumberNode',
    'StringNode',
    'BooleanNode',
    'NoneNode',
    'ScalarNode',
    'ArrayNode',
    'HashNode',
    'FunctionRefNode',
    'BinaryOpNode',
    'UnaryOpNode',
    'ArrayLiteralNode',
    'HashLiteralNode',
    'IndexNode',
    'AttributeNode',
    'CallNode',
    'LambdaNode',
    'AssignNode',
    'PrintNode',
    'IfNode',
    'WhileNode',
    'ForNode',
    'ForRangeNode',
    'DefNode',
    'ReturnNode',
    'BreakNode',
    'ContinueNode',
    'PassNode',
    'ImportNode',
    'FromImportNode',
    'ClassNode',
    'TryNode',
    'RaiseNode',
    'WithNode',
    'GlobalNode',
    'NonlocalNode',
    
    # Builtins
    'get_builtins',
    'BUILTIN_CONSTANTS',
    'PyrlBuiltin',
]
