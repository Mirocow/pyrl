"""
Pyrl Test Configuration
Pytest fixtures and configuration for Pyrl tests.
"""
import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from the correct module path (FIXED: was from pyrl_vm import)
from src.core.vm import (
    PyrlVM,
    run,
    run_file,
    create_vm,
)
from src.core.lexer import tokenize, Lexer
from src.core.parser import parse, Parser
from src.core.interpreter import Interpreter, Environment
from src.core.exceptions import (
    PyrlError,
    LexerError,
    ParseError,
    RuntimeError as PyrlRuntimeError,
    VariableError,
    FunctionError,
)
from src.core.ast_nodes import Token, TokenType


# Pytest fixtures
@pytest.fixture
def vm():
    """Create a fresh PyrlVM instance for each test."""
    return PyrlVM()


@pytest.fixture
def vm_debug():
    """Create a PyrlVM instance with debug mode enabled."""
    return PyrlVM(debug=True)


@pytest.fixture
def lexer():
    """Create a Lexer instance."""
    return Lexer


@pytest.fixture
def parser():
    """Create a Parser instance."""
    return Parser


@pytest.fixture
def interpreter():
    """Create an Interpreter instance with fresh environment."""
    return Interpreter()


@pytest.fixture
def environment():
    """Create a fresh Environment instance."""
    return Environment()


# Test helpers
def assert_vm_result(vm: PyrlVM, source: str, expected):
    """Helper to run source and assert the result."""
    result = vm.run(source)
    assert result == expected, f"Expected {expected}, got {result}"


def assert_vm_variable(vm: PyrlVM, var_name: str, expected):
    """Helper to check a variable value."""
    value = vm.get_variable(var_name)
    assert value == expected, f"Variable '{var_name}': expected {expected}, got {value}"


def assert_raises(vm: PyrlVM, source: str, exception_class):
    """Helper to assert that running source raises an exception."""
    with pytest.raises(exception_class):
        vm.run(source)


# Configure pytest
def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "lexer: marks tests for lexer functionality"
    )
    config.addinivalue_line(
        "markers", "parser: marks tests for parser functionality"
    )
    config.addinivalue_line(
        "markers", "interpreter: marks tests for interpreter functionality"
    )
    config.addinivalue_line(
        "markers", "vm: marks tests for VM functionality"
    )
    config.addinivalue_line(
        "markers", "integration: marks integration tests"
    )
