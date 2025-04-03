import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
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

# Function to delete multiple rides from history
def delete_rides():
    selected_items = ride_table.selection()
    
    if not selected_items:
        messagebox.showwarning("No Selection", "Please select one or more rides to delete from history.")
        return
    
    ride_names = [ride_table.item(item)['values'][0] for item in selected_items if ride_table.item(item)['values']]
    
    if not ride_names:
        messagebox.showwarning("Invalid Selection", "Selected ride data is missing.")
        return
    
    # Delete selected ride requests from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany("DELETE FROM ride_requests WHERE name = ?", [(name,) for name in ride_names])
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Rides Deleted", f"Selected ride history has been removed.")
    populate_ride_table()

# Initialize main window
root = ctk.CTk()
root.title("Admin Dashboard - Ride History")
root.geometry("700x450")

# UI Title
title_label = ctk.CTkLabel(root, text="Ride History", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Table to show ride history
columns = ("Rider", "Pickup", "Dropoff", "Ride Type", "Preferred Time", "Status")
ride_table = ttk.Treeview(root, columns=columns, show="headings", selectmode="extended")
ride_table.pack(pady=10, fill="both", expand=True)

# Define column headings
for col in columns:
    ride_table.heading(col, text=col)
    ride_table.column(col, anchor="center")

# Delete Ride History Button
delete_btn = ctk.CTkButton(root, text="Delete Ride History", command=delete_rides, fg_color="red", hover_color="darkred")
delete_btn.pack(pady=10)

# Populate the table with ride data
populate_ride_table()

# Run the main event loop
root.mainloop()
