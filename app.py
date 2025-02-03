from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this for security

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="6himalaya",
        database="hospital_db"
    )

# Hash password before storing
def hash_password(plain_text_password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_text_password.encode("utf-8"), salt).decode("utf-8")

# General Login Route (For all users)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode("utf-8")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, password, role FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            stored_hashed_password = user[1]
            
            if bcrypt.checkpw(password, stored_hashed_password.encode("utf-8")):
                session["user_id"] = user[0]
                session["role"] = user[2]
                
                if user[2] == "super_admin":
                    return redirect("/admin")
                elif user[2] == "doctor":
                    return redirect("/doctor")
                elif user[2] == "patient":
                    return redirect("/patient")
        
        flash("Invalid Credentials", "error")
        return redirect("/")
    
    return render_template("login.html")

# Separate Patient Login Route
@app.route("/patient_login", methods=["GET", "POST"])
def patient_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode("utf-8")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, password FROM Users WHERE username = %s AND role = 'patient'", (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            stored_hashed_password = user[1]
            if bcrypt.checkpw(password, stored_hashed_password.encode("utf-8")):
                session["user_id"] = user[0]
                session["role"] = "patient"
                return redirect("/patient")
        
        flash("Invalid Patient Credentials", "error")
        return redirect("/patient_login")
    
    return render_template("patient_login.html")

# Super Admin Dashboard
@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "super_admin":
        return redirect("/")
    return render_template("admin.html")

# Doctor Dashboard
@app.route("/doctor")
def doctor_dashboard():
    if session.get("role") != "doctor":
        return redirect("/")
    return render_template("doctor.html")

# Patient Dashboard
@app.route("/patient")
def patient_dashboard():
    if session.get("role") != "patient":
        return redirect("/")
    return render_template("patient.html")

if __name__ == "__main__":
    app.run(debug=True)
