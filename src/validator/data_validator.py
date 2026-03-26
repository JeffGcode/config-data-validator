import pandas as pd
from pathlib import Path
from .exceptions import ValidationError

REQUIRED_COLUMNS = {"id", "email", "age"}


def validate_csv(file_path: str) -> pd.DataFrame:
    """
    Validate a CSV file for required columns, missing values, and email format.

    Args:
        file_path: Path to the CSV file.

    Returns:
        DataFrame containing the validated CSV data.

    Raises:
        ValidationError: If the CSV fails any validation rule.
    """
    path = Path(file_path)
    if not path.exists():
        raise ValidationError(f"CSV file not found: {file_path}")

    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise ValidationError(f"Could not read CSV: {e}")

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValidationError(f"CSV is missing required columns: {', '.join(missing)}")

    if df.isnull().any().any():
        raise ValidationError("CSV contains missing (NaN) values")

    invalid_emails = ~df["email"].str.contains("@", na=False)
    if invalid_emails.any():
        raise ValidationError("Some emails are missing '@'")

    return df
