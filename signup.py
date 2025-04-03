import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import sqlite3
import subprocess
import bcrypt  # Import bcrypt for password hashing
import os
import sys

# Function to Open Login Page Safely
def open_login_page():
    try:
        if signup_root.winfo_exists():  # Check if window exists
            signup_root.destroy()  # Close the window
        os.system("python auth/login.py")  # Open login page
    except:
        os.system("python auth/login.py")  # Fallback to opening login.py

# Function to Hash Password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Function to Register User and Redirect to Login Page
def signup_user():
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if not username or not email or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required!")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    # Hash the password before storing it
    hashed_password = hash_password(password)

    # Save user to database
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Create the users table if it does not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        username TEXT UNIQUE NOT NULL, 
                        email TEXT NOT NULL, 
                        password TEXT NOT NULL)''')

    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, hashed_password))
        conn.commit()
        messagebox.showinfo("Success", "Registration Successful!")
        signup_root.destroy()
        open_login_page()  # Redirect to login page after signup
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    
    conn.close()

# Initialize Sign-Up Window
signup_root = ctk.CTk()
signup_root.title("Ride-Share App - Sign Up")
signup_root.state("zoomed")  # Fullscreen mode

# Get Screen Dimensions
screen_width = signup_root.winfo_screenwidth()
screen_height = signup_root.winfo_screenheight()

# Load and Resize Background Image
try:
    bg_image = Image.open("assets/Adobe Express - file.png")  # Fixed path issue
except FileNotFoundError:
    bg_image = Image.new("RGB", (2000, 1400), (30, 30, 30))  # Placeholder background

bg_image = bg_image.resize((2000, 1400), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Canvas for Background
canvas = tk.Canvas(signup_root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas_bg = canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Sign-Up Form Container
signup_frame = ctk.CTkFrame(signup_root, fg_color="black", corner_radius=20, width=450, height=450)
signup_frame.place(relx=0.5, rely=0.5, anchor="center")

# Sign-Up Heading
signup_label = ctk.CTkLabel(signup_frame, text="Create Account", font=("Arial", 28, "bold"), text_color="white")
signup_label.pack(pady=20)

# Username, Email, Password, Confirm Password Fields
username_entry = ctk.CTkEntry(signup_frame, placeholder_text="Username", font=("Arial", 16), width=350)
username_entry.pack(pady=10)

email_entry = ctk.CTkEntry(signup_frame, placeholder_text="Email", font=("Arial", 16), width=350)
email_entry.pack(pady=10)

password_entry = ctk.CTkEntry(signup_frame, placeholder_text="Password", show="*", font=("Arial", 16), width=350)
password_entry.pack(pady=10)

confirm_password_entry = ctk.CTkEntry(signup_frame, placeholder_text="Confirm Password", show="*", font=("Arial", 16), width=350)
confirm_password_entry.pack(pady=10)

# Sign-Up Button
signup_btn = ctk.CTkButton(signup_frame, text="Sign Up", height=40, fg_color="magenta", text_color="white", corner_radius=20, command=signup_user)
signup_btn.pack(pady=20)

# Already have an account? Login Link
login_label = ctk.CTkLabel(
    signup_frame, text="Already have an account? Login", 
    font=("Arial", 12, "underline"), text_color="magenta", cursor="hand2"
)
login_label.pack()
login_label.bind("<Button-1>", lambda event: open_login_page())  # Make it a clickable link

# Start Tkinter Main Loop
signup_root.mainloop()
