# THIS FILE IS NOT NEEDED INSTEAD USE setup_student_system.py


import sqlite3

conn = sqlite3.connect("student.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    student_name TEXT,
    student_class TEXT,
    date TEXT,
    qr_scan TEXT,
    face_recognition TEXT
)
""")

conn.commit()
conn.close()

print("✅ Meal database created successfully!")
