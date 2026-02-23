"""
Pytest configuration and fixtures for Pyrl tests.
"""
import pytest
from src.core.vm import PyrlVM


@pytest.fixture
def vm():
    """Create a fresh VM instance for each test."""
    return PyrlVM()


@pytest.fixture
def debug_vm():
    """Create a debug VM instance."""
    return PyrlVM(debug=True)


@pytest.fixture
def clean_vm():
    """Create a VM and reset it before each test."""
    vm = PyrlVM()
    vm.reset()
    return vm
