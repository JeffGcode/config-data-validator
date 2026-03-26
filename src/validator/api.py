"""
FastAPI application for the Config & Data Validator.
Exposes validation endpoints for configuration files, CSV data, and database tables.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .loader import load_config
from .schema import validate_config as validate_config_schema
from .data_validator import validate_csv
from .db_validator import validate_table_schema, validate_table_data
from .exceptions import ConfigLoadError, ValidationError
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Config & Data Validator API")


# ---------- Request Models ----------
class ConfigRequest(BaseModel):
    """Request model for config validation."""

    file_path: str


class DataRequest(BaseModel):
    """Request model for CSV validation."""

    file_path: str


class DBRequest(BaseModel):
    """Request model for database validation."""

    db_url: str
    table: str
    condition: str | None = None


# ---------- Endpoints ----------
@app.get("/health")
def health() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: {"status": "ok"}
    """
    return {"status": "ok"}


@app.post("/validate/config")
def validate_config_endpoint(req: ConfigRequest) -> dict:
    """
    Validate a configuration file (YAML/JSON) using Pydantic schema.

    Args:
        req: ConfigRequest containing the file path.

    Returns:
        dict: {"valid": True, "config": validated_config}

    Raises:
        HTTPException: 400 if validation fails or file not found.
    """
    try:
        config = load_config(req.file_path)
        validated = validate_config_schema(config)
        logger.info(f"Config validation succeeded for {req.file_path}")
        return {"valid": True, "config": validated.model_dump()}
    except (ValidationError, ConfigLoadError, FileNotFoundError) as e:
        logger.error(f"Config validation failed for {req.file_path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/validate/csv")
def validate_csv_endpoint(req: DataRequest) -> dict:
    """
    Validate a CSV file for required columns, missing values, and email format.

    Args:
        req: DataRequest containing the file path.

    Returns:
        dict: {"valid": True, "rows": number_of_rows}

    Raises:
        HTTPException: 400 if validation fails.
    """
    try:
        df = validate_csv(req.file_path)
        logger.info(f"CSV validation succeeded for {req.file_path}")
        return {"valid": True, "rows": len(df)}
    except ValidationError as e:
        logger.error(f"CSV validation failed for {req.file_path}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/validate/db")
def validate_db_endpoint(req: DBRequest) -> dict:
    """
    Validate a database table's schema and optional data condition.

    Args:
        req: DBRequest containing database URL, table name, and optional SQL condition.

    Returns:
        dict: {"valid": True}

    Raises:
        HTTPException: 400 if validation fails.
    """
    try:
        # Default required columns – could be made configurable later
        required = ["id", "email"]
        validate_table_schema(req.db_url, req.table, required)
        if req.condition:
            validate_table_data(req.db_url, req.table, req.condition)
        logger.info(f"Database validation succeeded for {req.table}")
        return {"valid": True}
    except ValidationError as e:
        logger.error(f"Database validation failed for {req.table}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
