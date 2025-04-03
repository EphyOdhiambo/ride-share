import sqlite3

# Connect to SQLite Database
conn = sqlite3.connect("rideshare.db")
cursor = conn.cursor()

# Add missing columns if they do not exist
try:
    cursor.execute("ALTER TABLE drivers ADD COLUMN latitude REAL")
    cursor.execute("ALTER TABLE drivers ADD COLUMN longitude REAL")
    print("Columns latitude and longitude added successfully!")
except sqlite3.OperationalError:
    print("Columns already exist or cannot be added.")

# Commit and Close
conn.commit()
conn.close()
