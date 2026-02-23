"""
Pyrl VM Exceptions

Exceptions used by the Pyrl Virtual Machine for control flow and error handling.
"""
from typing import Any


class ReturnValue(Exception):
    """Exception used to return values from functions.
    
    This exception is raised when a return statement is executed,
    and is caught by the function execution mechanism to return
    the value to the caller.
    """
    def __init__(self, value: Any = None):
        self.value = value


class BreakException(Exception):
    """Exception used for break statement in loops.
    
    Raised when a break statement is encountered inside a loop,
    causing the loop to terminate immediately.
    """
    pass


class ContinueException(Exception):
    """Exception used for continue statement in loops.
    
    Raised when a continue statement is encountered inside a loop,
    causing the current iteration to skip to the next iteration.
    """
    pass


class PyrlRuntimeError(Exception):
    """Runtime error in Pyrl code.
    
    This is the base exception for all runtime errors that occur
    during Pyrl code execution, such as undefined variables,
    type errors, and invalid operations.
    """
    pass
