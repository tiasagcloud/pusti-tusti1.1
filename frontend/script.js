function go(page) {
    window.location.href = page;
}

// QR Scan
function scanQR() {
    let id = document.getElementById("student_id").value;

    fetch("http://127.0.0.1:5000/scan_qr", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ student_id: id })
    })
    .then(res => res.json())
    .then(data => {
        localStorage.setItem("data", JSON.stringify(data));
        localStorage.setItem("mode", "qr");
        window.location.href = "result.html";
    });
}

// Face Scan
function scanFace() {
    let id = document.getElementById("student_id").value;

    fetch("http://127.0.0.1:5000/scan_face", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ student_id: id })
    })
    .then(res => res.json())
    .then(data => {
        localStorage.setItem("data", JSON.stringify(data));
        localStorage.setItem("mode", "face");
        window.location.href = "result.html";
    });
}

// LOAD RESULT PAGE
if (document.getElementById("status")) {

    let data = JSON.parse(localStorage.getItem("data"));
    let mode = localStorage.getItem("mode");

    let status = document.getElementById("status");
    let details = document.getElementById("studentDetails");
    let buttons = document.getElementById("actionButtons");

    if (data.status === "error") {
        status.innerText = data.message;
        return;
    }

    status.innerText = "Student Found";

    details.innerText =
        "ID: " + data.student_id +
        " | Name: " + data.name +
        " | Class: " + data.class;

    // QR MODE
    if (mode === "qr") {
        buttons.innerHTML = `
            <button onclick="approveQR('${data.student_id}')">Approve Entry</button>
            <button onclick="cancel()">Cancel</button>
        `;
    }

    // FACE MODE
    if (mode === "face") {
        buttons.innerHTML = `
            <button onclick="approveFace('${data.student_id}')">Allocate Meal</button>
            <button onclick="cancel()">Cancel</button>
        `;
    }
}

// Approve QR
function approveQR(id) {
    fetch("http://127.0.0.1:5000/approve_qr", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ student_id: id })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        go("qr_scan.html");
    });
}

// Approve Face
function approveFace(id) {
    fetch("http://127.0.0.1:5000/approve_face", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ student_id: id })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        go("face_scan.html");
    });
}

// Cancel
function cancel() {
    alert("Action Cancelled");
    go("verify.html");
}