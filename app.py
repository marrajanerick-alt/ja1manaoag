from flask import Flask, render_template, request
import sqlite3
import os


app = Flask(__name__)


# ============================================================
# DATABASE
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(
    BASE_DIR,
    "database.db"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_database():

    conn = sqlite3.connect(DATABASE)

    # Create table if it does not exist
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


    # ========================================================
    # ADD MISSING COLUMNS
    # ========================================================

    columns = conn.execute(
        "PRAGMA table_info(users)"
    ).fetchall()

    existing_columns = [
        column[1]
        for column in columns
    ]


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
# HOME PAGE
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


    # ========================================================
    # GET FORM DATA
    # ========================================================

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


    # SKILLS IS OPTIONAL
    skills = request.form.get(
        "skills",
        ""
    ).strip()


    # ========================================================
    # REQUIRED FIELD VALIDATION
    # ========================================================

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


    # ========================================================
    # AGE VALIDATION
    # ========================================================

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


    # ========================================================
    # CONTACT VALIDATION
    # ========================================================

    if (

        not contact.isdigit()

        or len(contact) != 10

        or not contact.startswith("9")

    ):

        return render_error(

            "Invalid Contact Number",

            "Please enter a valid Philippine mobile number with 10 digits starting with 9."

        ), 400


    # Add Philippines country code

    contact = "+63" + contact


    # ========================================================
    # SAVE TO DATABASE
    # ========================================================

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


    # ========================================================
    # SUCCESS
    # ========================================================

    return render_success()


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

            background: rgba(
                255,
                255,
                255,
                0.95
            );

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
                rgba(
                    255,
                    255,
                    255,
                    0.95
                );

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
# IMPORTANT FOR RENDER / GUNICORN
# ============================================================

init_database()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
