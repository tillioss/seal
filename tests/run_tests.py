#!/usr/bin/env python3
"""
Test runner script for SEAL API tests.

This script provides a comprehensive way to run all tests with various options
for coverage reporting, test selection, and output formatting.
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"❌ {description} failed with exit code {result.returncode}")
        return False
    else:
        print(f"✅ {description} completed successfully")
        return True


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run SEAL API tests")
    parser.add_argument(
        "--unit", 
        action="store_true", 
        help="Run only unit tests"
    )
    parser.add_argument(
        "--integration", 
        action="store_true", 
        help="Run only integration tests"
    )
    parser.add_argument(
        "--coverage", 
        action="store_true", 
        default=True,
        help="Generate coverage report (default: True)"
    )
    parser.add_argument(
        "--no-coverage", 
        action="store_true", 
        help="Skip coverage reporting"
    )
    parser.add_argument(
        "--html", 
        action="store_true", 
        help="Generate HTML coverage report"
    )
    parser.add_argument(
        "--verbose", 
        "-v", 
        action="store_true", 
        help="Verbose output"
    )
    parser.add_argument(
        "--fast", 
        action="store_true", 
        help="Skip slow tests"
    )
    parser.add_argument(
        "--parallel", 
        "-n", 
        type=int, 
        help="Run tests in parallel (number of workers)"
    )
    parser.add_argument(
        "--module", 
        "-m", 
        help="Run tests for specific module"
    )
    parser.add_argument(
        "--test", 
        "-t", 
        help="Run specific test function"
    )
    
    args = parser.parse_args()
    
    # Set up environment
    os.environ["PYTHONPATH"] = str(Path(__file__).parent.parent)
    
    # Build pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add test selection
    if args.unit and not args.integration:
        cmd.extend(["-m", "unit"])
    elif args.integration and not args.unit:
        cmd.extend(["-m", "integration"])
    elif args.unit and args.integration:
        cmd.extend(["-m", "unit or integration"])
    
    # Add specific module or test
    if args.module:
        cmd.append(f"tests/unit/{args.module}")
    elif args.test:
        cmd.extend(["-k", args.test])
    
    # Add coverage options
    if args.coverage and not args.no_coverage:
        cmd.extend([
            "--cov=app",
            "--cov-report=term-missing"
        ])
        if args.html:
            cmd.extend(["--cov-report=html"])
    
    # Add verbosity
    if args.verbose:
        cmd.append("-v")
    
    # Add parallel execution
    if args.parallel:
        cmd.extend(["-n", str(args.parallel)])
    
    # Skip slow tests if requested
    if args.fast:
        cmd.extend(["-m", "not slow"])
    
    # Add other useful options
    cmd.extend([
        "--tb=short",
        "--strict-markers",
        "--disable-warnings"
    ])
    
    # Run the tests
    success = run_command(cmd, "Running tests")
    
    if success and args.coverage and not args.no_coverage:
        print(f"\n{'='*60}")
        print("📊 Coverage Summary")
        print(f"{'='*60}")
        
        # Generate coverage report
        coverage_cmd = ["python", "-m", "coverage", "report", "--show-missing"]
        run_command(coverage_cmd, "Generating coverage report")
        
        if args.html:
            html_cmd = ["python", "-m", "coverage", "html"]
            if run_command(html_cmd, "Generating HTML coverage report"):
                print("📄 HTML coverage report generated in htmlcov/index.html")
    
    # Print summary
    print(f"\n{'='*60}")
    if success:
        print("🎉 All tests completed successfully!")
        print("✅ Test suite passed")
    else:
        print("❌ Some tests failed")
        print("🔍 Check the output above for details")
    print(f"{'='*60}")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main()) 