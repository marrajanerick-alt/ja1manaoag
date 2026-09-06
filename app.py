from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)

app.secret_key = "manaoag-admin-secret-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")


def init_database():

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            nickname TEXT,
            age INTEGER,
            date_of_birth TEXT,
            address TEXT NOT NULL,
            contact TEXT NOT NULL,
            sex TEXT NOT NULL,
            civil_status TEXT NOT NULL,
            educational_attainment TEXT NOT NULL,
            father_name TEXT NOT NULL,
            mother_name TEXT NOT NULL,
            employment_status TEXT NOT NULL,
            baptized TEXT,
            christian_duration TEXT,
            skills TEXT
        )
    """)

    # Add new columns to an existing database
    existing_columns = [
        row[1]
        for row in conn.execute("PRAGMA table_info(users)").fetchall()
    ]

    new_columns = {
        "nickname": "TEXT",
        "age": "INTEGER",
        "date_of_birth": "TEXT",
        "baptized": "TEXT",
        "christian_duration": "TEXT",
        "skills": "TEXT"
    }

    for column, data_type in new_columns.items():

        if column not in existing_columns:

            conn.execute(
                f"ALTER TABLE users ADD COLUMN {column} {data_type}"
            )

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name", "").strip()
    nickname = request.form.get("nickname", "").strip()
    age = request.form.get("age", "").strip()
    date_of_birth = request.form.get("date_of_birth", "").strip()

    address = request.form.get("address", "").strip()
    contact = request.form.get("contact", "").strip()
    sex = request.form.get("sex", "").strip()
    civil_status = request.form.get("civil_status", "").strip()

    educational_attainment = request.form.get(
        "educational_attainment", ""
    ).strip()

    father_name = request.form.get(
        "father_name", ""
    ).strip()

    mother_name = request.form.get(
        "mother_name", ""
    ).strip()

    employment_status = request.form.get(
        "employment_status", ""
    ).strip()

    baptized = request.form.get(
        "baptized", ""
    ).strip()

    christian_duration = request.form.get(
        "christian_duration", ""
    ).strip()

    skills = request.form.get(
        "skills", ""
    ).strip()


    # Check required fields

    if not all([
        name,
        nickname,
        age,
        date_of_birth,
        address,
        contact,
        sex,
        civil_status,
        educational_attainment,
        father_name,
        mother_name,
        employment_status,
        baptized,
        christian_duration,
        skills
    ]):

        return render_error(
            "Incomplete Information",
            "Please fill in all required fields."
        ), 400


    # Age must be an integer

    try:

        age = int(age)

    except ValueError:

        return render_error(
            "Invalid Age",
            "Age must be a whole number."
        ), 400


    if age < 1 or age > 120:

        return render_error(
            "Invalid Age",
            "Please enter a valid age."
        ), 400


    # Philippine mobile number validation

    if (
        not contact.isdigit()
        or len(contact) != 10
        or not contact.startswith("9")
    ):

        return render_error(
            "Invalid Contact Number",
            "Please enter a valid Philippine mobile number with 10 digits starting with 9."
        ), 400


    contact = "+63" + contact


    # Save information

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        INSERT INTO users (
            name,
            nickname,
            age,
            date_of_birth,
            address,
            contact,
            sex,
            civil_status,
            educational_attainment,
            father_name,
            mother_name,
            employment_status,
            baptized,
            christian_duration,
            skills
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        name,
        nickname,
        age,
        date_of_birth,
        address,
        contact,
        sex,
        civil_status,
        educational_attainment,
        father_name,
        mother_name,
        employment_status,
        baptized,
        christian_duration,
        skills

    ))

    conn.commit()
    conn.close()


    return render_success()


# =========================
# ADMIN LOGIN
# =========================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == "admin" and password == "@Manaoag21":

            session["admin_logged_in"] = True

            return redirect(url_for("admin_dashboard"))

        return render_template(
            "admin_login.html",
            error="Invalid username or password."
        )

    return render_template("admin_login.html")


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get("admin_logged_in"):

        return redirect(url_for("admin"))


    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    users = conn.execute("""
        SELECT *
        FROM users
        ORDER BY id DESC
    """).fetchall()

    conn.close()


    return render_template(
        "admin_dashboard.html",
        users=users
    )


# =========================
# DELETE USER
# =========================

@app.route("/admin/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):

    if not session.get("admin_logged_in"):

        return redirect(url_for("admin"))


    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()


    return redirect(url_for("admin_dashboard"))


# =========================
# LOGOUT
# =========================

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect(url_for("admin"))


# =========================
# ERROR PAGE
# =========================

def render_error(title, message):

    return f"""
    <!DOCTYPE html>

    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0">

        <title>{title}</title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;

                min-height: 100vh;

                display: flex;

                justify-content: center;

                align-items: center;

                padding: 20px;

                font-family: Arial, sans-serif;

                background:
                    linear-gradient(
                        rgba(255,255,255,0.88),
                        rgba(255,255,255,0.88)
                    ),
                    url("/static/14fbb570668080d5d5952ab7b710bcf7 (1).jpg");

                background-size: cover;

                background-position: center;

                color: #333;
            }}

            .card {{
                width: 100%;

                max-width: 430px;

                padding: 40px 25px;

                text-align: center;

                background: rgba(255,255,255,0.95);

                border: 1px solid #eeeeee;

                border-radius: 18px;

                box-shadow:
                    0 10px 35px rgba(0,0,0,0.08);
            }}

            .icon {{
                width: 65px;

                height: 65px;

                margin: 0 auto 20px;

                border-radius: 50%;

                display: flex;

                align-items: center;

                justify-content: center;

                background: #b83b5e;

                color: white;

                font-size: 32px;

                font-weight: bold;
            }}

            h1 {{
                margin: 0 0 10px;

                color: #8f2948;

                font-size: 24px;
            }}

            p {{
                margin: 0;

                color: #777;

                line-height: 1.6;

                font-size: 14px;
            }}

            a {{
                display: inline-block;

                margin-top: 25px;

                padding: 12px 24px;

                border-radius: 10px;

                background: #b83b5e;

                color: white;

                text-decoration: none;

                font-size: 14px;

                font-weight: 600;
            }}

            a:hover {{
                background: #8f2948;
            }}

        </style>

    </head>

    <body>

        <div class="card">

            <div class="icon">!</div>

            <h1>{title}</h1>

            <p>{message}</p>

            <a href="/">Go Back</a>

        </div>

    </body>

    </html>
    """


# =========================
# SUCCESS PAGE
# =========================

def render_success():

    return """
    <!DOCTYPE html>

    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0">

        <title>Information Submitted</title>

        <style>

            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;

                min-height: 100vh;

                display: flex;

                justify-content: center;

                align-items: center;

                padding: 20px;

                font-family: Arial, sans-serif;

                background:
                    linear-gradient(
                        rgba(255,255,255,0.88),
                        rgba(255,255,255,0.88)
                    ),
                    url("/static/14fbb570668080d5d5952ab7b710bcf7 (1).jpg");

                background-size: cover;

                background-position: center;

                color: #333;
            }

            .card {
                width: 100%;

                max-width: 430px;

                padding: 40px 25px;

                text-align: center;

                background: rgba(255,255,255,0.95);

                border: 1px solid #eeeeee;

                border-radius: 18px;

                box-shadow:
                    0 10px 35px rgba(0,0,0,0.08);
            }

            .icon {
                width: 65px;

                height: 65px;

                margin: 0 auto 20px;

                border-radius: 50%;

                display: flex;

                align-items: center;

                justify-content: center;

                background: #b83b5e;

                color: white;

                font-size: 32px;

                font-weight: bold;
            }

            h1 {
                margin: 0 0 10px;

                color: #8f2948;

                font-size: 24px;
            }

            p {
                margin: 0;

                color: #777;

                line-height: 1.6;

                font-size: 14px;
            }

            a {
                display: inline-block;

                margin-top: 25px;

                padding: 12px 24px;

                border-radius: 10px;

                background: #b83b5e;

                color: white;

                text-decoration: none;

                font-size: 14px;

                font-weight: 600;
            }

            a:hover {
                background: #8f2948;
            }

        </style>

    </head>

    <body>

        <div class="card">

            <div class="icon">✓</div>

            <h1>Information Submitted</h1>

            <p>
                Your personal information has been successfully recorded.
            </p>

            <a href="/">Submit Another</a>

        </div>

    </body>

    </html>
    """


# Initialize database
init_database()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
