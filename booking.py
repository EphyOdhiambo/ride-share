import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import subprocess
import sys

DB_PATH = "rides.db"

def ensure_database():
    """Ensure the ride_requests table exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create ride_requests table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS ride_requests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        pickup TEXT NOT NULL,
                        dropoff TEXT NOT NULL,
                        ride_type TEXT NOT NULL,
                        preferred_time TEXT NOT NULL,
                        status TEXT DEFAULT 'pending',
                        estimated_fare REAL)''')
    
    conn.commit()
    conn.close()

def open_admin_dashboard():
    """Opens the admin dashboard."""
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
    file_path = os.path.join(script_dir, "admin_dashboard.py")  # Ensure correct path

    if os.path.exists(file_path):
        subprocess.Popen([sys.executable, file_path])
    else:
        messagebox.showerror("Error", "admin_dashboard.py not found!") 

def create_time_options():
    """Create list of time slots in 30-minute intervals"""
    times = []
    current_time = datetime.now()
    # Round to next 30-minute interval
    minutes = current_time.minute
    if minutes < 30:
        current_time = current_time.replace(minute=30, second=0, microsecond=0)
    else:
        current_time = (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    
    # Generate time slots for next 24 hours
    for _ in range(48):  # 48 slots of 30 minutes each
        times.append(current_time.strftime("%I:%M %p"))
        current_time += timedelta(minutes=30)
    return times

def submit_ride():
    """Handles ride request submission and redirects to fare estimation."""
    name = name_entry.get().strip()
    pickup = pickup_entry.get().strip()
    dropoff = dropoff_entry.get().strip()
    ride_type = ride_type_var.get().strip()
    
    # Get selected date and time
    selected_date = calendar.get_date().strftime("%Y-%m-%d")
    selected_time = time_var.get()
    preferred_datetime = f"{selected_date} {selected_time}"
    
    if not name or not pickup or not dropoff:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Insert ride request into the ride_requests table
        cursor.execute("""
            INSERT INTO ride_requests 
            (name, pickup, dropoff, ride_type, preferred_time, status) 
            VALUES (?, ?, ?, ?, ?, 'pending')
        """, (name, pickup, dropoff, ride_type, preferred_datetime))
        
        ride_id = cursor.lastrowid
        conn.commit()
        
        # Debug print
        print(f"Inserted ride request - ID: {ride_id}, From: {pickup}, To: {dropoff}")
        
        messagebox.showinfo("Success", "Ride Request Submitted Successfully!")

        # Define the path to fare_estimation.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        fare_script = os.path.join(script_dir, "fare_estimation.py")

        if not os.path.exists(fare_script):
            messagebox.showerror("Error", f"File not found: {fare_script}")
            return
        
        # Close the database connection before launching fare estimation
        conn.close()
        
        # Run fare_estimation.py
        subprocess.Popen([sys.executable, fare_script])
        
        # Close the booking window
        root.destroy()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to save ride request: {e}")
        if 'conn' in locals():
            conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        if 'conn' in locals():
            conn.close()

# Ensure the database structure is correct
ensure_database()

# Initialize main window
root = ctk.CTk()
root.title("Ride Request Form")
root.geometry("400x550")

# UI Components
ctk.CTkLabel(root, text="Name:").pack(pady=5)
name_entry = ctk.CTkEntry(root, width=300)
name_entry.pack(pady=5)

ctk.CTkLabel(root, text="Pickup Location:").pack(pady=5)
pickup_entry = ctk.CTkEntry(root, width=300)
pickup_entry.pack(pady=5)

ctk.CTkLabel(root, text="Drop-off Location:").pack(pady=5)
dropoff_entry = ctk.CTkEntry(root, width=300)
dropoff_entry.pack(pady=5)

ctk.CTkLabel(root, text="Ride Type:").pack(pady=5)
ride_type_var = tk.StringVar(value="Solo")
ctk.CTkRadioButton(root, text="Solo", variable=ride_type_var, value="Solo").pack()
ctk.CTkRadioButton(root, text="Shared", variable=ride_type_var, value="Shared").pack()

# Date and Time Selection
date_time_frame = ctk.CTkFrame(root)
date_time_frame.pack(pady=10, padx=10, fill="x")

ctk.CTkLabel(date_time_frame, text="Select Date:").pack(pady=5)
calendar = DateEntry(date_time_frame, width=12, background='darkblue',
                    foreground='white', borderwidth=2, mindate=datetime.now())
calendar.pack(pady=5)

ctk.CTkLabel(date_time_frame, text="Select Time:").pack(pady=5)
time_var = tk.StringVar(value=datetime.now().strftime("%I:%M %p"))
time_dropdown = ctk.CTkOptionMenu(date_time_frame, 
                                values=create_time_options(),
                                variable=time_var)
time_dropdown.pack(pady=5)

ctk.CTkButton(root, text="Request Ride", command=submit_ride).pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
