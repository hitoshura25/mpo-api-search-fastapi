import pytest
import sys

if __name__ == "__main__":
    # Run pytest and capture the exit code
    exit_code = pytest.main([
        "tests/", 
        "-vv", 
        "--cov=app", 
        "--cov-report=html",
        "--cov-report=xml",
        "--cov-report=term-missing"
    ])  # You can add more pytest arguments here

    # Exit with the same code as pytest
    sys.exit(exit_code)