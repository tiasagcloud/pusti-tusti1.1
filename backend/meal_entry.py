import sqlite3
from datetime import date

def get_today():
    return date.today().strftime("%Y-%m-%d")


def create_entry_if_not_exists(student_id):
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    today = get_today()

    # Check if already exists
    cursor.execute("""
    SELECT * FROM meals WHERE student_id=? AND date=?
    """, (student_id, today))

    record = cursor.fetchone()

    if record:
        conn.close()
        return "EXISTS"

    # Get student info
    cursor.execute("""
    SELECT student_name, student_class FROM students WHERE student_id=?
    """, (student_id,))

    student = cursor.fetchone()

    if not student:
        conn.close()
        return "NOT_FOUND"

    name, student_class = student

    # Insert new record
    cursor.execute("""
    INSERT INTO meals 
    (student_id, student_name, student_class, date, qr_scan, face_recognition)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (student_id, name, student_class, today, "", ""))

    conn.commit()
    conn.close()

    return "CREATED"