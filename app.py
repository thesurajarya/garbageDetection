from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os, uuid

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
DB_PATH = "database.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- AUTH ROUTES ---------------- #
@app.route('/')
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard" if session["role"] == "admin" else "index"))
    return redirect(url_for("login"))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed = generate_password_hash(password)
        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                         (username, hashed, "user"))
            conn.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "Username already exists!"
    return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard" if user["role"] == "admin" else "index"))
        return "Invalid credentials!"
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- USER ROUTES ---------------- #
@app.route('/index')
def index():
    if "user_id" not in session or session["role"] != "user":
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if "user_id" not in session or session["role"] != "user":
        return redirect(url_for("login"))

    if request.method == "POST":
        image = request.files["image"]
        lat = request.form["latitude"]
        lon = request.form["longitude"]

        if image:
            filename = f"{uuid.uuid4().hex}_{image.filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            image.save(filepath)

            conn = get_db()
            conn.execute("INSERT INTO reports (user_id, image_path, latitude, longitude) VALUES (?, ?, ?, ?)",
                         (session["user_id"], filepath, lat, lon))
            conn.commit()
            conn.close()

            return "✅ Report submitted successfully!"

    return render_template("upload.html")

# ---------------- ADMIN ROUTES ---------------- #
@app.route('/dashboard')
def dashboard():
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("login"))
    conn = get_db()
    reports = conn.execute("SELECT * FROM reports").fetchall()
    return render_template("dashboard.html", reports=reports)

if __name__ == "__main__":
    app.run(debug=True)
