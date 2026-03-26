from sqlalchemy import create_engine, inspect, text
from sqlalchemy.pool import NullPool
from .exceptions import ValidationError


def validate_table_schema(
    engine_url: str, table_name: str, required_columns: list
) -> None:
    """
    Check that a database table exists and contains all required columns.

    Args:
        engine_url: SQLAlchemy database URL (e.g., sqlite:///data.db).
        table_name: Name of the table to validate.
        required_columns: List of column names that must be present.

    Raises:
        ValidationError: If table missing or required columns missing.
    """
    engine = create_engine(engine_url, poolclass=NullPool)
    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        raise ValidationError(f"Table '{table_name}' does not exist")

    columns = [col["name"] for col in inspector.get_columns(table_name)]
    missing = set(required_columns) - set(columns)
    if missing:
        raise ValidationError(
            f"Table '{table_name}' is missing required columns: {', '.join(missing)}"
        )
    engine.dispose()


def validate_table_data(engine_url: str, table_name: str, condition: str) -> None:
    """
    Run a SQL condition and raise if any row violates it.

    Args:
        engine_url: SQLAlchemy database URL.
        table_name: Name of the table.
        condition: SQL WHERE clause condition (e.g., "age < 18").

    Raises:
        ValidationError: If any rows satisfy the condition (i.e., bad data).
    """
    engine = create_engine(engine_url, poolclass=NullPool)
    with engine.connect() as conn:
        result = conn.execute(
            text(f"SELECT COUNT(*) FROM {table_name} WHERE {condition}")
        )
        count = result.scalar() or 0
        if count > 0:
            raise ValidationError(f"{count} rows violate condition: {condition}")
    engine.dispose()
