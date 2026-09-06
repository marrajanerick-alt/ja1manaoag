from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from functools import wraps

app = Flask(__name__)

# =========================================================
# CONFIGURATION
# =========================================================

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key"
)

# PostgreSQL connection provided by Render
DATABASE_URL = os.environ.get("DATABASE_URL")

# Admin credentials
# You can change these later using Render Environment Variables.
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "@Manaoag21")


# =========================================================
# DATABASE
# =========================================================

def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not configured."
        )

    return psycopg2.connect(
        DATABASE_URL,
        cursor_factory=RealDictCursor
    )


def init_database():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,

            name TEXT NOT NULL,
            nickname TEXT,

            age INTEGER NOT NULL,
            date_of_birth DATE NOT NULL,

            address TEXT NOT NULL,
            contact TEXT NOT NULL,

            sex TEXT NOT NULL,
            civil_status TEXT NOT NULL,
            educational_attainment TEXT NOT NULL,

            father_name TEXT NOT NULL,
            mother_name TEXT NOT NULL,

            employment_status TEXT NOT NULL,

            baptized TEXT NOT NULL,
            christian_duration TEXT NOT NULL,

            skills TEXT
        )
    """)

    conn.commit()

    cur.close()
    conn.close()


# =========================================================
# ADMIN AUTHENTICATION
# =========================================================

def admin_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):

        if not session.get("logged_in_as_admin"):
            return redirect(url_for("admin"))

        return function(*args, **kwargs)

    return decorated_function


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# SUBMIT PERSONAL INFORMATION
# =========================================================

@app.route("/submit", methods=["POST"])
def submit():

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

    # Skills are optional
    skills = request.form.get(
        "skills", ""
    ).strip()


    # -----------------------------------------------------
    # REQUIRED FIELDS
    # -----------------------------------------------------

    required_fields = [
        name,
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
        christian_duration
    ]

    if not all(required_fields):

        return render_error(
            "Incomplete Information",
            "Please fill in all required fields."
        ), 400


    # -----------------------------------------------------
    # AGE VALIDATION
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # CONTACT VALIDATION
    # -----------------------------------------------------

    contact = contact.replace(
        " ", ""
    ).replace(
        "-", ""
    )


    # Accept:

    # 9123456789
    # 09123456789
    # +639123456789

    if contact.startswith("+63"):

        contact = contact[3:]

    elif contact.startswith("0"):

        contact = contact[1:]


    if (
        not contact.isdigit()
        or len(contact) != 10
        or not contact.startswith("9")
    ):

        return render_error(
            "Invalid Contact Number",
            "Please enter a valid Philippine mobile number with 10 digits starting with 9."
        ), 400


    # Store in +63 format
    contact = "+63" + contact


    # -----------------------------------------------------
    # INSERT INTO POSTGRESQL
    # -----------------------------------------------------

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
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
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """, (
        name,
        nickname if nickname else None,
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
        skills if skills else None
    ))

    conn.commit()

    cur.close()
    conn.close()


    return render_success()


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        )

        password = request.form.get(
            "password",
            ""
        )


        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            session["logged_in_as_admin"] = True

            return redirect(
                url_for("admin_dashboard")
            )


        return render_template(
            "admin_login.html",
            error="Invalid username or password."
        )


    return render_template(
        "admin_login.html"
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():

    # -----------------------------------------------------
    # FILTER VALUES
    # -----------------------------------------------------

    search = request.args.get(
        "search",
        ""
    ).strip()

    sex = request.args.get(
        "sex",
        ""
    ).strip()

    civil_status = request.args.get(
        "civil_status",
        ""
    ).strip()

    educational_attainment = request.args.get(
        "educational_attainment",
        ""
    ).strip()

    employment_status = request.args.get(
        "employment_status",
        ""
    ).strip()

    baptized = request.args.get(
        "baptized",
        ""
    ).strip()

    christian_duration = request.args.get(
        "christian_duration",
        ""
    ).strip()


    # -----------------------------------------------------
    # BUILD QUERY
    # -----------------------------------------------------

    conditions = []
    values = []


    # Search
    if search:

        conditions.append("""
            (
                name ILIKE %s
                OR nickname ILIKE %s
                OR contact ILIKE %s
                OR address ILIKE %s
            )
        """)

        search_value = "%" + search + "%"

        values.extend([
            search_value,
            search_value,
            search_value,
            search_value
        ])


    # Sex
    if sex:

        conditions.append(
            "sex = %s"
        )

        values.append(sex)


    # Civil status
    if civil_status:

        conditions.append(
            "civil_status = %s"
        )

        values.append(civil_status)


    # Educational attainment
    if educational_attainment:

        conditions.append(
            "educational_attainment = %s"
        )

        values.append(
            educational_attainment
        )


    # Employment
    if employment_status:

        conditions.append(
            "employment_status = %s"
        )

        values.append(
            employment_status
        )


    # Baptized
    if baptized:

        conditions.append(
            "baptized = %s"
        )

        values.append(baptized)


    # Christian duration
    if christian_duration:

        conditions.append(
            "christian_duration = %s"
        )

        values.append(
            christian_duration
        )


    # -----------------------------------------------------
    # FINAL QUERY
    # -----------------------------------------------------

    query = """
        SELECT *
        FROM users
    """


    if conditions:

        query += (
            " WHERE "
            + " AND ".join(conditions)
        )


    query += """
        ORDER BY id DESC
    """


    # -----------------------------------------------------
    # GET USERS
    # -----------------------------------------------------

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        query,
        values
    )

    users = cur.fetchall()


    # -----------------------------------------------------
    # TOTAL RECORDS
    # -----------------------------------------------------

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM users
    """)

    total = cur.fetchone()["total"]


    cur.close()
    conn.close()


    return render_template(
        "admin_dashboard.html",

        users=users,
        total=total,

        search=search,
        sex=sex,
        civil_status=civil_status,
        educational_attainment=educational_attainment,
        employment_status=employment_status,
        baptized=baptized,
        christian_duration=christian_duration
    )


# =========================================================
# ADMIN EDIT
# =========================================================

@app.route(
    "/admin/edit/<int:user_id>",
    methods=["GET", "POST"]
)
@admin_required
def admin_edit(user_id):

    conn = get_db_connection()
    cur = conn.cursor()


    # -----------------------------------------------------
    # UPDATE RECORD
    # -----------------------------------------------------

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        nickname = request.form.get(
            "nickname",
            ""
        ).strip()

        age = request.form.get(
            "age",
            ""
        ).strip()

        date_of_birth = request.form.get(
            "date_of_birth",
            ""
        ).strip()

        address = request.form.get(
            "address",
            ""
        ).strip()

        contact = request.form.get(
            "contact",
            ""
        ).strip()

        sex = request.form.get(
            "sex",
            ""
        ).strip()

        civil_status = request.form.get(
            "civil_status",
            ""
        ).strip()

        educational_attainment = request.form.get(
            "educational_attainment",
            ""
        ).strip()

        father_name = request.form.get(
            "father_name",
            ""
        ).strip()

        mother_name = request.form.get(
            "mother_name",
            ""
        ).strip()

        employment_status = request.form.get(
            "employment_status",
            ""
        ).strip()

        baptized = request.form.get(
            "baptized",
            ""
        ).strip()

        christian_duration = request.form.get(
            "christian_duration",
            ""
        ).strip()

        skills = request.form.get(
            "skills",
            ""
        ).strip()


        # -------------------------------------------------
        # REQUIRED FIELDS
        # -------------------------------------------------

        required_fields = [
            name,
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
            christian_duration
        ]


        if not all(required_fields):

            cur.close()
            conn.close()

            return render_error(
                "Incomplete Information",
                "Please fill in all required fields."
            ), 400


        # -------------------------------------------------
        # AGE
        # -------------------------------------------------

        try:

            age = int(age)

        except ValueError:

            cur.close()
            conn.close()

            return render_error(
                "Invalid Age",
                "Age must be a whole number."
            ), 400


        if age < 1 or age > 120:

            cur.close()
            conn.close()

            return render_error(
                "Invalid Age",
                "Please enter a valid age."
            ), 400


        # -------------------------------------------------
        # CONTACT
        # -------------------------------------------------

        contact = contact.replace(
            " ", ""
        ).replace(
            "-", ""
        )


        if contact.startswith("+63"):

            contact = contact[3:]

        elif contact.startswith("0"):

            contact = contact[1:]


        if (
            not contact.isdigit()
            or len(contact) != 10
            or not contact.startswith("9")
        ):

            cur.close()
            conn.close()

            return render_error(
                "Invalid Contact Number",
                "Please enter a valid Philippine mobile number."
            ), 400


        contact = "+63" + contact


        # -------------------------------------------------
        # UPDATE DATABASE
        # -------------------------------------------------

        cur.execute("""
            UPDATE users
            SET
                name = %s,
                nickname = %s,
                age = %s,
                date_of_birth = %s,
                address = %s,
                contact = %s,
                sex = %s,
                civil_status = %s,
                educational_attainment = %s,
                father_name = %s,
                mother_name = %s,
                employment_status = %s,
                baptized = %s,
                christian_duration = %s,
                skills = %s
            WHERE id = %s
        """, (
            name,
            nickname if nickname else None,
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
            skills if skills else None,
            user_id
        ))


        conn.commit()

        cur.close()
        conn.close()


        return redirect(
            url_for("admin_dashboard")
        )


    # -----------------------------------------------------
    # GET RECORD
    # -----------------------------------------------------

    cur.execute("""
        SELECT *
        FROM users
        WHERE id = %s
    """, (user_id,))


    user = cur.fetchone()


    cur.close()
    conn.close()


    if not user:

        return render_error(
            "Record Not Found",
            "The requested record does not exist."
        ), 404


    return render_template(
        "admin_edit.html",
        user=user
    )


# =========================================================
# ADMIN DELETE
# =========================================================

@app.route(
    "/admin/delete/<int:user_id>",
    methods=["POST"]
)
@admin_required
def admin_delete(user_id):

    conn = get_db_connection()
    cur = conn.cursor()


    cur.execute("""
        DELETE FROM users
        WHERE id = %s
    """, (user_id,))


    conn.commit()

    cur.close()
    conn.close()


    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "logged_in_as_admin",
        None
    )

    return redirect(
        url_for("admin")
    )


# =========================================================
# ERROR PAGE
# =========================================================

def render_error(title, message):

    return f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
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

    align-items: center;

    justify-content: center;

    padding: 20px;

    font-family: Arial, sans-serif;

    background:
        linear-gradient(
            rgba(0,0,0,.35),
            rgba(0,0,0,.35)
        ),
        url("/static/14fbb570668080d5d5952ab7b710bcf7%20(1).jpg")
        center/cover fixed;
}}

.box {{

    width: 100%;

    max-width: 450px;

    padding: 35px;

    text-align: center;

    background: white;

    border-radius: 20px;

    box-shadow:
        0 10px 40px
        rgba(0,0,0,.25);
}}

h1 {{

    margin-bottom: 10px;

}}

p {{

    color: #555;

    line-height: 1.6;

}}

a {{

    display: inline-block;

    margin-top: 15px;

    padding: 12px 24px;

    color: white;

    background: #b83b5e;

    border-radius: 10px;

    text-decoration: none;

}}

</style>

</head>

<body>

<div class="box">

<h1>{title}</h1>

<p>{message}</p>

<a href="/">Go Back</a>

</div>

</body>

</html>
"""


