import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import os
import sys

# Function to launch a script
def open_page(page):
    root.destroy()
    if sys.platform.startswith("win"):  # Windows
        os.system(f"python {page.replace(os.sep, '/')}")
    else:  # Mac/Linux
        os.system(f"python3 {page.replace(os.sep, '/')}")

# Initialize main window
root = ctk.CTk()
root.geometry("1200x700")
root.title("Ride-Share App - Landing Page")

# Load Background Image (Fixed Path Issue)
try:
    bg_image = Image.open(r"assets/landing.png")  # Ensure this image exists
except FileNotFoundError:
    bg_image = Image.new("RGB", (2000, 1400), (30, 30, 30))  # Placeholder background
bg_image = bg_image.resize((2000, 1400))
bg_photo = ImageTk.PhotoImage(bg_image)

# Set Canvas for Background
canvas = tk.Canvas(root, width=1200, height=700)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Button Styling
btn_style = {
    "fg_color": "#8A2BE2",
    "border_width": 2,
    "border_color": "white",
    "text_color": "white",
    "font": ("Arial", 14, "bold"),
    "corner_radius": 20
}

# Animated Buttons
def on_enter(e):
    e.widget.configure(fg_color="#6A1B9A")  # Darker hover effect

def on_leave(e):
    e.widget.configure(fg_color="#8A2BE2")  # Restore original

# Buttons (Fixed Path Issues)
home_btn = ctk.CTkButton(root, text="Home", height=40, command=lambda: open_page(r"index/index.py"), **btn_style)
home_btn.place(x=1050, y=20)
home_btn.bind("<Enter>", on_enter)
home_btn.bind("<Leave>", on_leave)

logout_btn = ctk.CTkButton(root, text="Logout", height=40, command=lambda: open_page(r"auth/login.py"), **btn_style)
logout_btn.place(x=50, y=20)
logout_btn.bind("<Enter>", on_enter)
logout_btn.bind("<Leave>", on_leave)

driver_btn = ctk.CTkButton(root, text="Driver Dashboard", height=40, command=lambda: open_page(r"index/driver_auth.py"), **btn_style)
driver_btn.place(relx=0.3, rely=0.5, anchor="center")
driver_btn.bind("<Enter>", on_enter)
driver_btn.bind("<Leave>", on_leave)

passenger_btn = ctk.CTkButton(root, text="Passenger Dashboard", height=40, command=lambda: open_page(r"dashboards/passenger_dashboard.py"), **btn_style)
passenger_btn.place(relx=0.5, rely=0.5, anchor="center")
passenger_btn.bind("<Enter>", on_enter)
passenger_btn.bind("<Leave>", on_leave)

support_btn = ctk.CTkButton(root, text="Support", height=40, command=lambda: open_page(r"dashboards/support_dashboard.py"), **btn_style)
support_btn.place(relx=0.7, rely=0.5, anchor="center")
support_btn.bind("<Enter>", on_enter)
support_btn.bind("<Leave>", on_leave)

# Run App
root.mainloop()
