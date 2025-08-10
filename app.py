import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

current_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(current_dir, "log.txt")

if not os.path.exists(log_path):
    with open(log_path, "w"): pass

def get_log_count():
    with open(log_path, "r") as f:
        return len(f.readlines())

app = ctk.CTk()
app.title("Fake Login Page Generator")
app.geometry("400x350")

log_counter_var = ctk.StringVar(value=f"Recorded Logins: {get_log_count()}")

title = ctk.CTkLabel(app, text="Select Fake Login Page", font=("Arial", 20))
title.pack(pady=10)

log_counter_label = ctk.CTkLabel(app, textvariable=log_counter_var, text_color="green")
log_counter_label.pack()

options = ["Facebook", "Gmail", "Instagram"]
selected_option = ctk.StringVar(value=options[0])
dropdown = ctk.CTkOptionMenu(app, values=options, variable=selected_option)
dropdown.pack(pady=10)

def open_login_window(platform_name):
    bg_color = {
        "Facebook": "#3b5998",
        "Gmail": "#ffffff",
        "Instagram": "#c13584"
    }.get(platform_name, "#2b2b2b")

    fg_color = "#ffffff" if platform_name != "Gmail" else "#000000"

    login_win = ctk.CTkToplevel(app)
    login_win.title(f"{platform_name} - Fake Login")
    login_win.geometry("350x350")
    login_win.configure(fg_color=bg_color)

    try:
        logo_path = os.path.join(current_dir, f"{platform_name.lower()}.png")
        img = Image.open(logo_path)
        img = img.resize((64, 64))
        logo = ctk.CTkImage(light_image=img, dark_image=img, size=(64, 64))
        logo_label = ctk.CTkLabel(login_win, image=logo, text="")
        logo_label.pack(pady=5)
    except:
        pass

    label = ctk.CTkLabel(login_win, text=f"{platform_name} Login", font=("Arial", 18), text_color=fg_color)
    label.pack(pady=5)

    email_entry = ctk.CTkEntry(login_win, placeholder_text="Email or Username")
    email_entry.pack(pady=10)

    pass_entry = ctk.CTkEntry(login_win, placeholder_text="Password", show="*")
    pass_entry.pack(pady=10)

    def on_login():
        email = email_entry.get()
        password = pass_entry.get()

        with open(log_path, "a") as f:
            f.write(f"{platform_name} | Email: {email} | Password: {password}\n")

        log_counter_var.set(f"Recorded Logins: {get_log_count()}")
        login_win.destroy()
        show_data_window(platform_name, email, password)

    login_btn = ctk.CTkButton(login_win, text="Login", command=on_login)
    login_btn.pack(pady=15)

def show_data_window(platform, email, password):
    data_win = ctk.CTkToplevel(app)
    data_win.title("Simulated Keylogger Result")
    data_win.geometry("400x250")

    msg = f"""⚠️ This was just a demo.
Your typed data was recorded to simulate a keylogger attack.

Platform: {platform}
Email/Username: {email}
Password: {password}
"""

    label = ctk.CTkLabel(data_win, text=msg, justify="left", wraplength=380)
    label.pack(pady=20)

    footer = ctk.CTkLabel(data_win, text="🛡 Educational use only. Don't enter real data!", font=("Arial", 10), text_color="red")
    footer.pack(side="bottom", pady=10)

def create_fake_page():
    platform = selected_option.get()
    open_login_window(platform)

def clear_logs():
    with open(log_path, "w"): pass
    log_counter_var.set(f"Recorded Logins: 0")
    messagebox.showinfo("Logs Cleared", "All logs have been cleared.")

create_btn = ctk.CTkButton(app, text="Create Fake Page", command=create_fake_page)
create_btn.pack(pady=10)

clear_btn = ctk.CTkButton(app, text="🧪 Clear Logs", command=clear_logs)
clear_btn.pack(pady=5)

app.mainloop()
