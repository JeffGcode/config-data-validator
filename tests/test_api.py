from fastapi.testclient import TestClient
from src.validator.api import app
import tempfile
import os
import sqlite3
import shutil
import time

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_validate_config_valid():
    response = client.post("/validate/config", json={"file_path": "samples/sample_config.yaml"})
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert "config" in data

def test_validate_config_invalid_file():
    response = client.post("/validate/config", json={"file_path": "nonexistent.yaml"})
    assert response.status_code == 400

def test_validate_csv_valid():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("id,email,age\n1,test@test.com,30\n2,user@domain.com,25")
        tmp_path = f.name
    try:
        response = client.post("/validate/csv", json={"file_path": tmp_path})
        assert response.status_code == 200
        assert response.json()["valid"] is True
        assert response.json()["rows"] == 2
    finally:
        os.unlink(tmp_path)

def test_validate_csv_missing_columns():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("id,name\n1,Alice")
        tmp_path = f.name
    try:
        response = client.post("/validate/csv", json={"file_path": tmp_path})
        assert response.status_code == 400
        # Updated assertion to match improved error message
        assert "missing required columns" in response.json()["detail"].lower()
    finally:
        os.unlink(tmp_path)

def test_validate_db_valid():
    tmp_dir = tempfile.mkdtemp()
    try:
        db_path = os.path.join(tmp_dir, "test.db")
        db_url = f"sqlite:///{db_path}"
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE users (id INTEGER, email TEXT, age INTEGER)")
        conn.execute("INSERT INTO users VALUES (1, 'a@b.com', 25)")
        conn.commit()
        conn.close()
        response = client.post("/validate/db", json={
            "db_url": db_url,
            "table": "users",
            "condition": None
        })
        assert response.status_code == 200
        assert response.json()["valid"] is True
    finally:
        for _ in range(5):
            try:
                shutil.rmtree(tmp_dir)
                break
            except PermissionError:
                time.sleep(0.1)

def test_validate_db_condition_fails():
    tmp_dir = tempfile.mkdtemp()
    try:
        db_path = os.path.join(tmp_dir, "test.db")
        db_url = f"sqlite:///{db_path}"
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE users (id INTEGER, email TEXT, age INTEGER)")
        conn.execute("INSERT INTO users VALUES (1, 'a@b.com', 20), (2, 'b@b.com', 15)")
        conn.commit()
        conn.close()
        response = client.post("/validate/db", json={
            "db_url": db_url,
            "table": "users",
            "condition": "age < 18"
        })
        assert response.status_code == 400
        assert "rows violate condition" in response.json()["detail"]
    finally:
        for _ in range(5):
            try:
                shutil.rmtree(tmp_dir)
                break
            except PermissionError:
                time.sleep(0.1)