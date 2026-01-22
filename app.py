from flask import Flask, render_template, request, redirect, session
import sqlite3
import random
import os

app = Flask(__name__)
app.secret_key = "wincash_super_secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            password TEXT NOT NULL,
            saldo INTEGER DEFAULT 0,
            apuestas INTEGER DEFAULT 0,
            codigo INTEGER
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE usuario=? AND password=?",
            (usuario, password)
        ).fetchone()

        if user:
            session.clear()
            session["user_id"] = user["id"]
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        codigo = random.randint(1000, 9999)

        db = get_db()
        db.execute(
            "INSERT INTO users (usuario, password, saldo, apuestas, codigo) VALUES (?, ?, 0, 0, ?)",
            (usuario, password, codigo)
        )
        db.commit()
        return redirect("/")

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()

    return render_template(
        "dashboard.html",
        usuario=user["usuario"],
        saldo=user["saldo"],
        apuestas=user["apuestas"],
        codigo=user["codigo"]
    )


@app.route("/recargar", methods=["POST"])
def recargar():
    if "user_id" not in session:
        return redirect("/")

    monto = int(request.form["monto"])
    db = get_db()
    db.execute(
        "UPDATE users SET saldo = saldo + ? WHERE id = ?",
        (monto, session["user_id"])
    )
    db.commit()
    return redirect("/dashboard")


@app.route("/retirar", methods=["POST"])
def retirar():
    if "user_id" not in session:
        return redirect("/")

    monto = int(request.form["monto"])
    db = get_db()

    user = db.execute(
        "SELECT saldo FROM users WHERE id=?",
        (session["user_id"],)
    ).fetchone()

    if user["saldo"] >= monto:
        db.execute(
            "UPDATE users SET saldo = saldo - ? WHERE id = ?",
            (monto, session["user_id"])
        )
        db.commit()

    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, debug=True)
