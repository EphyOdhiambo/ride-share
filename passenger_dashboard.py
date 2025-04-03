import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import os
import subprocess

# Get the absolute path of the current directory (dashboards folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level to the "Module II" folder
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

# Function to open another Python script safely
def open_script(script_name):
    script_path = os.path.join(PROJECT_DIR, script_name).replace("\\", "/")  # Fixes Windows path issue

    if os.path.exists(script_path):
        print(f"✅ Opening: {script_path}")  # Debugging
        subprocess.run(["python", script_path], check=True)
    else:
        print(f"❌ Error: {script_path} not found!")  # Debugging

# Initialize Passenger Dashboard
root = ctk.CTk()
root.title("Passenger Dashboard - Ride-Share App")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Load Background Image
try:
    bg_image = Image.open(os.path.join(PROJECT_DIR, "assets", "passenger.png"))
except FileNotFoundError:
    bg_image = Image.new("RGB", (2000, 1400), (30, 30, 30))  # Dark fallback
bg_image = bg_image.resize((2000, 1400), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Set Canvas for Background
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Function for Button Actions
def go_booking():
    root.destroy()
    open_script("index/booking.py")  # Opens booking.py

def go_home():
    root.destroy()
    open_script("index/index.py")  # Opens index.py

def go_dashboard():
    root.destroy()
    open_script("index/landing.py")  # Opens landing.py

def go_ride_history():
    root.destroy()
    open_script("index/ride_history.py")  # Opens ride_history.py

def go_track_ride():
    root.destroy()
    open_script("index/track_ride.py")  # Opens track_ride.py

# Function for Hover Effect (Fixes fg_color issue)
def on_enter(e):
    if isinstance(e.widget, ctk.CTkButton):
        e.widget.configure(fg_color="#800080")  # Darker magenta on hover

def on_leave(e):
    if isinstance(e.widget, ctk.CTkButton):
        e.widget.configure(fg_color="magenta")  # Reset to magenta

# Button Styling
btn_style = {
    "fg_color": "magenta",
    "border_width": 0,
    "text_color": "white",
    "font": ("Arial", 16, "bold"),
    "corner_radius": 20,
    "width": 250,
    "height": 50
}

# Sidebar for Navigation
sidebar = ctk.CTkFrame(root, width=300, height=screen_height, fg_color="silver")
sidebar.place(x=0, y=0)

# Passenger Features
book_ride_btn = ctk.CTkButton(sidebar, text="Book Ride", **btn_style, command=go_booking)
book_ride_btn.pack(pady=20)
book_ride_btn.bind("<Enter>", on_enter)
book_ride_btn.bind("<Leave>", on_leave)

ride_history_btn = ctk.CTkButton(sidebar, text="Ride History", **btn_style, command=go_ride_history)
ride_history_btn.pack(pady=20)
ride_history_btn.bind("<Enter>", on_enter)
ride_history_btn.bind("<Leave>", on_leave)

track_ride_btn = ctk.CTkButton(sidebar, text="Track Ride", **btn_style, command=go_track_ride)
track_ride_btn.pack(pady=20)
track_ride_btn.bind("<Enter>", on_enter)
track_ride_btn.bind("<Leave>", on_leave)

# Dashboard Button (Top left)
dashboard_btn = ctk.CTkButton(root, text="Dashboard", **btn_style, command=go_dashboard)
dashboard_btn.place(x=1200, y=20)
dashboard_btn.bind("<Enter>", on_enter)
dashboard_btn.bind("<Leave>", on_leave)

# Home Button (Top Right)
home_btn = ctk.CTkButton(root, text="Home", **btn_style, command=go_home)
home_btn.place(x=900, y=20)
home_btn.bind("<Enter>", on_enter)
home_btn.bind("<Leave>", on_leave)

# Run the Tkinter main loop
root.mainloop()
