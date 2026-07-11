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

        cursor.execute("""
        SELECT *
        FROM employee_tasks
        WHERE employee_id=%s
        AND task_id=%s
        AND completed=0
        """, (employee_id, task_id))

        existing = cursor.fetchone()

        if existing:

            flash(
                "This task is already assigned to the employee!",
                "error"
            )

        else:

            cursor.execute("""
            INSERT INTO employee_tasks
            (employee_id, task_id, completed)
            VALUES (%s, %s, %s)
            """, (employee_id, task_id, completed))

            conn.commit()

            flash(
                "Task assigned successfully!",
                "success"
            )

       

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
    et.assignment_id,
    e.employee_name,
    t.task_title,
    et.completed,
    CASE
        WHEN et.completed = 1 THEN 'Completed'
        ELSE 'Pending'
    END AS status,
    et.assigned_date
    FROM employee_tasks et
    JOIN employees e
    ON et.employee_id = e.employee_id
    JOIN tasks t
    ON et.task_id = t.task_id
    ORDER BY et.assigned_date DESC;
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

@app.route("/delete/<int:assignment_id>")
def delete_task(assignment_id):

    if "manager" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM employee_tasks
        WHERE assignment_id=%s
    """, (assignment_id,))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Task deleted successfully!", "success")

    return redirect(url_for("dashboard"))

@app.route("/complete/<int:assignment_id>")
def complete_task(assignment_id):

    if "manager" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE employee_tasks
        SET completed = 1
        WHERE assignment_id = %s
    """, (assignment_id,))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Task marked as completed!", "success")

    return redirect(url_for("dashboard"))

@app.route("/edit/<int:assignment_id>", methods=["GET", "POST"])
def edit_task(assignment_id):

    if "manager" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT *
    FROM employee_tasks
    WHERE assignment_id = %s
    """, (assignment_id,))

    assignment = cursor.fetchone()

    if not assignment:
        flash("Task not found!", "error")
        cursor.close()
        conn.close()
        return redirect(url_for("dashboard"))
    
    cursor.execute("""
    SELECT employee_id, employee_name
    FROM employees
    ORDER BY employee_name
    """)

    employees = cursor.fetchall()

    cursor.execute("""
    SELECT task_id, task_title
    FROM tasks
    ORDER BY task_title
    """)

    tasks = cursor.fetchall()

    if request.method == "POST":

        employee_id = request.form["employee_id"]
        task_id = request.form["task_id"]
        completed = request.form["completed"]

        cursor.execute("""
        SELECT *
        FROM employee_tasks
        WHERE employee_id = %s
        AND task_id = %s
        AND assignment_id != %s
        """, (employee_id, task_id, assignment_id))

        duplicate = cursor.fetchone()

        
        if duplicate:

            flash(
                "This task is already assigned to the employee!",
                "error"
            )

        else:

            cursor.execute("""
                UPDATE employee_tasks
                SET employee_id=%s,
                    task_id=%s,
                    completed=%s
                WHERE assignment_id=%s
            """, (employee_id, task_id, completed, assignment_id))

            conn.commit()

            flash(
                "Task updated successfully!",
                "success"
                )

        cursor.close()
        conn.close()

        return redirect(url_for("dashboard"))

    cursor.close()
    conn.close()

    return render_template(
    "edit_task.html",
    assignment=assignment,
    employees=employees,
    tasks=tasks
)

@app.route("/logout")
def logout():

    session.pop("manager", None)
    session["logout_success"] = True

    return redirect(url_for("login"))
    

if __name__ == "__main__":
    app.run(debug=True)