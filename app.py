from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# =================================
# DATABASE
# =================================

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


# =================================
# HOME PAGE
# =================================

@app.route("/")
def home():
    return render_template("index.html")


# =================================
# SUBMIT FORM
# =================================

@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name", "").strip()

    address = request.form.get("address", "").strip()

    contact = request.form.get("contact", "").strip()

    sex = request.form.get("sex", "").strip()

    civil_status = request.form.get(
        "civil_status", ""
    ).strip()

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


    # =================================
    # VALIDATION
    # =================================

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

                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }


                body {

                    min-height: 100vh;

                    padding: 20px;

                    display: flex;

                    justify-content: center;

                    align-items: center;

                    font-family: "Inter", Arial, sans-serif;

                    color: #351b24;

                    background:
                        linear-gradient(
                            rgba(255, 250, 251, 0.70),
                            rgba(255, 250, 251, 0.70)
                        ),
                        url("/static/background.jpg");

                    background-size: 600px auto;

                    background-repeat: no-repeat;

                    background-position: center center;

                    background-attachment: fixed;
                }


                .message {

                    width: 100%;

                    max-width: 520px;

                    padding: 45px 30px;

                    text-align: center;

                    background:
                        rgba(255, 255, 255, 0.64);

                    border: 1px solid
                        rgba(255, 255, 255, 0.82);

                    border-radius: 22px;

                    box-shadow:
                        0 20px 55px
                        rgba(120, 35, 60, 0.15);

                    position: relative;

                    overflow: hidden;

                    animation: fadeUp 0.6s ease;
                }


                .message::before {

                    content: "";

                    position: absolute;

                    top: 0;

                    left: 0;

                    width: 100%;

                    height: 5px;

                    background:
                        linear-gradient(
                            90deg,
                            #922d4a,
                            #b83b5e,
                            #d35a78,
                            #b83b5e,
                            #922d4a
                        );
                }


                .error-icon {

                    width: 65px;

                    height: 65px;

                    margin: 0 auto 20px;

                    display: flex;

                    align-items: center;

                    justify-content: center;

                    border-radius: 50%;

                    background:
                        rgba(184, 59, 94, 0.10);

                    border: 2px solid
                        rgba(184, 59, 94, 0.25);

                    color: #b83b5e;

                    font-size: 28px;

                    font-weight: 700;
                }


                h2 {

                    margin-bottom: 12px;

                    color: #922d4a;

                    font-size: 25px;

                    font-weight: 700;

                    line-height: 1.3;
                }


                p {

                    margin-bottom: 28px;

                    color: #806a71;

                    font-size: 14px;

                    line-height: 1.6;
                }


                a {

                    display: inline-block;

                    padding: 14px 28px;

                    border-radius: 10px;

                    background:
                        linear-gradient(
                            135deg,
                            #922d4a,
                            #b83b5e,
                            #c34869
                        );

                    color: #ffffff;

                    text-decoration: none;

                    font-size: 14px;

                    font-weight: 600;

                    box-shadow:
                        0 9px 22px
                        rgba(184, 59, 94, 0.23);

                    transition:
                        transform 0.2s ease,
                        box-shadow 0.2s ease;
                }


                a:hover {

                    transform: translateY(-2px);

                    box-shadow:
                        0 13px 28px
                        rgba(184, 59, 94, 0.30);
                }


                @keyframes fadeUp {

                    from {

                        opacity: 0;

                        transform:
                            translateY(15px);
                    }

                    to {

                        opacity: 1;

                        transform:
                            translateY(0);
                    }
                }


                @media (max-width: 600px) {

                    body {

                        padding: 15px 10px;

                        background-size: 350px auto;
                    }


                    .message {

                        padding: 40px 22px;

                        border-radius: 18px;
                    }


                    .error-icon {

                        width: 58px;

                        height: 58px;

                        font-size: 25px;
                    }


                    h2 {

                        font-size: 22px;
                    }


                    p {

                        font-size: 13px;
                    }


                    a {

                        width: 100%;
                    }
                }

            </style>

        </head>


        <body>

            <div class="message">

                <div class="error-icon">
                    !
                </div>

                <h2>
                    Incomplete Information
                </h2>

                <p>
                    Please fill in all required fields
                    before submitting the form.
                </p>

                <a href="/">
                    Go Back
                </a>

            </div>

        </body>

        </html>
        """, 400


    # =================================
    # SAVE TO DATABASE
    # =================================

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


    # =================================
    # SUCCESS PAGE
    # =================================

    return """
    <!DOCTYPE html>
    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Submitted Successfully</title>


        <style>

            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }


            /* ================================
               PAGE
            ================================= */

            body {

                min-height: 100vh;

                padding: 20px;

                display: flex;

                justify-content: center;

                align-items: center;

                font-family: "Inter", Arial, sans-serif;

                color: #351b24;

                background:
                    linear-gradient(
                        rgba(255, 250, 251, 0.70),
                        rgba(255, 250, 251, 0.70)
                    ),
                    url("/static/background.jpg");

                background-size: 600px auto;

                background-repeat: no-repeat;

                background-position: center center;

                background-attachment: fixed;
            }


            /* ================================
               SUCCESS CARD
            ================================= */

            .message {

                width: 100%;

                max-width: 520px;

                padding: 45px 30px;

                text-align: center;

                background:
                    rgba(255, 255, 255, 0.64);

                border: 1px solid
                    rgba(255, 255, 255, 0.82);

                border-radius: 22px;

                box-shadow:
                    0 20px 55px
                    rgba(120, 35, 60, 0.15);

                position: relative;

                overflow: hidden;

                animation: fadeUp 0.6s ease;
            }


            /* ================================
               TOP ACCENT
            ================================= */

            .message::before {

                content: "";

                position: absolute;

                top: 0;

                left: 0;

                width: 100%;

                height: 5px;

                background:
                    linear-gradient(
                        90deg,
                        #922d4a,
                        #b83b5e,
                        #d35a78,
                        #b83b5e,
                        #922d4a
                    );
            }


            /* ================================
               SUCCESS ICON
            ================================= */

            .success-icon {

                width: 65px;

                height: 65px;

                margin: 0 auto 20px;

                display: flex;

                align-items: center;

                justify-content: center;

                border-radius: 50%;

                background:
                    rgba(184, 59, 94, 0.10);

                border: 2px solid
                    rgba(184, 59, 94, 0.25);

                color: #b83b5e;

                font-size: 30px;

                font-weight: 700;
            }


            /* ================================
               TITLE
            ================================= */

            h2 {

                margin-bottom: 12px;

                color: #922d4a;

                font-size: 25px;

                font-weight: 700;

                line-height: 1.3;
            }


            /* ================================
               DESCRIPTION
            ================================= */

            p {

                margin-bottom: 28px;

                color: #806a71;

                font-size: 14px;

                line-height: 1.6;
            }


            /* ================================
               BUTTON
            ================================= */

            a {

                display: inline-block;

                padding: 14px 28px;

                border-radius: 10px;

                background:
                    linear-gradient(
                        135deg,
                        #922d4a,
                        #b83b5e,
                        #c34869
                    );

                color: #ffffff;

                text-decoration: none;

                font-size: 14px;

                font-weight: 600;

                box-shadow:
                    0 9px 22px
                    rgba(184, 59, 94, 0.23);

                transition:
                    transform 0.2s ease,
                    box-shadow 0.2s ease,
                    filter 0.2s ease;
            }


            a:hover {

                transform: translateY(-2px);

                box-shadow:
                    0 13px 28px
                    rgba(184, 59, 94, 0.30);

                filter: brightness(1.05);
            }


            a:active {

                transform: translateY(0);
            }


            /* ================================
               ANIMATION
            ================================= */

            @keyframes fadeUp {

                from {

                    opacity: 0;

                    transform:
                        translateY(15px);
                }

                to {

                    opacity: 1;

                    transform:
                        translateY(0);
                }
            }


            /* ================================
               MOBILE
            ================================= */

            @media (max-width: 600px) {

                body {

                    padding: 15px 10px;

                    background-size: 350px auto;
                }


                .message {

                    padding: 40px 22px;

                    border-radius: 18px;
                }


                .success-icon {

                    width: 58px;

                    height: 58px;

                    font-size: 26px;
                }


                h2 {

                    font-size: 22px;
                }


                p {

                    font-size: 13px;
                }


                a {

                    width: 100%;

                    padding: 14px 20px;
                }
            }

        </style>

    </head>


    <body>

        <div class="message">

            <div class="success-icon">
                ✓
            </div>

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


# =================================
# INITIALIZE DATABASE
# =================================

# This must run when Flask/Gunicorn starts,
# including on Render.

init_database()


# =================================
# RUN SERVER
# =================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

