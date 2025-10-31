#!/usr/bin/env python3
"""
Test runner for Computer System project
"""
import pytest
import sys
import os

def main():
    """Run all tests"""
    # Запускаем pytest для директории tests
    return pytest.main([
        "tests",
        "-v",           # verbose
        "--tb=short",   # shorter tracebacks
        "-s"           # show print output
    ])

if __name__ == '__main__':
    print("Running Computer System Tests...")
    exit_code = main()
    print(f"Tests completed with exit code: {exit_code}")
    sys.exit(exit_code)