import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import os

# Get the base directory
BASE_DIR = "C:/Users/GILBERT PC/Desktop/Software Development/Module II"
DB_PATH = os.path.join(BASE_DIR, "rides.db")
DASHBOARD_PATH = os.path.join(BASE_DIR, "dashboards", "driver_dashboard.py")

# Ensure 'car_number' column exists and remove 'car_details' if needed
def ensure_database_integrity():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the driver table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS driver (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            license TEXT NOT NULL,
            car_number TEXT DEFAULT 'NOT PROVIDED'
        )
    """)
    conn.commit()

    cursor.execute("PRAGMA table_info(driver);")
    columns = [column[1] for column in cursor.fetchall()]

    if "car_number" not in columns:
        cursor.execute("ALTER TABLE driver ADD COLUMN car_number TEXT DEFAULT 'NOT PROVIDED';")
        conn.commit()
        print("Column 'car_number' added successfully!")

    if "car_details" in columns:
        # Create a new table without 'car_details'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS driver_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                license TEXT NOT NULL,
                car_number TEXT DEFAULT 'NOT PROVIDED'
            )
        """)
        
        # Update any NULL car_number values in the old table
        cursor.execute("UPDATE driver SET car_number = 'NOT PROVIDED' WHERE car_number IS NULL")
        
        # Copy data from old table
        cursor.execute("INSERT INTO driver_new (id, name, email, license, car_number) SELECT id, name, email, license, COALESCE(car_number, 'NOT PROVIDED') FROM driver")

        # Drop old table and rename new table
        cursor.execute("DROP TABLE driver")
        cursor.execute("ALTER TABLE driver_new RENAME TO driver")
        conn.commit()
        print("Column 'car_details' removed successfully!")

    conn.close()

# Function to handle driver signup and open dashboard after signup
def authenticate_driver():
    def submit():
        name = entry_name.get().strip()
        email = entry_email.get().strip()
        license = entry_license.get().strip()
        car_number = entry_car_number.get().strip()

        if not (name and email and license and car_number):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            conn = sqlite3.connect(DB_PATH, timeout=10)
            cursor = conn.cursor()

            # Check if email already exists
            cursor.execute("SELECT * FROM driver WHERE email = ?", (email,))
            existing_driver = cursor.fetchone()

            if existing_driver:
                messagebox.showerror("Error", "Email already registered! Use a different email.")
            else:
                # Insert new driver record
                cursor.execute("INSERT INTO driver (name, email, license, car_number) VALUES (?, ?, ?, ?)",
                               (name, email, license, car_number))
                conn.commit()
                messagebox.showinfo("Signup Successful", "You have been registered successfully!")
                
                popup.destroy()  # Close the signup window
                open_driver_dashboard()  # Open the dashboard after signup

        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

    # Create a popup window
    popup = tk.Tk()
    popup.title("Driver Signup")
    popup.geometry("400x300")

    # Labels and Entry Fields
    tk.Label(popup, text="Name:").pack(pady=5)
    entry_name = tk.Entry(popup)
    entry_name.pack(pady=5)

    tk.Label(popup, text="Email:").pack(pady=5)
    entry_email = tk.Entry(popup)
    entry_email.pack(pady=5)

    tk.Label(popup, text="License:").pack(pady=5)
    entry_license = tk.Entry(popup)
    entry_license.pack(pady=5)

    tk.Label(popup, text="Car Number:").pack(pady=5)
    entry_car_number = tk.Entry(popup)
    entry_car_number.pack(pady=5)

    # Submit Button (Blue Color) - Now performs signup instead of login
    submit_btn = tk.Button(popup, text="Signup", command=submit, bg="blue", fg="white", font=("Arial", 12, "bold"))
    submit_btn.pack(pady=15)

    popup.mainloop()

# Function to open driver dashboard
def open_driver_dashboard():
    try:
        subprocess.run(f'python "{DASHBOARD_PATH}"', shell=True)
    except Exception as e:
        print(f"Error opening driver dashboard: {e}")

# Run setup and start authentication process
if __name__ == "__main__":
    ensure_database_integrity()  # Ensure the database is correctly structured
    authenticate_driver()
