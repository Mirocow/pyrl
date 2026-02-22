"""
Pyrl Exceptions Module
Custom exceptions for the Pyrl language interpreter.
"""


class PyrlError(Exception):
    """Base exception for all Pyrl errors."""
    pass


class LexerError(PyrlError):
    """Exception raised during lexical analysis."""
    
    def __init__(self, message: str, line: int = 0, column: int = 0):
        self.line = line
        self.column = column
        super().__init__(f"Lexer Error at line {line}, column {column}: {message}")


class ParseError(PyrlError):
    """Exception raised during parsing."""
    
    def __init__(self, message: str, line: int = 0, column: int = 0):
        self.line = line
        self.column = column
        super().__init__(f"Parse Error at line {line}, column {column}: {message}")


class RuntimeError(PyrlError):
    """Exception raised during runtime execution."""
    
    def __init__(self, message: str, line: int = 0):
        self.line = line
        super().__init__(f"Runtime Error at line {line}: {message}")


class VariableError(PyrlError):
    """Exception for variable-related errors."""
    
    def __init__(self, message: str, var_name: str = ""):
        self.var_name = var_name
        super().__init__(f"Variable Error '{var_name}': {message}")


class FunctionError(PyrlError):
    """Exception for function-related errors."""
    
    def __init__(self, message: str, func_name: str = ""):
        self.func_name = func_name
        super().__init__(f"Function Error '{func_name}': {message}")


class TypeError_(PyrlError):
    """Exception for type-related errors."""
    
    def __init__(self, message: str, expected: str = "", got: str = ""):
        self.expected = expected
        self.got = got
        super().__init__(f"Type Error: expected {expected}, got {got}. {message}")


class IndexError_(PyrlError):
    """Exception for index-related errors."""
    
    def __init__(self, message: str, index: int = 0):
        self.index = index
        super().__init__(f"Index Error at index {index}: {message}")


class KeyError_(PyrlError):
    """Exception for key-related errors."""
    
    def __init__(self, message: str, key: str = ""):
        self.key = key
        super().__init__(f"Key Error '{key}': {message}")


class ImportError_(PyrlError):
    """Exception for import-related errors."""
    
    def __init__(self, message: str, module: str = ""):
        self.module = module
        super().__init__(f"Import Error '{module}': {message}")


class ReturnException(Exception):
    """Used to implement return statements in functions."""
    
    def __init__(self, value):
        self.value = value


class BreakException(Exception):
    """Used to implement break statements in loops."""
    pass


class ContinueException(Exception):
    """Used to implement continue statements in loops."""
    pass
