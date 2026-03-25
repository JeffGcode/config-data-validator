#!/usr/bin/env python3
"""
Demo script for the Config & Data Validator.
Runs CLI commands against sample files and the sample database.
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd):
    """Run a shell command and print its output."""
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Command failed with error:")
        print(result.stderr)
    else:
        print(result.stdout)
    return result.returncode

def main():
    # Ensure we are in the project root
    if not (Path(__file__).parent / "src").exists():
        print("Error: Run this script from the project root directory.")
        sys.exit(1)

    # 1. Validate config file
    run_command([
        sys.executable, "-m", "src.validator.cli",
        "--file", "samples/sample_config.yaml"
    ])

    # 2. Validate CSV file
    run_command([
        sys.executable, "-m", "src.validator.cli",
        "--data-file", "samples/sample_data.csv"
    ])

    # 3. Validate database (schema only)
    run_command([
        sys.executable, "-m", "src.validator.cli",
        "--db-url", "sqlite:///sample.db",
        "--table", "users"
    ])

    # 4. Validate database with condition (find underage users)
    run_command([
        sys.executable, "-m", "src.validator.cli",
        "--db-url", "sqlite:///sample.db",
        "--table", "users",
        "--condition", "age < 18"
    ])

    # 5. Validate database with a custom configuration file (if exists)
    config_path = Path("samples/validator_config.yaml")
    if config_path.exists():
        run_command([
            sys.executable, "-m", "src.validator.cli",
            "--config", str(config_path),
            "--verbose"
        ])

    print("\n✅ Demo completed.")

if __name__ == "__main__":
    main()