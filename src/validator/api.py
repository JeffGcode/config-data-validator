from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from .loader import load_config
from .schema import validate_config as validate_config_schema
from .data_validator import validate_csv
from .db_validator import validate_table_schema, validate_table_data
from .exceptions import ValidationError, ConfigLoadError

# ---------- Logging Configuration ----------
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Config & Data Validator API")


# ---------- Request Models ----------
class ConfigRequest(BaseModel):
    file_path: str


class DataRequest(BaseModel):
    file_path: str


class DBRequest(BaseModel):
    db_url: str
    table: str
    condition: str | None = None


# ---------- Health Check ----------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------- Config Validation Endpoint ----------
@app.post("/validate/config")
def validate_config_endpoint(req: ConfigRequest):
    try:
        config = load_config(req.file_path)
        validated = validate_config_schema(config)
        return {"valid": True, "config": validated.model_dump()}
    except (ValidationError, ConfigLoadError, FileNotFoundError) as e:
        logger.error(f"Config validation failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ---------- CSV Validation Endpoint ----------
@app.post("/validate/csv")
def validate_csv_endpoint(req: DataRequest):
    try:
        df = validate_csv(req.file_path)
        return {"valid": True, "rows": len(df)}
    except ValidationError as e:
        logger.error(f"CSV validation failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ---------- Database Validation Endpoint ----------
@app.post("/validate/db")
def validate_db_endpoint(req: DBRequest):
    try:
        required = ["id", "email"]
        validate_table_schema(req.db_url, req.table, required)
        if req.condition:
            validate_table_data(req.db_url, req.table, req.condition)
        return {"valid": True}
    except ValidationError as e:
        logger.error(f"Database validation failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
