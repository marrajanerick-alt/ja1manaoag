from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)

app.secret_key = "manaoag-admin-secret-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")


# =========================
# DATABASE
# =========================

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

    # Add new columns if using an older database
    existing_columns = [
        row[1]
        for row in conn.execute(
            "PRAGMA table_info(users)"
        ).fetchall()
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


# =========================
# HOME
# =========================

@app.route("/")
def home():

    return render_template("index.html")


# =========================
# SUBMIT
# =========================

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


    # Get filters
    search = request.args.get("search", "").strip()

    sex = request.args.get("sex", "").strip()
    civil_status = request.args.get("civil_status", "").strip()
    educational_attainment = request.args.get(
        "educational_attainment", ""
    ).strip()

    employment_status = request.args.get(
        "employment_status", ""
    ).strip()

    baptized = request.args.get(
        "baptized", ""
    ).strip()

    christian_duration = request.args.get(
        "christian_duration", ""
    ).strip()


    # Allowed filter values
    allowed_sex = ["Male", "Female"]

    allowed_civil_status = [
        "Single",
        "Married",
        "Widowed",
        "Separated"
    ]

    allowed_education = [
        "Elementary",
        "Junior High School",
        "Senior High School",
        "College",
        "Vocational",
        "Postgraduate"
    ]

    allowed_employment = [
        "Employed",
        "Self-Employed",
        "Unemployed",
        "Student",
        "Retired"
    ]

    allowed_baptized = [
        "Yes",
        "No"
    ]

    allowed_duration = [
        "New",
        "1-6 months",
        "6-11 months",
        "1-2 years",
        "3-4 years",
        "5 years and above"
    ]


    # Ignore invalid filter values

    if sex not in allowed_sex:
        sex = ""

    if civil_status not in allowed_civil_status:
        civil_status = ""

    if educational_attainment not in allowed_education:
        educational_attainment = ""

    if employment_status not in allowed_employment:
        employment_status = ""

    if baptized not in allowed_baptized:
        baptized = ""

    if christian_duration not in allowed_duration:
        christian_duration = ""


    # Build query safely

    query = "SELECT * FROM users WHERE 1=1"

    params = []


    # Search

    if search:

        query += """
            AND (
                name LIKE ?
                OR nickname LIKE ?
                OR address LIKE ?
                OR contact LIKE ?
                OR skills LIKE ?
            )
        """

        search_value = f"%{search}%"

        params.extend([
            search_value,
            search_value,
            search_value,
            search_value,
            search_value
        ])


    # Filters

    if sex:

        query += " AND sex = ?"

        params.append(sex)


    if civil_status:

        query += " AND civil_status = ?"

        params.append(civil_status)


    if educational_attainment:

        query += " AND educational_attainment = ?"

        params.append(educational_attainment)


    if employment_status:

        query += " AND employment_status = ?"

        params.append(employment_status)


    if baptized:

        query += " AND baptized = ?"

        params.append(baptized)


    if christian_duration:

        query += " AND christian_duration = ?"

        params.append(christian_duration)


    query += " ORDER BY id DESC"


    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    users = conn.execute(
        query,
        params
    ).fetchall()

    conn.close()


    return render_template(
        "admin_dashboard.html",
        users=users,

        search=search,

        sex=sex,
        civil_status=civil_status,
        educational_attainment=educational_attainment,
        employment_status=employment_status,
        baptized=baptized,
        christian_duration=christian_duration
    )


# =========================
# EDIT USER
# =========================

@app.route("/admin/edit/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):

    if not session.get("admin_logged_in"):

        return redirect(url_for("admin"))


    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row


    # GET USER

    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()


    if not user:

        conn.close()

        return render_error(
            "User Not Found",
            "The selected record does not exist."
        ), 404


    # UPDATE USER

    if request.method == "POST":

        name = request.form.get(
            "name", ""
        ).strip()

        nickname = request.form.get(
            "nickname", ""
        ).strip()

        age = request.form.get(
            "age", ""
        ).strip()

        date_of_birth = request.form.get(
            "date_of_birth", ""
        ).strip()

        address = request.form.get(
            "address", ""
        ).strip()

        contact = request.form.get(
            "contact", ""
        ).strip()

        sex = request.form.get(
            "sex", ""
        ).strip()

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

        baptized = request.form.get(
            "baptized", ""
        ).strip()

        christian_duration = request.form.get(
            "christian_duration", ""
        ).strip()

        skills = request.form.get(
            "skills", ""
        ).strip()


        # Validate required fields

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

            return render_template(
                "admin_edit.html",
                user=request.form,
                error="Please fill in all required fields."
            )


        # Validate age

        try:

            age = int(age)

        except ValueError:

            return render_template(
                "admin_edit.html",
                user=request.form,
                error="Age must be a whole number."
            )


        if age < 1 or age > 120:

            return render_template(
                "admin_edit.html",
                user=request.form,
                error="Please enter a valid age."
            )


        # Validate contact

        if contact.startswith("+63"):

            contact = contact[3:]


        if (
            not contact.isdigit()
            or len(contact) != 10
            or not contact.startswith("9")
        ):

            return render_template(
                "admin_edit.html",
                user=request.form,
                error="Please enter a valid Philippine mobile number."
            )


        contact = "+63" + contact


        # Update database

        conn.execute("""
            UPDATE users

            SET
                name = ?,
                nickname = ?,
                age = ?,
                date_of_birth = ?,
                address = ?,
                contact = ?,
                sex = ?,
                civil_status = ?,
                educational_attainment = ?,
                father_name = ?,
                mother_name = ?,
                employment_status = ?,
                baptized = ?,
                christian_duration = ?,
                skills = ?

            WHERE id = ?
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
            skills,
            user_id
        ))


        conn.commit()

        conn.close()


        return redirect(
            url_for("admin_dashboard")
        )


    conn.close()


    return render_template(
        "admin_edit.html",
        user=user,
        error=None
    )


# =========================
# DELETE USER
# =========================

@app.route(
    "/admin/delete/<int:user_id>",
    methods=["POST"]
)
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


    return redirect(
        url_for("admin_dashboard")
    )


# =========================
# LOGOUT
# =========================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "admin_logged_in",
        None
    )

    return redirect(
        url_for("admin")
    )


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

                border-radius: 18px;

                box-shadow:
                    0 10px 35px rgba(0,0,0,0.08);
            }}

            h1 {{
                color: #8f2948;
            }}

            p {{
                color: #777;

                line-height: 1.6;
            }}

            a {{
                display: inline-block;

                margin-top: 20px;

                padding: 12px 24px;

                border-radius: 10px;

                background: #b83b5e;

                color: white;

                text-decoration: none;
            }}

        </style>

    </head>

    <body>

        <div class="card">

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

                border-radius: 18px;

                box-shadow:
                    0 10px 35px rgba(0,0,0,0.08);
            }

            h1 {
                color: #8f2948;
            }

            p {
                color: #777;

                line-height: 1.6;
            }

            a {
                display: inline-block;

                margin-top: 20px;

                padding: 12px 24px;

                border-radius: 10px;

                background: #b83b5e;

                color: white;

                text-decoration: none;
            }

        </style>

    </head>

    <body>

        <div class="card">

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
