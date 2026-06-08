import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "tasks.json"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart To-Do List")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e2f")

        self.tasks = []
        self.load_tasks()

        title = tk.Label(
            root,
            text="✅ Smart To-Do List",
            font=("Segoe UI", 22, "bold"),
            bg="#1e1e2f",
            fg="#00d4ff"
        )
        title.pack(pady=15)

        input_frame = tk.Frame(root, bg="#1e1e2f")
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(
            input_frame,
            width=40,
            font=("Segoe UI", 12)
        )
        self.task_entry.grid(row=0, column=0, padx=10)

        self.priority_var = tk.StringVar()
        self.priority_var.set("Medium")

        priority_menu = tk.OptionMenu(
            input_frame,
            self.priority_var,
            "High",
            "Medium",
            "Low"
        )
        priority_menu.grid(row=0, column=1)

        tk.Button(
            input_frame,
            text="Add Task",
            bg="#00c853",
            fg="white",
            command=self.add_task
        ).grid(row=0, column=2, padx=10)

        self.task_listbox = tk.Listbox(
            root,
            width=80,
            height=18,
            font=("Segoe UI", 11),
            bg="#2a2a40",
            fg="white",
            selectbackground="#00d4ff"
        )
        self.task_listbox.pack(pady=15)

        button_frame = tk.Frame(root, bg="#1e1e2f")
        button_frame.pack()

        tk.Button(
            button_frame,
            text="✔ Complete",
            bg="#2196f3",
            fg="white",
            command=self.complete_task
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="🗑 Delete",
            bg="#f44336",
            fg="white",
            command=self.delete_task
        ).grid(row=0, column=1, padx=10)

        self.counter_label = tk.Label(
            root,
            text="",
            bg="#1e1e2f",
            fg="white",
            font=("Segoe UI", 10)
        )
        self.counter_label.pack(pady=10)

        self.display_tasks()

    def load_tasks(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as file:
                try:
                    self.tasks = json.load(file)
                except:
                    self.tasks = []

    def save_tasks(self):
        with open(FILE_NAME, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self):
        task = self.task_entry.get()

        if task == "":
            messagebox.showwarning("Warning", "Enter a task")
            return

        self.tasks.append({
            "task": task,
            "priority": self.priority_var.get(),
            "completed": False
        })

        self.save_tasks()
        self.task_entry.delete(0, tk.END)
        self.display_tasks()

    def display_tasks(self):
        self.task_listbox.delete(0, tk.END)

        completed = 0

        for task in self.tasks:
            status = "✔" if task["completed"] else "⏳"

            if task["completed"]:
                completed += 1

            self.task_listbox.insert(
                tk.END,
                f"{status} [{task['priority']}] {task['task']}"
            )

        self.counter_label.config(
            text=f"Completed: {completed}/{len(self.tasks)}"
        )

    def complete_task(self):
        selected = self.task_listbox.curselection()

        if not selected:
            return

        index = selected[0]
        self.tasks[index]["completed"] = True

        self.save_tasks()
        self.display_tasks()

    def delete_task(self):
        selected = self.task_listbox.curselection()

        if not selected:
            return

        index = selected[0]

        del self.tasks[index]

        self.save_tasks()
        self.display_tasks()

root = tk.Tk()
app = TodoApp(root)
root.mainloop()