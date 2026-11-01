import tkinter as tk
from tkinter import ttk


REQUIREMENTS = [
    ("At least 8 characters", lambda password: len(password) >= 8),
    ("Contains a lowercase letter", lambda password: any(char.islower() for char in password)),
    ("Contains an uppercase letter", lambda password: any(char.isupper() for char in password)),
    ("Contains a number", lambda password: any(char.isdigit() for char in password)),
    ("Contains a special character", lambda password: any(not char.isalnum() for char in password)),
]


def evaluate_password(password):
    """Evaluate the password and return its score and requirement status."""
    requirement_status = [
        (description, check(password))
        for description, check in REQUIREMENTS
    ]

    score = sum(status for _, status in requirement_status)
    return score, requirement_status


def get_security_tip(strength):
    """Return a helpful security tip based on password strength."""
    tips = {
        "Weak": (
            "Security tip: Avoid common words and add more character variety."
        ),
        "Medium": (
            "Security tip: Add more unique characters to make your password stronger."
        ),
        "Strong": (
            "Security tip: Great password! Use a unique password for every account."
        ),
    }

    return tips[strength]


def update_password_strength(*args):
    """Update password strength, checklist, and security tip while typing."""
    password = password_var.get()

    if not password:
        result_label.config(text="")
        strength_var.set("Strength: —")
        progress_var.set(0)
        security_tip_label.config(text="")

        for label in requirement_labels:
            label.config(
                text=f"○ {label.requirement_text}",
                foreground=""
            )

        return

    score, requirement_status = evaluate_password(password)

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
    security_tip_label.config(text=get_security_tip(strength))

    for label, (description, passed) in zip(
        requirement_labels, requirement_status
    ):
        if passed:
            label.config(
                text=f"✓ {description}",
                foreground="#2e8b57"
            )
        else:
            label.config(
                text=f"✗ {description}",
                foreground="#c0392b"
            )


def check_password():
    """Display a message when the password field is empty."""
    if not password_var.get():
        result_label.config(
            text="Please enter a password",
            foreground="#d9534f"
        )
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
    """Clear the password and reset the checker."""
    password_var.set("")
    password_entry.focus()


root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("520x600")
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
subtitle_label.pack(pady=(0, 20))

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
result_label.pack(pady=(20, 8))

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

requirements_title = ttk.Label(
    main_frame,
    text="Password Requirements",
    font=("Segoe UI", 11, "bold")
)
requirements_title.pack(anchor="w", pady=(5, 8))

requirement_labels = []

for description, _ in REQUIREMENTS:
    requirement_label = ttk.Label(
        main_frame,
        text=f"○ {description}",
        font=("Segoe UI", 10)
    )
    requirement_label.requirement_text = description
    requirement_label.pack(anchor="w", pady=2)
    requirement_labels.append(requirement_label)

security_tip_label = ttk.Label(
    main_frame,
    text="",
    font=("Segoe UI", 10),
    wraplength=450,
    justify="left"
)
security_tip_label.pack(anchor="w", pady=(20, 0))

# Update password strength and requirements while typing.
password_var.trace_add("write", update_password_strength)

password_entry.focus()

root.mainloop()