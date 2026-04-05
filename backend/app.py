from flask import Flask, request, jsonify
import sqlite3
from datetime import date
import face_recognition
import cv2
import numpy as np
from pyzbar import pyzbar
import os

app = Flask(__name__)

# -------------------------
# Config: Change this to False if using phone upload
USE_LAPTOP_CAMERA = True

# -------------------------
# Helper Functions
# -------------------------

def get_today():
    return date.today().strftime("%Y-%m-%d")

def get_db_connection():
    return sqlite3.connect("student.db")

# -------------------------
# QR SCAN (Laptop camera)
# -------------------------
def scan_qr_from_camera():
    cap = cv2.VideoCapture(0)  # Laptop camera
    student_id = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        qrcodes = pyzbar.decode(frame)
        for qr in qrcodes:
            student_id = qr.data.decode("utf-8")
            cap.release()
            cv2.destroyAllWindows()
            return student_id
        cv2.imshow("QR Scan - Press Q to exit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return student_id

# -------------------------
# Face Matching Helper
# -------------------------
def match_face(uploaded_image_path, student_image_path):
    unknown_image = face_recognition.load_image_file(uploaded_image_path)
    known_image = face_recognition.load_image_file(student_image_path)

    unknown_encodings = face_recognition.face_encodings(unknown_image)
    known_encodings = face_recognition.face_encodings(known_image)

    if len(unknown_encodings) == 0 or len(known_encodings) == 0:
        return False  # No face detected

    match = face_recognition.compare_faces([known_encodings[0]], unknown_encodings[0])
    return match[0]

# -------------------------
# QR SCAN API
# -------------------------
@app.route("/scan_qr", methods=["POST"])
def scan_qr():
    if USE_LAPTOP_CAMERA:
        student_id = scan_qr_from_camera()
        if not student_id:
            return jsonify({"status": "error", "message": "QR Scan failed"})
    else:
        data = request.json
        student_id = data.get("student_id")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
    student = cursor.fetchone()
    if not student:
        conn.close()
        return jsonify({"status": "error", "message": "Invalid Student"})

    today = get_today()
    cursor.execute("SELECT * FROM meals WHERE student_id=? AND date=?", (student_id, today))
    meal = cursor.fetchone()

    if meal:
        if meal[4] == "Done":  # qr_scan column
            conn.close()
            return jsonify({"status": "error", "message": "Student already entered"})
    else:
        cursor.execute("""
            INSERT INTO meals 
            (student_id, student_name, student_class, date, qr_scan, face_recognition)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student[0], student[1], student[2], today, "", ""))
        conn.commit()

    conn.close()
    return jsonify({
        "status": "success",
        "student_id": student[0],
        "name": student[1],
        "class": student[2]
    })

# -------------------------
# APPROVE QR ENTRY
# -------------------------
@app.route("/approve_qr", methods=["POST"])
def approve_qr():
    data = request.json
    student_id = data.get("student_id")

    conn = get_db_connection()
    cursor = conn.cursor()
    today = get_today()

    cursor.execute("SELECT qr_scan FROM meals WHERE student_id=? AND date=?", (student_id, today))
    record = cursor.fetchone()

    if not record:
        conn.close()
        return jsonify({"status": "error", "message": "No entry found"})
    if record[0] == "Done":
        conn.close()
        return jsonify({"status": "error", "message": "Already marked"})

    cursor.execute("UPDATE meals SET qr_scan='Done' WHERE student_id=? AND date=?", (student_id, today))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "QR Entry Approved"})

# -------------------------
# FACE SCAN API
# -------------------------
@app.route("/scan_face", methods=["POST"])
def scan_face():
    if USE_LAPTOP_CAMERA:
        # Laptop camera simulation: we just check the student_id
        data = request.json
        student_id = data.get("student_id")
    else:
        # Phone upload
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file uploaded"})
        file = request.files['file']
        uploaded_path = f"temp_{file.filename}"
        file.save(uploaded_path)
        student_id = request.form.get("student_id")

    conn = get_db_connection()
    cursor = conn.cursor()
    today = get_today()

    # Check QR first
    cursor.execute("SELECT qr_scan FROM meals WHERE student_id=? AND date=?", (student_id, today))
    record = cursor.fetchone()
    if not record or record[0] == "":
        conn.close()
        if not USE_LAPTOP_CAMERA: os.remove(uploaded_path)
        return jsonify({"status": "error", "message": "Please scan QR first"})

    # Check student exists
    cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
    student = cursor.fetchone()
    if not student:
        conn.close()
        if not USE_LAPTOP_CAMERA: os.remove(uploaded_path)
        return jsonify({"status": "error", "message": "Student not found"})

    if USE_LAPTOP_CAMERA:
        match = True  # Just simulate for laptop
    else:
        student_face_path = f"faces/{student_id}.jpg"
        if not os.path.exists(student_face_path):
            conn.close()
            os.remove(uploaded_path)
            return jsonify({"status": "error", "message": "Student face image not found"})
        match = match_face(uploaded_path, student_face_path)
        os.remove(uploaded_path)

    if not match:
        conn.close()
        return jsonify({"status": "error", "message": "Face does not match"})

    conn.close()
    return jsonify({
        "status": "success",
        "student_id": student[0],
        "name": student[1],
        "class": student[2]
    })

# -------------------------
# APPROVE FACE
# -------------------------
@app.route("/approve_face", methods=["POST"])
def approve_face():
    data = request.json
    student_id = data.get("student_id")

    conn = get_db_connection()
    cursor = conn.cursor()
    today = get_today()

    cursor.execute("SELECT face_recognition FROM meals WHERE student_id=? AND date=?", (student_id, today))
    record = cursor.fetchone()

    if not record:
        conn.close()
        return jsonify({"status": "error", "message": "No record found"})
    if record[0] == "Meal Approved":
        conn.close()
        return jsonify({"status": "error", "message": "Already allocated"})

    cursor.execute("UPDATE meals SET face_recognition='Meal Approved' WHERE student_id=? AND date=?", (student_id, today))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Meal Allocated"})

# -------------------------
# GET ALL STUDENTS
# -------------------------
@app.route("/get_students", methods=["GET"])
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, student_name, student_class FROM students")
    students = cursor.fetchall()
    conn.close()
    data = [{"id": s[0], "name": s[1], "class": s[2]} for s in students]
    return jsonify(data)

# -------------------------
# GET MEAL DATA
# -------------------------
@app.route("/get_meals", methods=["GET"])
def get_meals():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT student_id, student_name, student_class, date, qr_scan, face_recognition
        FROM meals
        ORDER BY date DESC
    """)
    meals = cursor.fetchall()
    conn.close()
    data = [{"id": m[0], "name": m[1], "class": m[2], "date": m[3], "qr": m[4], "face": m[5]} for m in meals]
    return jsonify(data)

# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)






