# FILE: tests/conftest.py
"""
Pytest configuration and fixtures for Pyrl tests
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pyrl_vm import (
    PyrlVM, PyrlParser, ASTBuilder, PyrlInterpreter,
    PyrlSyntaxError, PyrlRuntimeError, PyrlTypeError, ReturnException,
    # AST Nodes
    ASTNode, AssignmentNode, BinaryOpNode, UnaryOpNode, VariableNode,
    LiteralNode, HashLiteralNode, ArrayLiteralNode, HashAccessNode,
    ArrayAccessNode, ConditionalNode, LoopNode, FunctionDefNode,
    FunctionCallNode, PrintNode, ReturnNode, AssertionNode,
    TestBlockNode, VueGenNode, BlockNode, ProgramNode, TestResult,
    generate_vue_component
)


@pytest.fixture
def vm():
    """Create a fresh PyrlVM instance for each test"""
    return PyrlVM()


@pytest.fixture
def parser():
    """Create a PyrlParser instance"""
    return PyrlParser()


@pytest.fixture
def ast_builder():
    """Create an ASTBuilder instance"""
    return ASTBuilder()


@pytest.fixture
def interpreter(vm):
    """Create an interpreter with a VM"""
    return PyrlInterpreter(vm)


# Export all classes for tests
__all__ = [
    'pytest',
    'vm',
    'parser', 
    'ast_builder',
    'interpreter',
    'PyrlVM',
    'PyrlParser',
    'ASTBuilder',
    'PyrlInterpreter',
    'PyrlSyntaxError',
    'PyrlRuntimeError',
    'PyrlTypeError',
    'ReturnException',
    'ASTNode',
    'AssignmentNode',
    'BinaryOpNode',
    'UnaryOpNode',
    'VariableNode',
    'LiteralNode',
    'HashLiteralNode',
    'ArrayLiteralNode',
    'HashAccessNode',
    'ArrayAccessNode',
    'ConditionalNode',
    'LoopNode',
    'FunctionDefNode',
    'FunctionCallNode',
    'PrintNode',
    'ReturnNode',
    'AssertionNode',
    'TestBlockNode',
    'VueGenNode',
    'BlockNode',
    'ProgramNode',
    'TestResult',
    'generate_vue_component'
]
