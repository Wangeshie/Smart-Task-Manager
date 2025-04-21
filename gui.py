import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from db import init_db, add_task, get_all_tasks, update_task, delete_task, mark_task_complete

# --- Initialize DB ---
init_db()

# --- Globals ---
selected_task_id = None

# --- Main Window ---
root = tk.Tk()
root.title("Smart Task Manager")
root.geometry("700x600")
root.configure(bg="#f0f4f7")

# --- Styles ---
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'), background="#e1e1e1")
style.configure("Treeview", font=('Helvetica', 10), rowheight=30)

# --- Top Frame ---
form_frame = tk.Frame(root, bg="#f0f4f7")
form_frame.pack(pady=10)

tk.Label(form_frame, text="Title:", bg="#f0f4f7", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w")
title_entry = tk.Entry(form_frame, width=40, font=("Helvetica", 10))
title_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Description:", bg="#f0f4f7", font=("Helvetica", 10)).grid(row=1, column=0, sticky="w")
desc_entry = tk.Entry(form_frame, width=40, font=("Helvetica", 10))
desc_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Due Date:", bg="#f0f4f7", font=("Helvetica", 10)).grid(row=2, column=0, sticky="w")

due_var = tk.StringVar()
due_entry = tk.Entry(form_frame, textvariable=due_var, width=30, font=("Helvetica", 10))
due_entry.grid(row=2, column=1, sticky="w", padx=(10, 0))

def open_calendar():
    cal_win = tk.Toplevel(root)
    cal_win.title("Pick a Date")
    cal = Calendar(cal_win, selectmode="day")
    cal.pack(pady=20)

    def grab_date():
        due_var.set(cal.get_date())
        cal_win.destroy()

    tk.Button(cal_win, text="Select", command=grab_date, bg="#4CAF50", fg="white").pack(pady=10)

tk.Button(form_frame, text="📅", command=open_calendar).grid(row=2, column=1, sticky="e", padx=(0, 10))

tk.Label(form_frame, text="Priority:", bg="#f0f4f7", font=("Helvetica", 10)).grid(row=3, column=0, sticky="w")
priority_var = tk.StringVar()
priority_dropdown = ttk.Combobox(form_frame, textvariable=priority_var, values=["High", "Medium", "Low"], state="readonly")
priority_dropdown.grid(row=3, column=1, padx=10, pady=5)
priority_dropdown.current(1)  # Default to Medium

# --- Buttons ---
btn_frame = tk.Frame(root, bg="#f0f4f7")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Task", command=lambda: add_task_action(), bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update Task", command=lambda: update_task_action(), bg="#2196F3", fg="white", width=15).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete Task", command=lambda: delete_task_action(), bg="#f44336", fg="white", width=15).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Mark Complete", command=lambda: complete_task_action(), bg="#9C27B0", fg="white", width=15).grid(row=0, column=3, padx=5)

# --- Task List ---
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

task_list = ttk.Treeview(tree_frame, columns=("ID", "Title", "Due", "Priority", "Status"), show="headings", height=12)
task_list.pack()

for col in ["ID", "Title", "Due", "Priority", "Status"]:
    task_list.heading(col, text=col)
    task_list.column(col, anchor="center")

def color_priority(priority):
    if priority == "High":
        return "red"
    elif priority == "Medium":
        return "orange"
    elif priority == "Low":
        return "green"
    return "black"

def refresh_task_list():
    for i in task_list.get_children():
        task_list.delete(i)
    for task in get_all_tasks():
        status = "✅ COMPLETE" if task[5] == "Complete" else "🕒 Pending"
        task_list.insert("", "end", values=(task[0], task[1], task[3], task[4], status))

def on_task_select(event):
    global selected_task_id
    try:
        item = task_list.item(task_list.focus())
        task = item['values']
        selected_task_id = task[0]

        # Fill input fields
        title_entry.delete(0, tk.END)
        title_entry.insert(0, task[1])
        desc_entry.delete(0, tk.END)
        for full_task in get_all_tasks():
            if full_task[0] == selected_task_id:
                desc_entry.insert(0, full_task[2])
        due_var.set(task[2])
        priority_var.set(task[3])

        title_entry.focus_set()
    except:
        pass

task_list.bind('<<TreeviewSelect>>', on_task_select)

# --- Actions ---
def clear_fields():
    global selected_task_id
    selected_task_id = None
    title_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    due_var.set("")
    priority_var.set("Medium")

def add_task_action():
    if title_entry.get() and due_var.get() and priority_var.get():
        add_task(title_entry.get(), desc_entry.get(), due_var.get(), priority_var.get())
        clear_fields()
        refresh_task_list()
    else:
        messagebox.showwarning("Missing Info", "Please fill all required fields.")

def update_task_action():
    if selected_task_id:
        update_task(selected_task_id, title_entry.get(), desc_entry.get(), due_var.get(), priority_var.get())
        clear_fields()
        refresh_task_list()
    else:
        messagebox.showwarning("Select Task", "Select a task to update.")

def delete_task_action():
    if selected_task_id:
        delete_task(selected_task_id)
        clear_fields()
        refresh_task_list()
    else:
        messagebox.showwarning("Select Task", "Select a task to delete.")

def complete_task_action():
    if selected_task_id:
        mark_task_complete(selected_task_id)
        clear_fields()
        refresh_task_list()
    else:
        messagebox.showwarning("Select Task", "Select a task to mark complete.")

# --- Load tasks initially ---
refresh_task_list()

# --- Run ---
root.mainloop()