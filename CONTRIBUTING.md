# Contributing to Config & Data Validator

 Thank you for considering contributing to this project! We welcome bug reports, feature requests, and pull requests.

## Table of Contents
 - [Code of Conduct](#code-of-conduct)
 - [Getting Started](#getting-started)
 - [Development Setup](#development-setup)
 - [Code Style](#code-style)
 - [Testing](#testing)
 - [Submitting Changes](#submitting-changes)
 - [Reporting Issues](#reporting-issues)

## Code of Conduct

 Please be respectful and constructive in all interactions. This project aims to be a welcoming   space for everyone.

## Getting Started

 1. **Fork the repository** on GitHub.
 2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/config-data-validator.git
   cd config-data-validator
- python -m venv .venv
- source .venv/bin/activate   # On Windows: .venv\Scripts\activate
- pip install -r requirements.txt

## Development Setup

 - The project uses Python 3.11 or higher.
 - All source code lives under src/validator/.
 - Tests are in the tests/ directory.
 - Sample files for testing are in samples/.

## code-style

 - This project enforces consistent style with:
 - Black for automatic formatting (line length 88)
 - flake8 for linting
 - mypy for type checking

  # Format code
    black src tests

  # Check linting
    flake8 src tests --max-line-length=88

  # Check types
    mypy src

  # Run tests
    pytest -v
    All commands should pass without errors.

## testing
 We use pytest for unit and integration tests. Run the full test suite with:

 Powershell cmmd
 pytest -v
 To run a specific test file:

 Powershell cmmd
 pytest tests/test_api.py -v

## submitting-changes
 Create a new branch for your feature/fix:

 bash:
 git checkout -b feature/your-feature-name
 Make your changes, following the code style.

 # Write or update tests as needed.

 - Ensure all tests pass and linting is clean.

 - Commit with a clear message:

 bash:
  git commit -m "Add feature: your description"
  Push to your fork:

 bash:
  git push origin feature/your-feature-name

 # Open a Pull Request against the main branch of the original repository.

## reporting-issues

 # Use the GitHub issue tracker. Please include:

 - A clear, descriptive title.

 - Steps to reproduce the problem.

 - Expected vs. actual behavior.

 - Your environment (OS, Python version, any   relevant details).

 - If applicable, logs or screenshots.

# Thank you for helping make this project better! #