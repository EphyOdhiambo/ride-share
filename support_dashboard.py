import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import subprocess
import os
import sys

# Initialize main window
root = ctk.CTk()
root.title("Support Dashboard - Ride-Share App")
root.geometry("1200x700")
root.state("zoomed")  # Make the window full screen

# Load and Resize Background Image
try:
    bg_image = Image.open("support.png")  # Replace with your image file
except FileNotFoundError:
    bg_image = Image.new("RGB", (1920, 1080), "#ffffff")  # White fallback background
bg_image = bg_image.resize((1920, 1080), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Canvas for Background
canvas = tk.Canvas(root, width=1920, height=1080, bg="#f5f5f5", highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Function to Open FAQ Page
def go_faq():
    file_path = "index/Faqs.py"
    if os.path.exists(file_path):
        subprocess.Popen([sys.executable, file_path])
    else:
        print("Error: faq.py not found!")

# Function to Open Contact Page
def go_contact():
    file_path = "index/contact.py"
    if os.path.exists(file_path):
        subprocess.Popen([sys.executable, file_path])
    else:
        print("Error: contact.py not found!")

# Function to Open Dashboard Page
def go_dashboard():
    file_path = "index/landing.py"
    if os.path.exists(file_path):
        subprocess.Popen([sys.executable, file_path])
    else:
        print("Error: landing.py not found!")

# Function to Open Home Page
def go_home():
    file_path = "index/index.py"
    if os.path.exists(file_path):
        subprocess.Popen([sys.executable, file_path])
    else:
        print("Error: index.py not found!")

# Function for Hover Effect
def on_enter(e):
    e.widget.configure(fg_color="#800080")  # Dark magenta hover

def on_leave(e):  # Fixed missing parentheses
    e.widget.configure(fg_color="#ba55d3")  # Light magenta original

# Button Styling
btn_style = {
    "fg_color": "#ba55d3",  # Light magenta
    "border_width": 2,
    "border_color": "white",
    "text_color": "white",
    "font": ("Arial", 16, "bold"),
    "corner_radius": 25,
    "height": 60,
    "width": 300
}

# Home Button (Top Right)
home_btn = ctk.CTkButton(root, text="Home", command=go_home, **btn_style)
home_btn.place(x=1550, y=20)
home_btn.bind("<Enter>", on_enter)
home_btn.bind("<Leave>", on_leave)

# Centered Buttons
button_frame = ctk.CTkFrame(root, fg_color="transparent")
button_frame.place(relx=0.5, rely=0.6, anchor="center")

faq_btn = ctk.CTkButton(button_frame, text="FAQs", command=go_faq, **btn_style)
faq_btn.pack(pady=20)
faq_btn.bind("<Enter>", on_enter)
faq_btn.bind("<Leave>", on_leave)

contact_btn = ctk.CTkButton(button_frame, text="Get in Touch", command=go_contact, **btn_style)
contact_btn.pack(pady=20)
contact_btn.bind("<Enter>", on_enter)
contact_btn.bind("<Leave>", on_leave)

dashboard_btn = ctk.CTkButton(button_frame, text="Dashboard", command=go_dashboard, **btn_style)
dashboard_btn.pack(pady=20)
dashboard_btn.bind("<Enter>", on_enter)
dashboard_btn.bind("<Leave>", on_leave)

# Start the Tkinter main loop
root.mainloop()
