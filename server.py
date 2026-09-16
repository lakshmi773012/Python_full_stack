from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)


# -----------------------------------
# Create Database and Table
# -----------------------------------

def create_database():

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()


# -----------------------------------
# Home Page
# -----------------------------------

@app.route("/")
def home():

    return render_template("navbar.html")


# -----------------------------------
# Registration Page
# -----------------------------------

@app.route("/register", methods=["GET"])
def register_page():

    return render_template("registrationdemo.html")


# -----------------------------------
# Registration Path
# -----------------------------------

@app.route("/register", methods=["POST"])
def register():

    fullname = request.form["fullname"]
    username = request.form["username"]
    password = request.form["password"]

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO users (fullname, username, password)
            VALUES (?, ?, ?)
        """, (fullname, username, password))

        connection.commit()

    except sqlite3.IntegrityError:

        connection.close()

        return """
        <h2>Username already exists!</h2>
        <a href="/register">Try Again</a>
        """

    connection.close()

    return redirect("/login")


# -----------------------------------
# Login Page
# -----------------------------------

@app.route("/login", methods=["GET"])
def login_page():

    return render_template("login.html")


# -----------------------------------
# Login Path
# -----------------------------------

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()

    connection.close()

    if user:

        return """
        <h2>Login successful!</h2>
        <p>Welcome, """ + username + """!</p>
        <a href="/">Go to Home</a>
        """

    else:

        return """
        <h2>Login failed!</h2>
        <p>Username or password is incorrect.</p>
        <a href="/login">Try Again</a>
        """

# -----------------------------------
# Add Employee Page
# -----------------------------------

@app.route("/add-employee", methods=["GET"])
def add_employee_page():

    return render_template("add-employee.html")


# -----------------------------------
# Add Employee Path
# -----------------------------------

@app.route("/add-employee", methods=["POST"])
def add_employee():

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    department = request.form["department"]
    salary = request.form["salary"]
    join_date = request.form["join_date"]
    address = request.form["address"]

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            department TEXT NOT NULL,
            salary TEXT NOT NULL,
            join_date TEXT NOT NULL,
            address TEXT NOT NULL
        )
    """)

    cursor.execute("""
        INSERT INTO employees
        (name, email, phone, department, salary, join_date, address)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        department,
        salary,
        join_date,
        address
    ))

    connection.commit()

    connection.close()

    # After adding employee
    # go to Employees page

    return redirect("/employees")


# -----------------------------------
# Employees Page
# -----------------------------------

@app.route("/employees")
def employees():

    connection = sqlite3.connect("users.db")

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            phone,
            department,
            salary,
            join_date,
            address
        FROM employees
        ORDER BY id DESC
    """)

    employees = cursor.fetchall()

    connection.close()

    return render_template(
        "employees.html",
        employees=employees
    )


# -----------------------------------
# Edit Employee
# -----------------------------------

@app.route("/edit-employee/<int:id>", methods=["GET", "POST"])
def edit_employee(id):

    connection = sqlite3.connect("users.db")

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    # -----------------------------------
    # Update Employee
    # -----------------------------------

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        salary = request.form["salary"]
        join_date = request.form["join_date"]
        address = request.form["address"]

        cursor.execute("""
            UPDATE employees
            SET
                name = ?,
                email = ?,
                phone = ?,
                department = ?,
                salary = ?,
                join_date = ?,
                address = ?
            WHERE id = ?
        """, (
            name,
            email,
            phone,
            department,
            salary,
            join_date,
            address,
            id
        ))

        connection.commit()

        connection.close()

        return redirect("/employees")


    # -----------------------------------
    # Get Employee Details
    # -----------------------------------

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            phone,
            department,
            salary,
            join_date,
            address
        FROM employees
        WHERE id = ?
    """, (id,))

    employee = cursor.fetchone()

    connection.close()


    if employee is None:

        return """
        <h2>Employee not found!</h2>

        <a href="/employees">
            Back to Employees
        </a>
        """, 404


    return render_template(
        "edit-employee.html",
        employee=employee
    )


# -----------------------------------
# Delete Employee
# -----------------------------------

@app.route("/delete-employee/<int:id>")
def delete_employee(id):

    connection = sqlite3.connect("users.db")

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM employees
        WHERE id = ?
    """, (id,))

    connection.commit()

    connection.close()

    return redirect("/employees")


# -----------------------------------
# Start Server
# -----------------------------------

if __name__ == "__main__":

    create_database()

    app.run(debug=True)