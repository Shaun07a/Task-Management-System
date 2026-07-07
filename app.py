from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db_connection

app = Flask(__name__)

app.secret_key = "task_management_secret"

@app.route("/", methods=["GET", "POST"])
def login():

    logout_success = session.pop("logout_success", False)

    if request.method == "POST":

        manager_id = request.form["manager_id"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM manager
            WHERE manager_code=%s
            AND password=%s
        """, (manager_id, password))

        manager = cursor.fetchone()

        cursor.close()
        conn.close()

        if manager:
            session["manager"] = manager["manager_code"]
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid Manager ID or Password",
            logout_success=logout_success
        )

    # This executes ONLY for GET requests
    return render_template(
        "login.html",
        logout_success=logout_success
    )




@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "manager" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Total Employees
    cursor.execute("SELECT COUNT(*) AS total FROM employees")
    total_employees = cursor.fetchone()["total"]

    # Total Tasks
    cursor.execute("SELECT COUNT(*) AS total FROM tasks")
    total_tasks = cursor.fetchone()["total"]

    # Completed Tasks
    cursor.execute("""
    SELECT COUNT(*) AS total
    FROM employee_tasks
    WHERE completed = 1
    """)
    completed_tasks = cursor.fetchone()["total"]

    # Pending Tasks
    cursor.execute("""
    SELECT COUNT(*) AS total
    FROM employee_tasks
    WHERE completed = 0
    """)
    pending_tasks = cursor.fetchone()["total"]

    success = None

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

        cursor.execute(query, (employee_id, task_id, completed))
        conn.commit()

        flash("Task assigned successfully!")

        cursor.close()
        conn.close()

        return redirect(url_for("dashboard"))

        success = "Task assigned successfully!"

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

    cursor.execute("""
    SELECT
        employee_tasks.assignment_id,
        employees.employee_name,
        tasks.task_title,
        employee_tasks.completed,
        employee_tasks.assigned_date

    FROM employee_tasks

    JOIN employees
    ON employee_tasks.employee_id = employees.employee_id

    JOIN tasks
    ON employee_tasks.task_id = tasks.task_id

    ORDER BY employee_tasks.assignment_id DESC
    """)

    assignments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
    "dashboard.html",
    employees=employees,
    tasks=tasks,
    assignments=assignments,
    success=success,

    total_employees=total_employees,
    total_tasks=total_tasks,
    completed_tasks=completed_tasks,
    pending_tasks=pending_tasks

)

@app.route("/logout")
def logout():

    session.pop("manager", None)
    session["logout_success"] = True

    return redirect(url_for("login"))
    

if __name__ == "__main__":
    app.run(debug=True)