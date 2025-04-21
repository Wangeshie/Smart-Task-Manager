import sqlite3

DB_NAME = "tasks.db"

# --- Initialize DB and Table ---
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)
    conn.commit()
    conn.close()


# --- Create Task ---
def add_task(title, description, due_date, priority):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, due_date, priority) VALUES (?, ?, ?, ?)",
                   (title, description, due_date, priority))
    conn.commit()
    conn.close()


# --- Read Tasks ---
def get_all_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks


# --- Update Task ---
def update_task(task_id, title, description, due_date, priority, status):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET title = ?, description = ?, due_date = ?, priority = ?, status = ?
        WHERE id = ?
    """, (title, description, due_date, priority, status, task_id))
    conn.commit()
    conn.close()


# --- Delete Task ---
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


# --- Mark Task as Complete ---
def mark_task_complete(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def update_task(task_id, title, description, due_date, priority):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks
        SET title = ?, description = ?, due_date = ?, priority = ?
        WHERE id = ?
    ''', (title, description, due_date, priority, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def mark_task_complete(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks
        SET status = 'Complete'
        WHERE id = ?
    ''', (task_id,))
    conn.commit()
    conn.close()
