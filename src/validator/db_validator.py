from sqlalchemy import create_engine, inspect, text
from sqlalchemy.pool import NullPool
from .exceptions import ValidationError


def validate_table_schema(
    engine_url: str, table_name: str, required_columns: list
) -> None:
    """
    Check that a table exists and has the required columns.
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


def validate_table_data(
    engine_url: str, table_name: str, condition: str
) -> None:
    """
    Run a SQL condition and raise if any row violates it.
    """
    engine = create_engine(engine_url, poolclass=NullPool)
    with engine.connect() as conn:
        result = conn.execute(
            text(f"SELECT COUNT(*) FROM {table_name} WHERE {condition}")
        )
        count = result.scalar() or 0
        if count > 0:
            raise ValidationError(
                f"{count} rows violate condition: {condition}"
            )
    engine.dispose()
