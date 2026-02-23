#!/usr/bin/env python3
"""
Run all Pyrl examples sequentially
"""
import subprocess
import sys
import os
from pathlib import Path

def run_pyrl_file(filepath):
    """Run a single Pyrl file and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {filepath.name}")
    print(f"{'='*60}")
    
    result = subprocess.run(
        [sys.executable, "/home/z/my-project/pyrl/pyrl_cli.py", str(filepath)],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    # Print stdout
    if result.stdout:
        print(result.stdout)
    
    # Print stderr if there are errors
    if result.stderr:
        print(f"[STDERR] {result.stderr}")
    
    return result.returncode == 0

def main():
    examples_dir = Path("/home/z/my-project/pyrl/examples/runnable")
    
    if not examples_dir.exists():
        print(f"Error: Directory {examples_dir} not found")
        return 1
    
    # Get all .pyrl files sorted
    pyrl_files = sorted(examples_dir.glob("*.pyrl"))
    
    if not pyrl_files:
        print("No .pyrl files found")
        return 1
    
    print(f"Found {len(pyrl_files)} Pyrl files to run\n")
    
    passed = 0
    failed = 0
    results = []
    
    for filepath in pyrl_files:
        success = run_pyrl_file(filepath)
        if success:
            passed += 1
            results.append((filepath.name, "PASSED"))
            print(f"✓ {filepath.name} - PASSED")
        else:
            failed += 1
            results.append((filepath.name, "FAILED"))
            print(f"✗ {filepath.name} - FAILED")
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total:  {len(pyrl_files)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"{'='*60}")
    
    # Detailed results
    print("\nDetailed Results:")
    for name, status in results:
        icon = "✓" if status == "PASSED" else "✗"
        print(f"  {icon} {name}: {status}")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
