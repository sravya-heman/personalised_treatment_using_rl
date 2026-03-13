import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS patient_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    disease TEXT,
    symptoms TEXT,
    report_path TEXT,
    treatment TEXT,
    severity TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    rating INTEGER,
    comment TEXT
)
""")

conn.commit()
conn.close()
print("Database updated successfully")
