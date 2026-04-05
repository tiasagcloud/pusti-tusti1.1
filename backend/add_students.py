import sqlite3
import qrcode
import os

# Connect DB
conn = sqlite3.connect("student.db")
cursor = conn.cursor()

# Sample student data (you can change)
students = [
    ("S001", "Tiasa Dutta", "10A"),
    ("S002", "Disha ", "9B"),
    ("S003", "Ankita Roy", "8C")
]

# Ensure QR folder exists
os.makedirs("../qr_codes", exist_ok=True)

for student in students:
    student_id, name, student_class = student

    # Generate QR
    qr_data = student_id
    qr_img = qrcode.make(qr_data)

    qr_path = f"../qr_codes/{student_id}.png"
    qr_img.save(qr_path)

    # Insert into DB
    cursor.execute("""
    INSERT OR REPLACE INTO students
    (student_id, student_name, student_class, student_face, qr_code)
    VALUES (?, ?, ?, ?, ?)
    """, (student_id, name, student_class, "", qr_path))

conn.commit()
conn.close()

print("✅ Students added and QR codes generated!")