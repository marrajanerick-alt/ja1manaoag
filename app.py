from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")


def init_database():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            contact TEXT NOT NULL,
            sex TEXT NOT NULL,
            civil_status TEXT NOT NULL,
            educational_attainment TEXT NOT NULL,
            father_name TEXT NOT NULL,
            mother_name TEXT NOT NULL,
            employment_status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name", "").strip()
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

    # Check required fields
    if not all([
        name,
        address,
        contact,
        sex,
        civil_status,
        educational_attainment,
        father_name,
        mother_name,
        employment_status
    ]):
        return render_error(
            "Incomplete Information",
            "Please fill in all required fields."
        ), 400

    # Validate Philippine mobile number
    if (
        not contact.isdigit()
        or len(contact) != 10
        or not contact.startswith("9")
    ):
        return render_error(
            "Invalid Contact Number",
            "Please enter a valid Philippine mobile number with 10 digits starting with 9."
        ), 400

    # Add +63 before saving
    contact = "+63" + contact

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        INSERT INTO users (
            name,
            address,
            contact,
            sex,
            civil_status,
            educational_attainment,
            father_name,
            mother_name,
            employment_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        address,
        contact,
        sex,
        civil_status,
        educational_attainment,
        father_name,
        mother_name,
        employment_status
    ))

    conn.commit()
    conn.close()

    return render_success()


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
                    url("/static/background.jpg");

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
                    url("/static/background.jpg");

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


# Required for Render/Gunicorn
init_database()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
