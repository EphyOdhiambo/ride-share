import sqlite3
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

DB_PATH = "rides.db"

# Function to fetch all ride requests from the database
def fetch_all_rides():
    """Fetches all ride requests from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, pickup, dropoff, ride_type, preferred_time, status FROM ride_requests")
    rides = cursor.fetchall()
    conn.close()
    return rides

# Function to update the table with ride data
def populate_ride_table():
    """Clears and populates the ride table with all rides."""
    for item in ride_table.get_children():
        ride_table.delete(item)
    
    all_rides = fetch_all_rides()
    for ride in all_rides:
        ride_table.insert("", "end", values=ride)

# Initialize main window
root = ctk.CTk()
root.title("Passenger Dashboard - Ride History")
root.geometry("700x450")

# UI Title
title_label = ctk.CTkLabel(root, text="Ride History", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Table to show ride history
columns = ("Rider", "Pickup", "Dropoff", "Ride Type", "Preferred Time", "Status")
ride_table = ttk.Treeview(root, columns=columns, show="headings", selectmode="browse")
ride_table.pack(pady=10, fill="both", expand=True)

# Define column headings
for col in columns:
    ride_table.heading(col, text=col)
    ride_table.column(col, anchor="center")

# Populate the table with ride data
populate_ride_table()

# Run the main event loop
root.mainloop()
