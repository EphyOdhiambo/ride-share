import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Initialize main window
root = ctk.CTk()
root.title("About Us - Ride-Share App")
root.geometry("1200x700")  # Set window size

# Load and Resize Background Image
try:
    bg_image = Image.open("assets\pexels-maurxeugenio-1128527 (3).jpg")  # Ensure you have a background image
except FileNotFoundError:
    bg_image = Image.new("RGB", (1200, 700), (30, 30, 30))  # Fallback dark background
bg_image = bg_image.resize((2000, 1400), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Canvas for Background
canvas = tk.Canvas(root, width=1000, height=600)
canvas.pack(fill="both", expand=True)
canvas_bg = canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Function to Handle Button Hover
def on_enter(e):
    e.widget.configure(bg_color="purple")  # Darker on hover

def on_leave(e):
    e.widget.configure(bg_color="magenta")  # Reset color

# Function to Open Home Page (index.py)
def go_home():
    root.destroy()  # Close About Page
    import index  # Open Home Page

# Function to Open Login Page (login.py)
def go_login():
    root.destroy()  # Close About Page
    from auth import login  # ✅ Correct absolute import
  # Open Login Page

# Button Styling (Like JavaScript UI)
btn_style = {
    "bg_color": "magenta",
    "border_width": 0,
    "border_color": "white",
    "text_color": "white",
    "font": ("Arial", 14, "bold"),
    "corner_radius": 20
}

# Home Button (Top Right) - Opens index.py
home_btn = ctk.CTkButton(root, text="Home", height=40, width=100, **btn_style, command=go_home)
home_btn.place(x=30, y=20)
home_btn.bind("<Enter>", on_enter)
home_btn.bind("<Leave>", on_leave)

# About Us Section (Frame)
about_frame = ctk.CTkFrame(root, fg_color="transparent", corner_radius=5, width=900, height=500)
about_frame.place(relx=0.5, rely=0.55, anchor="center")

# About Us Title
title_label = ctk.CTkLabel(
    about_frame, text="About Ride-Share App", font=("Castellar", 40, "bold"), text_color="magenta"
)
title_label.pack(pady=20)

# About Us Description
desc_text = (
    "Ride-Share is an affordable and convenient way to get around. Our platform "
    "connects passengers with drivers in real time, ensuring safe, fast, and cost-effective rides.\n\n"
    "Live Tracking: See your ride in real-time using Google Maps.\n"
    
    "Secure Payments: Integrated payment with Stripe and PayPal.\n"
    
    "AI-Based Pricing: Get the best ride fares using AI-powered calculations.\n\n"
    
    "Join our growing community and experience the future of ride-sharing!"
)

desc_label = ctk.CTkLabel(about_frame, text=desc_text, font=("Segoe_print", 20), text_color="black", wraplength=800, justify="left")
desc_label.pack(pady=20)

# Get Started Button - Opens login.py
get_started_btn = ctk.CTkButton(about_frame, text="Get Started", height=50, width=200, **btn_style, command=go_login)
get_started_btn.pack(pady=20)
get_started_btn.bind("<Enter>", on_enter)
get_started_btn.bind("<Leave>", on_leave)

# Run the App
root.mainloop()
