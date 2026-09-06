from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

import sqlite3
import os
from functools import wraps


app = Flask(__name__)

# ============================================================
# SECRET KEY
# ============================================================

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key"
)


# ============================================================
# DATABASE
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE = os.path.join(
    BASE_DIR,
    "database.db"
)


# ============================================================
# ADMIN LOGIN
# ============================================================

ADMIN_USERNAME = os.environ.get(
    "ADMIN_USERNAME",
    "admin"
)

ADMIN_PASSWORD = os.environ.get(
    "ADMIN_PASSWORD",
    "@Manaoag21"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():

    conn = sqlite3.connect(
        DATABASE
    )

    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_database():

    conn = sqlite3.connect(
        DATABASE
    )

    # --------------------------------------------------------
    # CREATE USERS TABLE
    # --------------------------------------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            nickname TEXT DEFAULT '',

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

            skills TEXT DEFAULT ''

        )
    """)

    conn.commit()


    # --------------------------------------------------------
    # CHECK EXISTING COLUMNS
    # --------------------------------------------------------

    columns = conn.execute(
        "PRAGMA table_info(users)"
    ).fetchall()

    existing_columns = [
        column[1]
        for column in columns
    ]


    # --------------------------------------------------------
    # ADD MISSING COLUMNS
    # --------------------------------------------------------

    new_columns = {

        "nickname":
            "ALTER TABLE users ADD COLUMN nickname TEXT DEFAULT ''",

        "age":
            "ALTER TABLE users ADD COLUMN age INTEGER",

        "date_of_birth":
            "ALTER TABLE users ADD COLUMN date_of_birth TEXT",

        "baptized":
            "ALTER TABLE users ADD COLUMN baptized TEXT",

        "christian_duration":
            "ALTER TABLE users ADD COLUMN christian_duration TEXT",

        "skills":
            "ALTER TABLE users ADD COLUMN skills TEXT DEFAULT ''"

    }


    for column_name, sql in new_columns.items():

        if column_name not in existing_columns:

            conn.execute(sql)


    conn.commit()

    conn.close()


# ============================================================
# ADMIN LOGIN REQUIRED DECORATOR
# ============================================================

def admin_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if not session.get(
            "logged_in_as_admin"
        ):

            return redirect(
                url_for("admin_login")
            )

        return function(
            *args,
            **kwargs
        )

    return decorated_function


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# SUBMIT FORM
# ============================================================

@app.route(
    "/submit",
    methods=["POST"]
)
def submit():

    # --------------------------------------------------------
    # GET FORM DATA
    # --------------------------------------------------------

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


    # Skills is OPTIONAL
    skills = request.form.get(
        "skills",
        ""
    ).strip()


    # --------------------------------------------------------
    # REQUIRED FIELDS
    # --------------------------------------------------------

    if not all([

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

    ]):

        return render_error(

            "Incomplete Information",

            "Please fill in all required fields."

        ), 400


    # --------------------------------------------------------
    # AGE VALIDATION
    # --------------------------------------------------------

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

            "Please enter an age between 1 and 120."

        ), 400


    # --------------------------------------------------------
    # CONTACT VALIDATION
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # INSERT
    # --------------------------------------------------------

    conn = get_db_connection()


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

        VALUES (

            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?

        )
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


# ============================================================
# ADMIN LOGIN
# ============================================================

@app.route(
    "/admin",
    methods=["GET", "POST"]
)
def admin_login():

    # Already logged in
    if session.get(
        "logged_in_as_admin"
    ):

        return redirect(
            url_for("admin_dashboard")
        )


    error = None


    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()


        password = request.form.get(
            "password",
            ""
        )


        if (

            username == ADMIN_USERNAME

            and password == ADMIN_PASSWORD

        ):

            session[
                "logged_in_as_admin"
            ] = True

            return redirect(
                url_for("admin_dashboard")
            )


        error = "Invalid username or password."


    return render_template(
        "admin_login.html",
        error=error
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.route(
    "/admin/dashboard"
)
@admin_required
def admin_dashboard():

    # --------------------------------------------------------
    # FILTER VALUES
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # QUERY
    # --------------------------------------------------------

    query = """
        SELECT *
        FROM users
        WHERE 1 = 1
    """


    params = []


    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    if search:

        query += """
            AND (
                name LIKE ?
                OR nickname LIKE ?
                OR address LIKE ?
                OR contact LIKE ?
                OR father_name LIKE ?
                OR mother_name LIKE ?
                OR skills LIKE ?
            )
        """

        search_value = f"%{search}%"


        params.extend([

            search_value,
            search_value,
            search_value,
            search_value,
            search_value,
            search_value,
            search_value

        ])


    # --------------------------------------------------------
    # SEX FILTER
    # --------------------------------------------------------

    if sex:

        query += """
            AND sex = ?
        """

        params.append(
            sex
        )


    # --------------------------------------------------------
    # CIVIL STATUS FILTER
    # --------------------------------------------------------

    if civil_status:

        query += """
            AND civil_status = ?
        """

        params.append(
            civil_status
        )


    # --------------------------------------------------------
    # EDUCATION FILTER
    # --------------------------------------------------------

    if educational_attainment:

        query += """
            AND educational_attainment = ?
        """

        params.append(
            educational_attainment
        )


    # --------------------------------------------------------
    # EMPLOYMENT FILTER
    # --------------------------------------------------------

    if employment_status:

        query += """
            AND employment_status = ?
        """

        params.append(
            employment_status
        )


    # --------------------------------------------------------
    # BAPTIZED FILTER
    # --------------------------------------------------------

    if baptized:

        query += """
            AND baptized = ?
        """

        params.append(
            baptized
        )


    # --------------------------------------------------------
    # CHRISTIAN DURATION FILTER
    # --------------------------------------------------------

    if christian_duration:

        query += """
            AND christian_duration = ?
        """

        params.append(
            christian_duration
        )


    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    query += """
        ORDER BY id DESC
    """


    conn = get_db_connection()


    users = conn.execute(
        query,
        params
    ).fetchall()


    conn.close()


    # --------------------------------------------------------
    # TOTAL COUNT
    # --------------------------------------------------------

    conn = get_db_connection()


    total_users = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]


    conn.close()


    return render_template(

        "admin_dashboard.html",

        users=users,

        total_users=total_users,

        search=search,

        sex=sex,

        civil_status=civil_status,

        educational_attainment=educational_attainment,

        employment_status=employment_status,

        baptized=baptized,

        christian_duration=christian_duration

    )


# ============================================================
# EDIT USER
# ============================================================

@app.route(
    "/admin/edit/<int:user_id>",
    methods=["GET", "POST"]
)
@admin_required
def edit_user(user_id):

    conn = get_db_connection()


    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()


    if user is None:

        conn.close()

        return render_error(

            "User Not Found",

            "The selected record does not exist."

        ), 404


    # --------------------------------------------------------
    # POST = UPDATE
    # --------------------------------------------------------

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


        # ----------------------------------------------------
        # REQUIRED VALIDATION
        # ----------------------------------------------------

        if not all([

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

        ]):

            conn.close()

            return render_error(

                "Incomplete Information",

                "Please fill in all required fields."

            ), 400


        # ----------------------------------------------------
        # AGE
        # ----------------------------------------------------

        try:

            age = int(age)

        except ValueError:

            conn.close()

            return render_error(

                "Invalid Age",

                "Age must be a whole number."

            ), 400


        if age < 1 or age > 120:

            conn.close()

            return render_error(

                "Invalid Age",

                "Please enter an age between 1 and 120."

            ), 400


        # ----------------------------------------------------
        # CONTACT
        # ----------------------------------------------------

        contact = contact.replace(
            " ",
            ""
        )


        # Allow either:
        #
        # 09123456789
        #
        # or
        #
        # +639123456789
        #
        # or
        #
        # 9123456789


        if contact.startswith(
            "+63"
        ):

            contact = contact[3:]


        elif contact.startswith(
            "0"
        ):

            contact = contact[1:]


        if (

            not contact.isdigit()

            or len(contact) != 10

            or not contact.startswith("9")

        ):

            conn.close()

            return render_error(

                "Invalid Contact Number",

                "Please enter a valid Philippine mobile number."

            ), 400


        contact = "+63" + contact


        # ----------------------------------------------------
        # UPDATE
        # ----------------------------------------------------

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


    # --------------------------------------------------------
    # GET = SHOW EDIT PAGE
    # --------------------------------------------------------

    conn.close()


    return render_template(

        "admin_edit.html",

        user=user

    )


# ============================================================
# DELETE USER
# ============================================================

@app.route(
    "/admin/delete/<int:user_id>",
    methods=["POST"]
)
@admin_required
def delete_user(user_id):

    conn = get_db_connection()


    conn.execute(
        """
        DELETE FROM users
        WHERE id = ?
        """,
        (user_id,)
    )


    conn.commit()

    conn.close()


    return redirect(
        url_for("admin_dashboard")
    )


# ============================================================
# ADMIN LOGOUT
# ============================================================

@app.route(
    "/admin/logout"
)
def admin_logout():

    session.pop(
        "logged_in_as_admin",
        None
    )


    return redirect(
        url_for("admin_login")
    )


# ============================================================
# ERROR PAGE
# ============================================================

def render_error(
    title,
    message
):

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

            background:
                rgba(255,255,255,0.95);

            border: 1px solid #eeeeee;

            border-radius: 18px;

            box-shadow:
                0 10px 35px
                rgba(0,0,0,0.08);

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


        <div class="icon">
            !
        </div>


        <h1>
            {title}
        </h1>


        <p>
            {message}
        </p>


        <a href="/">
            Go Back
        </a>


    </div>


</body>

</html>
"""


# ============================================================
# SUCCESS PAGE
# ============================================================

def render_success():

    return """
<!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0">

    <title>
        Information Submitted
    </title>


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

            background:
                rgba(255,255,255,0.95);

            border: 1px solid #eeeeee;

            border-radius: 18px;

            box-shadow:
                0 10px 35px
                rgba(0,0,0,0.08);

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


        <div class="icon">
            ✓
        </div>


        <h1>
            Information Submitted
        </h1>


        <p>
            Your personal information has been successfully recorded.
        </p>


        <a href="/">
            Submit Another
        </a>


    </div>


</body>

</html>
"""


# ============================================================
# INITIALIZE DATABASE
# IMPORTANT FOR RENDER/GUNICORN
# ============================================================

init_database()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
