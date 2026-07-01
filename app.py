from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db_connection

app = Flask(__name__)

app.secret_key = "task_management_secret"

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        manager_id = request.form["manager_id"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT * FROM manager
        WHERE manager_code = %s
        AND password = %s
        """

        cursor.execute(query, (manager_id, password))

        manager = cursor.fetchone()

        cursor.close()
        conn.close()

        if manager:

            session["manager"] = manager["manager_code"]

            return redirect(url_for("dashboard"))

        else:

            return render_template(
                "login.html",
                error="Invalid Manager ID or Password"
            )

    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "manager" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ---------- Save Assignment ----------
    if request.method == "POST":

        employee_id = request.form["employee_id"]
        task_id = request.form["task_id"]
        completed = request.form["completed"]

        query = """
        INSERT INTO employee_tasks
        (employee_id, task_id, completed)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (
            employee_id,
            task_id,
            completed
        ))

        conn.commit()

    # ---------- Employees ----------
    cursor.execute("""
        SELECT employee_id, employee_name
        FROM employees
        ORDER BY employee_name
    """)
    employees = cursor.fetchall()

    # ---------- Tasks ----------
    cursor.execute("""
        SELECT task_id, task_title
        FROM tasks
        ORDER BY task_title
    """)
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        employees=employees,
        tasks=tasks
    )

if __name__ == "__main__":
    app.run(debug=True)