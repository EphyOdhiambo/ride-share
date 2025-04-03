import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

DB_PATH = "rides.db"

# Database Setup
def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ride_ratings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ride_id INTEGER,
                        rating INTEGER
                    )''')
    conn.commit()
    conn.close()

# Function to fetch only accepted rides
def get_rides():
    """Fetches accepted rides from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM ride_requests WHERE status='accepted'")
    rides = cursor.fetchall()
    
    conn.close()
    return rides

# Function to submit the rating
def submit_rating():
    ride_info = ride_var.get()
    
    if not ride_info or ride_info == "No accepted rides available":
        messagebox.showerror("Error", "Please select a valid ride")
        return
    
    ride_id = ride_info.split(" - ")[0]  # Extract ride ID
    rating = rating_var.get()

    if not rating:
        messagebox.showerror("Error", "Please select a rating")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ride_ratings (ride_id, rating) VALUES (?, ?)", (ride_id, rating))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Rating submitted successfully!")
    root.destroy()

# Initialize database
initialize_db()

# GUI Setup
root = ctk.CTk()
root.title("Rate Your Ride")
root.geometry("500x400")
root.configure(bg="magenta")

# Styling
font_style = ("Arial", 14, "bold")
button_style = {"fg_color": "white", "text_color": "magenta", "font": ("Arial", 14, "bold"), "corner_radius": 10, "height": 50, "width": 250}

# Title Label
ctk.CTkLabel(root, text="Rate Your Ride", font=("Arial", 20, "bold"), text_color="white", bg_color="magenta").pack(pady=20)

# Ride Selection
ctk.CTkLabel(root, text="Select Ride:", font=font_style, text_color="white", bg_color="magenta").pack(pady=10)
ride_var = tk.StringVar()
rides = get_rides()

# If no accepted rides exist, show a placeholder
if not rides:
    ride_var.set("No accepted rides available")
    ride_options = ["No accepted rides available"]
else:
    ride_options = [f"{ride[0]} - {ride[1]}" for ride in rides]

ride_dropdown = ttk.Combobox(root, textvariable=ride_var, state="readonly", font=("Arial", 12), values=ride_options)
ride_dropdown.pack(pady=5)

# Rating Selection
ctk.CTkLabel(root, text="Rate your ride:", font=font_style, text_color="white", bg_color="magenta").pack(pady=10)
rating_var = tk.IntVar()
rating_frame = tk.Frame(root, bg="magenta")
rating_frame.pack()

for i in range(1, 6):
    tk.Radiobutton(rating_frame, text=f"{i}★", variable=rating_var, value=i, font=("Arial", 12), bg="magenta", fg="white").pack(side="left", padx=5)

# Submit Button
submit_btn = ctk.CTkButton(root, text="Submit Rating", command=submit_rating, **button_style)
submit_btn.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
