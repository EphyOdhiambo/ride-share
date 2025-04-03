import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import subprocess
import os

# Get the base directory
BASE_DIR = os.path.join("C:/Users/GILBERT PC/Desktop/Software Development/Module II")

# Function to Open Pages
def open_home():
    subprocess.run(f'python "{os.path.join(BASE_DIR, "index", "index.py")}"', shell=True)

def open_dashboard():
    subprocess.run(f'python "{os.path.join(BASE_DIR, "index", "landing.py")}"', shell=True)

def open_accept_ride():
    try:
        subprocess.run(f'python "{os.path.join(BASE_DIR, "index", "accept_ride.py")}"', shell=True)
    except Exception as e:
        print(f"Error opening ride request page: {e}")

def open_live_tracking():
    try:
        subprocess.run(f'python "{os.path.join(BASE_DIR, "index", "track_ride.py")}"', shell=True)
    except Exception as e:
        print(f"Error opening live tracking page: {e}")

def open_rate_ride():
    try:
        subprocess.run(f'python "{os.path.join(BASE_DIR, "index", "rating.py")}"', shell=True)
    except Exception as e:
        print(f"Error opening rating page: {e}")

def open_logout():
    try:
        subprocess.run(f'python "{os.path.join(BASE_DIR, "auth", "login.py")}"', shell=True)
    except Exception as e:
        print(f"Error opening logout page: {e}")

# Initialize Window
root = ctk.CTk()
root.title("Driver Dashboard")
root.geometry("1200x700")

# Load Background Image
bg_image = Image.open("assets/driver.png")  # Adjust path if needed
bg_image = bg_image.resize((2000, 1400), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=2000, height=1400)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Sidebar Menu
sidebar = ctk.CTkFrame(root, width=600, height=900, fg_color="silver")
sidebar.place(x=0, y=2)

btn_home = ctk.CTkButton(sidebar, text="Home", command=open_home, fg_color="magenta")
btn_home.pack(pady=10)

btn_dashboard = ctk.CTkButton(sidebar, text="Dashboard", command=open_dashboard, fg_color="magenta")
btn_dashboard.pack(pady=20)

btn_accept = ctk.CTkButton(sidebar, text="Ride Request", command=open_accept_ride, fg_color="magenta")
btn_accept.pack(pady=10)

btn_live_tracking = ctk.CTkButton(sidebar, text="Live Tracking", command=open_live_tracking, fg_color="magenta")
btn_live_tracking.pack(pady=10)

btn_reviews = ctk.CTkButton(sidebar, text="Ratings & Reviews", command=open_rate_ride, fg_color="magenta")
btn_reviews.pack(pady=10)


btn_logout = ctk.CTkButton(sidebar, text="Logout", command=open_logout, fg_color="red")
btn_logout.pack(pady=10)

root.mainloop()
