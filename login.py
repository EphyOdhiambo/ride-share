import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import sqlite3
import os
import bcrypt  # Import bcrypt for password hashing

# Function to open the landing page (dashboard)
def open_landing():
    root.destroy()
    os.system("python index\\landing.py")  # Ensure correct path separator for Windows

# Function to authenticate user and validate credentials
def login_user():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Fields cannot be empty!")
        return

    # Connect to database
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Fetch user data
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    conn.close()

    if user:
        hashed_password = user[0]  # Get the hashed password from the database
        if bcrypt.checkpw(password.encode(), hashed_password.encode()):  # Validate password
            messagebox.showinfo("Success", "Login Successful!")
            open_landing()  # Redirect to landing page
        else:
            messagebox.showerror("Error", "Invalid Credentials!")
    else:
        messagebox.showerror("Error", "User not found!")

# Event handlers for hover effects
def on_enter(e):
    widget = e.widget
    if isinstance(widget, ctk.CTkButton):  
        widget.configure(fg_color="#6A1B9A")  # CustomTkinter button hover effect
    else:
        widget.configure(bg="#6A1B9A")  # Standard Tkinter fallback

def on_leave(e):
    widget = e.widget
    if isinstance(widget, ctk.CTkButton):  
        widget.configure(fg_color="magenta")  # Restore original color
    else:
        widget.configure(bg="black")  # Restore background for Tkinter widgets

# Initialize main window
root = ctk.CTk()
root.title("Ride-Share App - Login Page")
root.state("zoomed")  # Fullscreen mode

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and Resize Background Image
bg_image = Image.open("assets\\Adobe Express - file.png")  
bg_image = bg_image.resize((2000, 1400), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Canvas for Background
canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Styling for Buttons
btn_style = {
    "fg_color": "magenta",
    "hover_color": "purple",
    "border_width": 0,
    "text_color": "white",
    "font": ("Arial", 14, "bold"),
    "corner_radius": 20
}

# Login Form Container
login_frame = ctk.CTkFrame(root, fg_color="black", corner_radius=20, width=400, height=350)
login_frame.place(relx=0.5, rely=0.5, anchor="center")

# Login Heading
login_label = ctk.CTkLabel(login_frame, text="Login", font=("Arial", 28, "bold"), text_color="white")
login_label.pack(pady=20)

# Username & Password Fields
username_entry = ctk.CTkEntry(login_frame, placeholder_text="Username", font=("Arial", 16), width=300)
username_entry.pack(pady=10)

password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*", font=("Arial", 16), width=300)
password_entry.pack(pady=10)

# Login Button
login_btn = ctk.CTkButton(login_frame, text="Login", height=40, **btn_style, command=login_user)
login_btn.pack(pady=20)

# Add hover effect
login_btn.bind("<Enter>", on_enter)
login_btn.bind("<Leave>", on_leave)

# Start Tkinter Main Loop
root.mainloop()
