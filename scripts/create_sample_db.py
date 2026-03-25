#!/usr/bin/env python3
"""
Create a sample SQLite database for testing the Config & Data Validator.
Run this script once to generate sample.db.
"""

import sqlite3
import os
from pathlib import Path

def create_sample_db():
    db_path = Path(__file__).parent.parent / "sample.db"
    print(f"Creating sample database at: {db_path}")

    # Remove existing if present (optional)
    if db_path.exists():
        print(f"Removing existing {db_path}")
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL
        )
    ''')

    # Insert some users
    users_data = [
        (1, "alice@example.com", 25),
        (2, "bob@domain.com", 30),
        (3, "charlie@test.org", 17),   # underage
        (4, "diana@example.com", 22),
        (5, "eve@company.net", 19)
    ]
    cursor.executemany("INSERT INTO users (id, email, age) VALUES (?, ?, ?)", users_data)

    # Create orders table (additional table to demonstrate validation)
    cursor.execute('''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    orders_data = [
        (101, 1, 49.99),
        (102, 2, 19.95),
        (103, 3, 5.99),
        (104, 1, 12.50)
    ]
    cursor.executemany(
        "INSERT INTO orders (order_id, user_id, amount) VALUES (?, ?, ?)",
        orders_data
    )

    conn.commit()
    conn.close()

    print("Sample database created successfully.")
    print("Tables: users, orders")
    print(f"Location: {db_path}")

if __name__ == "__main__":
    create_sample_db()