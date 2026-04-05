import sqlite3

conn = sqlite3.connect("student.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    student_name TEXT,
    student_class TEXT,
    student_face TEXT,
    qr_code TEXT
)
""")

conn.commit()
conn.close()

print("✅ Student database created successfully!")