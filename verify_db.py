import sqlite3
import os

# Define the base directory where your databases are stored
BASE_DIR = "C:/Users/GILBERT PC/Desktop/Software Development/Module II"

# Function to check table data
def check_table_data(db_name, table_name):
    db_path = os.path.join(BASE_DIR, db_name)

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch all data from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    records = cursor.fetchall()

    print(f"\n📌 Data from {db_name} - {table_name}:")
    if records:
        for row in records:
            print(row)
    else:
        print("⚠️ No data found!")

    conn.close()

# Function to check how many users are logged in
def count_logged_in_users():
    db_path = os.path.join(BASE_DIR, "user.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'logged_in'")
    result = cursor.fetchone()[0]
    
    conn.close()
    print(f"✅ Logged-in users: {result}")

# Function to check how many rides are active
def count_active_rides():
    db_path = os.path.join(BASE_DIR, "rides.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM rides WHERE status = 'active'")
    result = cursor.fetchone()[0]

    conn.close()
    print(f"✅ Active Rides: {result}")

# Function to check pending ride requests
def count_pending_requests():
    db_path = os.path.join(BASE_DIR, "rides.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM rides WHERE status = 'pending'")
    result = cursor.fetchone()[0]

    conn.close()
    print(f"✅ Pending ride requests: {result}")

# Function to check column names in a table
def check_columns(db_name, table_name):
    db_path = os.path.join(BASE_DIR, db_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    print(f"\n📌 Columns in {table_name}:")
    for col in columns:
        print(col)

    conn.close()

# Run the verification functions
if __name__ == "__main__":
    print("\n🔎 Checking Database Integrity...\n")
    
    # Check data in the users and rides tables
    check_table_data("user.db", "users")
    check_table_data("rides.db", "rides")

    # Check counts
    count_logged_in_users()
    count_active_rides()
    count_pending_requests()

    # Check column names
    check_columns("user.db", "users")
    check_columns("rides.db", "rides")

    print("\n✅ Database verification completed!\n")
