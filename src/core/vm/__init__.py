"""
Pyrl VM Package

Virtual Machine for the Pyrl programming language.

This package provides:
- PyrlVM: Main virtual machine for executing Pyrl code
- Environment: Variable scoping and lookup
- PyrlFunction, PyrlClass, PyrlInstance, PyrlMethod: OOP support
- Built-in functions organized by category
- Exception classes for control flow and errors
"""

# Main VM class
from .vm import PyrlVM, run, run_file, create_vm

# Environment
from .environment import Environment

# Objects (OOP support)
from .objects import PyrlFunction, PyrlClass, PyrlInstance, PyrlMethod

# Exceptions
from .exceptions import (
    ReturnValue,
    BreakException,
    ContinueException,
    PyrlRuntimeError
)

# Built-in registries (for extension)
from .builtins import BUILTINS, CONSTANTS
from .builtins_http import HTTP_BUILTINS
from .builtins_db import DB_BUILTINS
from .builtins_crypto import CRYPTO_BUILTINS

__all__ = [
    # Main VM
    'PyrlVM',
    'run',
    'run_file',
    'create_vm',
    
    # Environment
    'Environment',
    
    # Objects
    'PyrlFunction',
    'PyrlClass',
    'PyrlInstance',
    'PyrlMethod',
    
    # Exceptions
    'ReturnValue',
    'BreakException',
    'ContinueException',
    'PyrlRuntimeError',
    
    # Built-in registries
    'BUILTINS',
    'CONSTANTS',
    'HTTP_BUILTINS',
    'DB_BUILTINS',
    'CRYPTO_BUILTINS',
]
