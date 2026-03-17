import pandas as pd
from pathlib import Path
from .exceptions import ValidationError

REQUIRED_COLUMNS = {"id", "email", "age"}

def validate_csv(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise ValidationError(f"CSV file not found: {file_path}")

    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise ValidationError(f"Could not read CSV: {e}")

    # Check required columns
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValidationError(f"Missing columns: {missing}")

    # Check for empty values
    if df.isnull().any().any():
        raise ValidationError("CSV contains missing (NaN) values")

    # Optional: check email format (simple)
    invalid_emails = ~df["email"].str.contains("@", na=False)
    if invalid_emails.any():
        raise ValidationError("Some emails are missing '@'")

    return df
