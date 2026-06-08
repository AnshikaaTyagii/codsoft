import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILE_NAME = "contacts.json"


class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Contact Manager")
        self.root.geometry("1000x650")
        self.root.configure(bg="#1e1e2f")
        self.root.resizable(False, False)

        self.contacts = []
        self.load_contacts()

        title = tk.Label(
            root,
            text="📱 Smart Contact Manager",
            font=("Segoe UI", 24, "bold"),
            bg="#1e1e2f",
            fg="#00d4ff"
        )
        title.pack(pady=15)

        form_frame = tk.Frame(root, bg="#2a2a40")
        form_frame.pack(pady=10, padx=20, fill="x")

        labels = ["Name", "Phone", "Email", "Address"]

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()

        vars_list = [
            self.name_var,
            self.phone_var,
            self.email_var,
            self.address_var
        ]

        for i, label in enumerate(labels):
            tk.Label(
                form_frame,
                text=label,
                bg="#2a2a40",
                fg="white",
                font=("Segoe UI", 11)
            ).grid(row=i, column=0, padx=15, pady=10, sticky="w")

            tk.Entry(
                form_frame,
                textvariable=vars_list[i],
                width=45,
                font=("Segoe UI", 11)
            ).grid(row=i, column=1, padx=15, pady=10)

        button_frame = tk.Frame(root, bg="#1e1e2f")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="➕ Add",
            command=self.add_contact,
            bg="#00c853",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            width=15,
            cursor="hand2"
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            button_frame,
            text="✏ Update",
            command=self.update_contact,
            bg="#2196f3",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            width=15,
            cursor="hand2"
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            button_frame,
            text="🗑 Delete",
            command=self.delete_contact,
            bg="#f44336",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            width=15,
            cursor="hand2"
        ).grid(row=0, column=2, padx=8)

        tk.Button(
            button_frame,
            text="🧹 Clear",
            command=self.clear_fields,
            bg="#ff9800",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            width=15,
            cursor="hand2"
        ).grid(row=0, column=3, padx=8)

        search_frame = tk.Frame(root, bg="#1e1e2f")
        search_frame.pack(pady=15)

        tk.Label(
            search_frame,
            text="🔍 Search:",
            bg="#1e1e2f",
            fg="white",
            font=("Segoe UI", 11)
        ).pack(side=tk.LEFT)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.search_contact())

        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=40,
            font=("Segoe UI", 11)
        ).pack(side=tk.LEFT, padx=10)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#2a2a40",
            foreground="white",
            fieldbackground="#2a2a40",
            rowheight=30,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#00d4ff",
            foreground="black",
            font=("Segoe UI", 11, "bold")
        )

        columns = ("Name", "Phone", "Email", "Address")

        self.tree = ttk.Treeview(
            root,
            columns=columns,
            show="headings",
            height=12
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=220)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(
            root,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.select_contact)

        self.display_contacts()

        footer = tk.Label(
            root,
            text="Developed by Anshika | Smart Contact Manager",
            bg="#1e1e2f",
            fg="gray",
            font=("Segoe UI", 9)
        )
        footer.pack(side="bottom", pady=10)

    def load_contacts(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as file:
                try:
                    self.contacts = json.load(file)
                except:
                    self.contacts = []

    def save_contacts(self):
        with open(FILE_NAME, "w") as file:
            json.dump(self.contacts, file, indent=4)

    def add_contact(self):
        if not self.name_var.get() or not self.phone_var.get():
            messagebox.showwarning(
                "Warning",
                "Name and Phone are required!"
            )
            return

        contact = {
            "name": self.name_var.get(),
            "phone": self.phone_var.get(),
            "email": self.email_var.get(),
            "address": self.address_var.get()
        }

        self.contacts.append(contact)
        self.save_contacts()
        self.display_contacts()
        self.clear_fields()

    def display_contacts(self):
        self.tree.delete(*self.tree.get_children())

        for contact in self.contacts:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    contact["name"],
                    contact["phone"],
                    contact["email"],
                    contact["address"]
                )
            )

    def select_contact(self, event):
        selected = self.tree.focus()

        if selected:
            values = self.tree.item(selected, "values")

            self.name_var.set(values[0])
            self.phone_var.set(values[1])
            self.email_var.set(values[2])
            self.address_var.set(values[3])

    def update_contact(self):
        selected = self.tree.focus()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a contact first!"
            )
            return

        index = self.tree.index(selected)

        self.contacts[index] = {
            "name": self.name_var.get(),
            "phone": self.phone_var.get(),
            "email": self.email_var.get(),
            "address": self.address_var.get()
        }

        self.save_contacts()
        self.display_contacts()

    def delete_contact(self):
        selected = self.tree.focus()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a contact first!"
            )
            return

        index = self.tree.index(selected)

        del self.contacts[index]

        self.save_contacts()
        self.display_contacts()
        self.clear_fields()

    def search_contact(self):
        search = self.search_var.get().lower()

        self.tree.delete(*self.tree.get_children())

        for contact in self.contacts:
            if (
                search in contact["name"].lower()
                or search in contact["phone"]
            ):
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        contact["name"],
                        contact["phone"],
                        contact["email"],
                        contact["address"]
                    )
                )

    def clear_fields(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")


root = tk.Tk()
app = ContactBook(root)
root.mainloop()