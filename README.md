# Task Management System

A simple web-based Task Management System built using **Python Flask** and **MySQL**. This application allows a manager to log in, assign tasks to employees, and view all assigned tasks from a dashboard.

---

## Features

- Manager Login Authentication
- Employee Selection
- Automatic Employee Name Display
- Task Assignment
- Task Completion Status
- View Assigned Tasks
- MySQL Database Integration
- Clean and Responsive User Interface

---

## Technologies Used

### Backend
- Python
- Flask
- MySQL Connector

### Frontend
- HTML5
- CSS3
- JavaScript

### Database
- MySQL

### Development Tools
- Visual Studio Code
- MySQL Workbench
- Git
- GitHub

---

## Project Structure

```
Task_Management_System/
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│
├── templates/
│   ├── login.html
│   └── dashboard.html
│
├── database/
│   └── task_management.sql
│
├── app.py
├── config.py
├── database.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Database Tables

- Manager
- Employees
- Tasks
- Employee_Tasks

---

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/task-management-system.git
```

### Navigate to the project

```bash
cd Task_Management_System
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Import the MySQL database

Import the `task_management.sql` file into MySQL Workbench.

### Configure the database

Update your MySQL username and password inside `config.py`.

### Run the application

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---



## Future Improvements

- Edit Assigned Tasks
- Delete Assigned Tasks
- Search Tasks
- Task Filtering
- Bootstrap UI
- Password Hashing
- Role-based Authentication

---

## Learning Outcomes

Through this project I learned:

- Flask Routing
- Flask Templates (Jinja2)
- CRUD Operations
- MySQL Integration
- HTML Forms
- JavaScript DOM Manipulation
- Session Management
- Git and GitHub Workflow

---

## Author

Shaun Joseph
