import pytest
import sqlite3
from src.validator.db_validator import validate_table_schema, validate_table_data
from src.validator.exceptions import ValidationError


def test_missing_table(tmp_path):
    db = tmp_path / "temp.db"
    url = f"sqlite:///{db}"
    with pytest.raises(ValidationError, match="does not exist"):
        validate_table_schema(url, "nonexistent", [])


def test_missing_columns(tmp_path):
    db = tmp_path / "temp.db"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE users (id INTEGER)")
    conn.commit()
    conn.close()
    url = f"sqlite:///{db}"
    with pytest.raises(ValidationError, match="missing required columns"):
        validate_table_schema(url, "users", ["id", "email"])


def test_violation_condition(tmp_path):
    db = tmp_path / "temp.db"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE users (id INTEGER, age INTEGER)")
    conn.execute("INSERT INTO users VALUES (1, 20), (2, 15)")
    conn.commit()
    conn.close()
    url = f"sqlite:///{db}"
    with pytest.raises(ValidationError, match="1 rows violate"):
        validate_table_data(url, "users", "age < 18")


def test_valid_table(tmp_path):
    db = tmp_path / "temp.db"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE users (id INTEGER, email TEXT, age INTEGER)")
    conn.execute("INSERT INTO users VALUES (1, 'a@b.com', 25)")
    conn.commit()
    conn.close()
    url = f"sqlite:///{db}"
    validate_table_schema(url, "users", ["id", "email", "age"])
    validate_table_data(url, "users", "age < 18")  # Should not raise