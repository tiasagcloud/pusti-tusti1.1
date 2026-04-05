=============================================
FOLLOW THESE STEPS 
=============================================



To run this project from scratch, someone else should follow these steps in order. This assumes they have Python 3.8+ installed on their system.

1. Clone or Download the Project
Get the project files into a folder (e.g., pusti-tusti1.1).
2. Set Up the Python Virtual Environment
Open a terminal/command prompt in the project root folder.
Run: python -m venv .venv (creates a virtual environment).
Activate it:
Windows: & .venv\Scripts\Activate.ps1 (PowerShell) or activate (CMD).
macOS/Linux: source .venv/bin/activate.
3. Install Python Dependencies
With the venv activated, run: pip install flask opencv-python face-recognition flask-cors qrcode setuptools.
Also install the face recognition models: pip install git+https://github.com/ageitgey/face_recognition_models.
4. Set Up the Database
Run: python backend/setup_student_system.py.
This creates the SQLite database, sample students, and QR codes.
5. Run the Backend (Flask API)
In the terminal (venv activated), run: python backend/app.py.
It will start on http://localhost:5000.
6. Run the Frontend (Web Interface)
Open a new terminal, navigate to the project root, and run: cd frontend; python -m http.server 8000.
It will serve the frontend on http://localhost:8000.
7. Access the Application
Open a web browser and go to http://localhost:8000.
The app should load the home page, and you can navigate to verify students, scan QR codes, etc.
Notes:
Ensure camera permissions are granted in the browser for QR/face scanning.
If there are any errors (e.g., missing packages), install them as needed.
The backend must be running for the frontend API calls to work.
For production, use a proper web server instead of the simple HTTP server.
If they encounter issues, they can refer to the troubleshooting steps we went through (e.g., CORS, camera access). Let me know if you need more details!
