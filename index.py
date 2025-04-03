import tkinter as tk
from tkinter import BOTH
from PIL import Image, ImageTk
import customtkinter as ctk
import subprocess

# Initialize main window
root = ctk.CTk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f'{screen_width}x{screen_height}')
root.title("Ride-Share App - Landing Page")

# Load Background Image
try:
    bg_image = Image.open("assets\index12.png")  # ✅ Correct
except FileNotFoundError:
    bg_image = Image.new("RGB", (1920, 1080), (30, 30, 30))  # Placeholder background

bg_image = bg_image.resize((1920, 1080))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack(fill=BOTH, expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# App Title
app_title = tk.Label(root, text="WELCOME TO AFFORDABLE RIDE-SHARE", font=("clarendon", 40, "bold"), bg="silver", fg="black")
app_title.place(relx=0.5, rely=0.2, anchor="center")

# Landing Page Statements
statements = [
    "Reliable, Affordable, and Secure Rides at Your Fingertips!",
    "Seamless Booking, Live Tracking, and Hassle-Free Payments.",
    "Join Us Today and Experience a New Era of Ride-Sharing!"
]

for i, text in enumerate(statements):
    tk.Label(root, text=text, font=("Arial", 16), bg="black", fg="white").place(relx=0.5, rely=0.3 + (i * 0.05), anchor="center")

# Function to open login.py and then launch landing.py if login is successful
def open_login():
    process = subprocess.run(["python", r"auth/login.py"])  # Wait for login.py to complete
    if process.returncode == 0:  # Check if login was successful
        subprocess.Popen(["python", r"landing.py"], shell=True)  # Run with Python


# Function to open signup.py
def open_signup():
    subprocess.Popen(["python", r"auth\signup.py"])  # Open signup page

# Function to open About Us page
def open_about():
    subprocess.Popen(["python", r"index\About.py"])  # Open About Us page

# Button Styling
btn_style = {
    "fg_color": "magenta", 
    "hover_color": "#444444",
    "border_width": 2,
    "border_color": "red",
    "text_color": "white",
    "font": ("Arial", 14, "bold"),
    "corner_radius": 20
}

# Create Buttons
signup_btn = ctk.CTkButton(root, text="Sign Up", height=40, **btn_style, command=open_signup)
signup_btn.place(x=1220, y=20)

login_btn = ctk.CTkButton(root, text="Login", height=40, **btn_style, command=open_login)
login_btn.place(x=1050, y=20)

about_btn = ctk.CTkButton(root, text="About Us", height=40, **btn_style, command=open_about)
about_btn.place(x=1380, y=20)

# Start Tkinter main loop
root.mainloop()
