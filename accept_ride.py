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

# Function to accept a ride
def accept_ride():
    selected_item = ride_table.selection()
    
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a ride to accept.")
        return
    
    item_values = ride_table.item(selected_item)['values']
    if not item_values:
        messagebox.showwarning("Invalid Selection", "Selected ride data is missing.")
        return
    
    rider_name = item_values[0]
    
    # Update database to mark the ride as accepted
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE ride_requests SET status = 'accepted' WHERE name = ?", (rider_name,))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Ride Accepted", f"You have accepted the ride for {rider_name}!")
    populate_ride_table()

# Function to cancel a ride (Deletes the entry from the database)
def cancel_ride():
    selected_item = ride_table.selection()
    
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a ride to cancel.")
        return
    
    item_values = ride_table.item(selected_item)['values']
    if not item_values:
        messagebox.showwarning("Invalid Selection", "Selected ride data is missing.")
        return
    
    rider_name = item_values[0]
    
    # Delete the ride request from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ride_requests WHERE name = ?", (rider_name,))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Ride Canceled", f"The ride request for {rider_name} has been deleted.")
    populate_ride_table()

# Initialize main window
root = ctk.CTk()
root.title("Driver Dashboard - Ride Bookings")
root.geometry("700x450")

# UI Title
title_label = ctk.CTkLabel(root, text="Ride Booking Requests", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Table to show ride bookings
columns = ("Rider", "Pickup", "Dropoff", "Ride Type", "Preferred Time", "Status")
ride_table = ttk.Treeview(root, columns=columns, show="headings")
ride_table.pack(pady=10, fill="both", expand=True)

# Define column headings
for col in columns:
    ride_table.heading(col, text=col)
    ride_table.column(col, anchor="center")

# Accept Ride Button
accept_btn = ctk.CTkButton(root, text="Accept Ride", command=accept_ride)
accept_btn.pack(pady=10)

# Cancel Ride Button
cancel_btn = ctk.CTkButton(root, text="Cancel Ride", command=cancel_ride, fg_color="red", hover_color="darkred")
cancel_btn.pack(pady=10)

# Populate the table with ride data
populate_ride_table()

# Run the main event loop
root.mainloop()
