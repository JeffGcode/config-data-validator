import sqlite3
conn = sqlite3.connect('test.db')
conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, age INTEGER)')
conn.execute("INSERT INTO users VALUES (1, 'alice@example.com', 25), (2, 'bob@domain.com', 17)")
conn.commit()
conn.close()
print('Created test.db with users table')
