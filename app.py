from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# Always use the database inside the project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")


def init_database():
    """Create the users table if it does not already exist."""
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

    father_name = request.form.get(
        "father_name", ""
    ).strip()

    mother_name = request.form.get(
        "mother_name", ""
    ).strip()

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
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">
            <title>Error</title>

            <style>
                body {
                    min-height: 100vh;
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-family: Arial, sans-serif;
                    background: #f8f5f0;
                    color: #4b111f;
                    padding: 20px;
                    box-sizing: border-box;
                }

                .message {
                    width: 100%;
                    max-width: 500px;
                    text-align: center;
                    padding: 40px 25px;
                    background: white;
                    border: 1px solid #d4af37;
                    border-radius: 20px;
                    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
                }

                h2 {
                    margin-bottom: 15px;
                }

                p {
                    color: #555;
                    margin-bottom: 25px;
                }

                a {
                    display: inline-block;
                    padding: 13px 25px;
                    border-radius: 10px;
                    background: #7a1f2b;
                    color: white;
                    text-decoration: none;
                    font-weight: bold;
                }
            </style>
        </head>

        <body>

            <div class="message">
                <h2>Incomplete Information</h2>

                <p>
                    Please fill in all required fields.
                </p>

                <a href="/">
                    Go Back
                </a>
            </div>

        </body>
        </html>
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

    # Success page
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Submitted Successfully</title>

        <style>
            body {
                min-height: 100vh;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: Georgia, serif;
                background:
                    radial-gradient(
                        circle at top left,
                        rgba(122, 31, 43, 0.12),
                        transparent 40%
                    ),
                    radial-gradient(
                        circle at bottom right,
                        rgba(212, 175, 55, 0.18),
                        transparent 40%
                    ),
                    #f8f5f0;
                color: #4b111f;
                padding: 20px;
                box-sizing: border-box;
            }

            .message {
                width: 100%;
                max-width: 500px;
                text-align: center;
                padding: 45px 25px;
                background: rgba(255, 255, 255, 0.92);
                border: 1px solid rgba(212, 175, 55, 0.7);
                border-radius: 25px;
                box-shadow:
                    0 20px 50px rgba(75, 17, 31, 0.15);
                position: relative;
                overflow: hidden;
            }

            .message::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 6px;
                background: linear-gradient(
                    90deg,
                    #6d1726,
                    #d4af37,
                    #6d1726
                );
            }

            .cross {
                font-size: 42px;
                color: #d4af37;
                margin-bottom: 10px;
            }

            h2 {
                margin: 0 0 15px;
                color: #6d1726;
            }

            p {
                color: #666;
                margin-bottom: 28px;
                font-family: Arial, sans-serif;
            }

            a {
                display: inline-block;
                padding: 14px 28px;
                border-radius: 12px;
                background: linear-gradient(
                    135deg,
                    #6d1726,
                    #941f34
                );
                color: white;
                text-decoration: none;
                font-weight: bold;
                font-family: Arial, sans-serif;
                box-shadow:
                    0 8px 20px rgba(109, 23, 38, 0.25);
            }

            a:hover {
                transform: translateY(-2px);
            }
        </style>
    </head>

    <body>

        <div class="message">

            <div class="cross">✝</div>

            <h2>
                Information Submitted Successfully!
            </h2>

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


# IMPORTANT:
# Initialize the database when Flask/Gunicorn starts.
# This is required when deploying to Render.
init_database()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )