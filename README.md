# Config & Data Validator

[![CI Pipeline](https://github.com/JeffGcode/config-data-validator/actions/workflows/ci.yml/badge.svg)](https://github.com/JeffGcode/config-data-validator/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python-based validation service that checks configuration files (YAML/JSON), CSV data, and SQL database schemas. Built with FastAPI, Pydantic, SQLAlchemy, and Docker.

---

## 🚀 Live API

The service is deployed at:  
**[https://config-data-validator.onrender.com](https://config-data-validator.onrender.com)**

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /docs`   | Interactive Swagger UI |
| `POST /validate/config` | Validate YAML/JSON config |
| `POST /validate/csv`    | Validate CSV file |
| `POST /validate/db`     | Validate SQL database table |

**Quick test:**
```bash
curl https://config-data-validator.onrender.com/health


📖 Table of Contents
✨ Features

🚀 Quick Start

🛠️ Local Development

🧪 Testing

🐳 Docker

☁️ Deployment

🤝 Contributing

📄 License

✨ Features
CLI tool – validate files directly from the terminal

REST API – expose validation logic via FastAPI

Complex config validation – Pydantic schemas with cross‑field rules

CSV validation – required columns, data types, missing values

SQL validation – schema checks and custom SQL conditions

Custom configuration – load validation rules from YAML file

CI/CD pipeline – GitHub Actions runs linting, formatting, tests, and builds Docker image

Dockerized – ready to run anywhere

Deployed – live on Render (free tier)

🚀 Quick Start
Clone and run the CLI:

bash
git clone https://github.com/JeffGcode/config-data-validator.git
cd config-data-validator
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Validate a config file
python -m src.validator.cli --file samples/sample_config.yaml

# Validate a CSV file
python -m src.validator.cli --data-file samples/sample_data.csv

# Validate a SQLite database
python -m src.validator.cli --db-url sqlite:///test.db --table users --condition "age < 18"
Start the API server:

bash
uvicorn src.validator.api:app --reload
Visit http://127.0.0.1:8000/docs for interactive API docs.

🛠️ Local Development
Prerequisites
Python 3.11+

Virtual environment (recommended)

Docker (optional, for containerized runs)

Setup
bash
# Clone and enter directory
git clone https://github.com/JeffGcode/config-data-validator.git
cd config-data-validator

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
Custom Validation Rules
You can override default validation rules by creating a YAML file and passing it with --config. Example:

yaml
# validator_config.yaml
config:
  required_fields:
    - app_name
    - port
  type_checks:
    app_name: str
    port: int
Then run:

bash
python -m src.validator.cli --file config.yaml --config validator_config.yaml
CLI Options
Option	Description
--file	Path to config file (YAML/JSON)
--data-file	Path to CSV file
--db-url	Database URL (e.g., sqlite:///data.db)
--table	Table name to validate
--condition	SQL condition for data validation
--config	Path to custom validation rules YAML
--verbose	Enable debug logging
🧪 Testing
Run the full test suite:

bash
pytest -v
For test coverage:

bash
pip install pytest-cov
pytest --cov=src
🐳 Docker
Build and run with Docker:

bash
docker build -t config-validator .
docker run -p 8000:8000 config-validator
Then visit http://localhost:8000/docs.

☁️ Deployment
The API is automatically deployed to Render on every push to main. It runs inside a Docker container and is publicly accessible.

🤝 Contributing
Contributions are welcome! Please read CONTRIBUTING.md for guidelines on setting up the development environment, code style, and submitting pull requests.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

text

This matches the style you requested (badges, tables, code blocks) and includes all the sections from the improved README. Just copy and paste this into your `README.md` file.