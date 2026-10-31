import tkinter as tk
from tkinter import ttk


def evaluate_password(password):
    """Evaluate the password and return its score and improvement feedback."""
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    if any(char.islower() for char in password):
        score += 1
    else:
        feedback.append("Add lowercase letters")

    if any(char.isupper() for char in password):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("Add numbers")

    if any(not char.isalnum() for char in password):
        score += 1
    else:
        feedback.append("Add special characters")

    return score, feedback


def update_password_strength(*args):
    """Update the password strength automatically while typing."""
    password = password_var.get()

    if not password:
        result_label.config(text="")
        strength_var.set("Strength: —")
        progress_var.set(0)
        feedback_label.config(text="")
        return

    score, feedback = evaluate_password(password)

    if score <= 2:
        strength = "Weak"
        colour = "#d9534f"
    elif score <= 4:
        strength = "Medium"
        colour = "#f0ad4e"
    else:
        strength = "Strong"
        colour = "#5cb85c"

    result_label.config(
        text=f"Your password is {strength}",
        foreground=colour
    )

    strength_var.set(f"Strength: {strength}")
    progress_var.set(score * 20)

    if feedback:
        feedback_label.config(text=" • ".join(feedback))
    else:
        feedback_label.config(
            text="Excellent! Your password meets all security checks."
        )


def check_password():
    """Keep the button functionality for manually checking the password."""
    password = password_var.get()

    if not password:
        result_label.config(
            text="Please enter a password",
            foreground="#d9534f"
        )
        strength_var.set("Strength: —")
        progress_var.set(0)
        feedback_label.config(text="")
        return

    update_password_strength()


def toggle_password():
    """Show or hide the password text."""
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
        toggle_button.config(text="Show")
    else:
        password_entry.config(show="")
        toggle_button.config(text="Hide")


def clear_password():
    """Clear the password and reset all results."""
    password_var.set("")
    password_entry.focus()


root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("520x420")
root.resizable(False, False)

password_var = tk.StringVar()
strength_var = tk.StringVar(value="Strength: —")
progress_var = tk.IntVar(value=0)

main_frame = ttk.Frame(root, padding=30)
main_frame.pack(fill="both", expand=True)

title_label = ttk.Label(
    main_frame,
    text="Password Strength Checker",
    font=("Segoe UI", 20, "bold")
)
title_label.pack(pady=(0, 8))

subtitle_label = ttk.Label(
    main_frame,
    text="Check how strong and secure your password is.",
    font=("Segoe UI", 10)
)
subtitle_label.pack(pady=(0, 25))

password_label = ttk.Label(
    main_frame,
    text="Enter Password",
    font=("Segoe UI", 11, "bold")
)
password_label.pack(anchor="w")

password_frame = ttk.Frame(main_frame)
password_frame.pack(fill="x", pady=(6, 15))

password_entry = ttk.Entry(
    password_frame,
    textvariable=password_var,
    show="*",
    font=("Segoe UI", 12)
)
password_entry.pack(side="left", fill="x", expand=True)

toggle_button = ttk.Button(
    password_frame,
    text="Show",
    command=toggle_password
)
toggle_button.pack(side="left", padx=(8, 0))

button_frame = ttk.Frame(main_frame)
button_frame.pack(fill="x")

check_button = ttk.Button(
    button_frame,
    text="Check Password",
    command=check_password
)
check_button.pack(side="left")

clear_button = ttk.Button(
    button_frame,
    text="Clear",
    command=clear_password
)
clear_button.pack(side="left", padx=(10, 0))

result_label = ttk.Label(
    main_frame,
    text="",
    font=("Segoe UI", 14, "bold")
)
result_label.pack(pady=(25, 8))

strength_label = ttk.Label(
    main_frame,
    textvariable=strength_var,
    font=("Segoe UI", 11, "bold")
)
strength_label.pack(anchor="w")

progress_bar = ttk.Progressbar(
    main_frame,
    maximum=100,
    variable=progress_var
)
progress_bar.pack(fill="x", pady=(8, 15))

feedback_label = ttk.Label(
    main_frame,
    text="",
    font=("Segoe UI", 10),
    wraplength=450,
    justify="center"
)
feedback_label.pack(pady=(5, 0))

# Automatically update password strength whenever the user types.
password_var.trace_add("write", update_password_strength)

password_entry.focus()

root.mainloop()