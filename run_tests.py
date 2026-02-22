#!/usr/bin/env python3
"""
Run Pyrl tests with coverage reporting
"""

import subprocess
import sys
import os

def main():
    """Run tests with coverage"""
    
    # Change to project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n" + "="*60)
        print("ALL TESTS PASSED!")
        print("="*60)
        print("\nCoverage report generated in htmlcov/")
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
