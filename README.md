# Config & Data Validator

A Python‑based validation service that checks configuration files (YAML/JSON), CSV data, and SQL database schemas.  
Built with FastAPI, Pydantic, SQLAlchemy, and Docker.

[![CI Pipeline](https://github.com/JeffGcode/config-data-validator/actions/workflows/ci.yml/badge.svg)](https://github.com/JeffGcode/config-data-validator/actions/workflows/ci.yml)

---

## 🚀 Live API

The service is deployed at:  
[https://config-data-validator.onrender.com](https://config-data-validator.onrender.com)

**Note:** The root URL (`/`) returns `{"detail":"Not Found"}` – this is intentional. Use the endpoints below.

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check (returns `{"status":"ok"}`) |
| `GET /docs`   | Interactive Swagger UI for testing |
| `POST /validate/config` | Validate a YAML/JSON config file |
| `POST /validate/csv`    | Validate a CSV file |
| `POST /validate/db`     | Validate a SQL database table |

### Quick test

```bash
# Health check
curl https://config-data-validator.onrender.com/health

# Validate a config file (example uses a sample file inside the Docker image)
curl -X POST https://config-data-validator.onrender.com/validate/config \
  -H "Content-Type: application/json" \
  -d '{"file_path": "samples/sample_config.yaml"}'

## Features

- YAML config loading
- JSON schema validation
- CLI interface
- Automated tests
- GitHub Actions CI pipeline

## Usage

python -m validator.cli samples/config.yaml samples/schema.json

## Run Tests

pytest