# =========================================================
# SUCCESS PAGE
# =========================================================

def render_success():

    return """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
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

    align-items: center;

    justify-content: center;

    padding: 20px;

    font-family: Arial, sans-serif;

    background:
        linear-gradient(
            rgba(0,0,0,.35),
            rgba(0,0,0,.35)
        ),
        url("/static/14fbb570668080d5d5952ab7b710bcf7%20(1).jpg")
        center/cover fixed;
}

.box {

    width: 100%;

    max-width: 450px;

    padding: 35px;

    text-align: center;

    background: white;

    border-radius: 20px;

    box-shadow:
        0 10px 40px
        rgba(0,0,0,.25);
}

h1 {

    margin-bottom: 10px;

}

p {

    color: #555;

    line-height: 1.6;

}

a {

    display: inline-block;

    margin-top: 15px;

    padding: 12px 24px;

    color: white;

    background: #b83b5e;

    border-radius: 10px;

    text-decoration: none;

}

</style>

</head>

<body>

<div class="box">

<h1>Information Submitted!</h1>

<p>
Your personal information has been
successfully submitted.
</p>

<a href="/">Return to Form</a>

</div>

</body>

</html>
"""


# =========================================================
# INITIALIZE DATABASE
# =========================================================

# IMPORTANT:
# This runs when Gunicorn imports the Flask application.
# Therefore it also works on Render.

init_database()


# =========================================================
# RUN LOCALLY
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
