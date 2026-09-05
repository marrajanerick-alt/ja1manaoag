from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# Always use the database inside the mywebsite folder
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

    # Get information from the form
    name = request.form.get("name", "").strip()
    address = request.form.get("address", "").strip()
    contact = request.form.get("contact", "").strip()
    sex = request.form.get("sex", "").strip()
    civil_status = request.form.get("civil_status", "").strip()
    educational_attainment = request.form.get(
        "educational_attainment", ""
    ).strip()
    father_name = request.form.get("father_name", "").strip()
    mother_name = request.form.get("mother_name", "").strip()
    employment_status = request.form.get(
        "employment_status", ""
    ).strip()

    # Check if all fields are filled
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
        return """
        <h2>Error</h2>
        <p>Please fill in all required fields.</p>
        <a href="/">Go back</a>
        """, 400

    # Save information to SQLite database
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

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Submitted</title>

        <style>
            body {
                min-height: 100vh;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
                background:
                    radial-gradient(
                        circle at top left,
                        #4facfe,
                        transparent 40%
                    ),
                    radial-gradient(
                        circle at bottom right,
                        #00f2fe,
                        transparent 40%
                    ),
                    linear-gradient(
                        135deg,
                        #0f172a,
                        #1e293b
                    );
                color: white;
                padding: 20px;
                box-sizing: border-box;
            }

            .message {
                width: 100%;
                max-width: 500px;
                text-align: center;
                padding: 40px 25px;
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 25px;
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
            }

            h2 {
                margin-bottom: 15px;
            }

            p {
                color: rgba(255, 255, 255, 0.75);
                margin-bottom: 25px;
            }

            a {
                display: inline-block;
                padding: 13px 25px;
                border-radius: 12px;
                background: linear-gradient(
                    135deg,
                    #38bdf8,
                    #6366f1
                );
                color: white;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>

    <body>

        <div class="message">
            <h2>Information Submitted Successfully!</h2>

            <p>
                Your information has been saved to the database.
            </p>

            <a href="/">
                Submit Another
            </a>
        </div>

    </body>
    </html>
    """


if __name__ == "__main__":
    init_database()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )