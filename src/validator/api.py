from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Corrected imports – alias the conflicting exceptions
from .loader import load_config
from .schema import validate_config as validate_config_schema
from .data_validator import validate_csv
from .exceptions import ValidationError as ConfigValidationError, ConfigLoadError
from .db_validator import validate_table_schema, validate_table_data
from .db_validator import ValidationError as DBValidationError

app = FastAPI(title="Config & Data Validator API")


# --- Request Models ---
class ConfigRequest(BaseModel):
    file_path: str


class DataRequest(BaseModel):
    file_path: str


class DBRequest(BaseModel):
    db_url: str
    table: str
    condition: str | None = None  # Python 3.10+ union syntax


# --- Health Check ---
@app.get("/health")
def health():
    return {"status": "ok"}


# --- Config Validation Endpoint ---
@app.post("/validate/config")
def validate_config_endpoint(req: ConfigRequest):
    try:
        config = load_config(req.file_path)
        validated = validate_config_schema(config)
        return {"valid": True, "config": validated.model_dump()}  # Pydantic v2
    except (ConfigValidationError, FileNotFoundError, ConfigLoadError) as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- CSV Validation Endpoint ---
@app.post("/validate/csv")
def validate_csv_endpoint(req: DataRequest):
    try:
        df = validate_csv(req.file_path)
        return {"valid": True, "rows": len(df)}
    except ConfigValidationError as e:  # Assuming validate_csv raises this
        raise HTTPException(status_code=400, detail=str(e))


# --- Database Validation Endpoint ---
@app.post("/validate/db")
def validate_db_endpoint(req: DBRequest):
    try:
        # You may want to make required columns configurable (e.g., via request body)
        required = ["id", "email"]
        validate_table_schema(req.db_url, req.table, required)
        if req.condition:
            validate_table_data(req.db_url, req.table, req.condition)
        return {"valid": True}
    except DBValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    # Optional: catch database connection errors
    # except Exception as e:
    #     raise HTTPException(status_code=503, detail="Database unavailable")
