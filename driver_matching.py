import sqlite3

DB_PATH = "ride_share.db"

def run_sql_command():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Run SQL commands to add missing columns
    cursor.execute("PRAGMA table_info(drivers);")
    columns = [col[1] for col in cursor.fetchall()]

    if "latitude" not in columns:
        cursor.execute("ALTER TABLE drivers ADD COLUMN latitude REAL DEFAULT 0.0;")
    if "longitude" not in columns:
        cursor.execute("ALTER TABLE drivers ADD COLUMN longitude REAL DEFAULT 0.0;")

    conn.commit()
    conn.close()
    print("Database updated successfully!")

# Run this function once
run_sql_command()
