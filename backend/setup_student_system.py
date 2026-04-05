import sqlite3
import os
import qrcode
from shutil import copyfile

# -----------------------------
# Configuration
# -----------------------------
DB_FILE = "student.db"
FACES_FOLDER = "faces"
QRCODE_FOLDER = "qrcodes"

# Sample students (replace/add as needed)
students = [
    ("S001", "Tiasa Dutta", "10"),
    ("S002", "Disha", "11"),
    ("S003", "Jayatri", "12")
]

# -----------------------------
# 1. Create database
# -----------------------------
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    student_name TEXT,
    student_class TEXT
)
""")

# Create meals table
cursor.execute("""
CREATE TABLE IF NOT EXISTS meals (
    student_id TEXT,
    student_name TEXT,
    student_class TEXT,
    date TEXT,
    qr_scan TEXT,
    face_recognition TEXT
)
""")

conn.commit()

# -----------------------------
# 2. Insert students
# -----------------------------
for s in students:
    cursor.execute("""
    INSERT OR IGNORE INTO students (student_id, student_name, student_class)
    VALUES (?, ?, ?)
    """, s)

conn.commit()
conn.close()
print(f"Database '{DB_FILE}' created with {len(students)} students.")

# -----------------------------
# 3. Create faces folder if missing
# -----------------------------
if not os.path.exists(FACES_FOLDER):
    os.makedirs(FACES_FOLDER)
    print(f"Created faces folder: {FACES_FOLDER}")
else:
    print(f"Faces folder exists: {FACES_FOLDER}")
print("Place student images in 'faces/' named <student_id>.jpg (e.g., S001.jpg)")

# -----------------------------
# 4. Create QR codes folder & generate QR for each student
# -----------------------------
if not os.path.exists(QRCODE_FOLDER):
    os.makedirs(QRCODE_FOLDER)
    print(f"Created QR code folder: {QRCODE_FOLDER}")

for s in students:
    student_id = s[0]
    qr_path = os.path.join(QRCODE_FOLDER, f"{student_id}.png")
    qr_img = qrcode.make(student_id)
    qr_img.save(qr_path)
print(f"QR codes generated in '{QRCODE_FOLDER}' for all students.")

print("\nSetup complete! Your database, QR codes, and faces folder are ready.")
print("Now run 'python app.py' to start the website.")