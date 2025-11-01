import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Users table
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user', 'admin'))
)
""")

# Reports table
c.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    image_path TEXT,
    latitude REAL,
    longitude REAL,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# Add default admin
admin_pass = generate_password_hash("admin123")
try:
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
              ("admin", admin_pass, "admin"))
except sqlite3.IntegrityError:
    pass

conn.commit()
conn.close()
print("✅ Database initialized successfully!")
