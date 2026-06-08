import tkinter as tk
from tkinter import ttk
import random
import string
import pyperclip


class PasswordGenerator:

    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e2f")

        title = tk.Label(
            root,
            text="🔐 Password Generator",
            font=("Segoe UI", 22, "bold"),
            bg="#1e1e2f",
            fg="#00d4ff"
        )
        title.pack(pady=20)

        tk.Label(
            root,
            text="Password Length",
            bg="#1e1e2f",
            fg="white",
            font=("Segoe UI", 11)
        ).pack()

        self.length_var = tk.IntVar(value=12)

        tk.Scale(
            root,
            from_=4,
            to=32,
            orient="horizontal",
            variable=self.length_var,
            bg="#1e1e2f",
            fg="white",
            highlightthickness=0
        ).pack()

        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        tk.Checkbutton(
            root,
            text="Include Numbers",
            variable=self.numbers_var,
            bg="#1e1e2f",
            fg="white",
            selectcolor="#2a2a40"
        ).pack()

        tk.Checkbutton(
            root,
            text="Include Symbols",
            variable=self.symbols_var,
            bg="#1e1e2f",
            fg="white",
            selectcolor="#2a2a40"
        ).pack()

        self.password_var = tk.StringVar()

        tk.Entry(
            root,
            textvariable=self.password_var,
            font=("Segoe UI", 14),
            width=35,
            justify="center"
        ).pack(pady=20)

        tk.Button(
            root,
            text="Generate Password",
            command=self.generate_password,
            bg="#00c853",
            fg="white",
            font=("Segoe UI", 11, "bold")
        ).pack(pady=10)

        tk.Button(
            root,
            text="Copy Password",
            command=self.copy_password,
            bg="#2196f3",
            fg="white",
            font=("Segoe UI", 11, "bold")
        ).pack()

        self.strength_label = tk.Label(
            root,
            text="Strength: ",
            bg="#1e1e2f",
            fg="white",
            font=("Segoe UI", 12)
        )
        self.strength_label.pack(pady=20)

        self.progress = ttk.Progressbar(
            root,
            length=300,
            mode="determinate"
        )
        self.progress.pack()

    def generate_password(self):

        chars = string.ascii_letters

        if self.numbers_var.get():
            chars += string.digits

        if self.symbols_var.get():
            chars += string.punctuation

        password = "".join(
            random.choice(chars)
            for _ in range(self.length_var.get())
        )

        self.password_var.set(password)

        self.check_strength(password)

    def check_strength(self, password):

        score = len(password)

        if any(c.isdigit() for c in password):
            score += 5

        if any(c in string.punctuation for c in password):
            score += 5

        if score < 12:
            strength = "Weak"
            value = 30

        elif score < 20:
            strength = "Medium"
            value = 60

        else:
            strength = "Strong"
            value = 100

        self.strength_label.config(
            text=f"Strength: {strength}"
        )

        self.progress["value"] = value

    def copy_password(self):
        pyperclip.copy(self.password_var.get())


root = tk.Tk()
app = PasswordGenerator(root)
root.mainloop()