import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import sqlite3
import subprocess
import requests
import json

DB_PATH = "rides.db"
ORS_API_KEY = "5b3ce3597851110001cf6248b22dc99cd40441b8abd8e36ef278e9c4"

def fetch_latest_ride():
    """Fetches the most recent ride request from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT r.*, datetime('now', 'localtime') as request_time
            FROM ride_requests r
            ORDER BY r.id DESC 
            LIMIT 1
        """)
        ride = cursor.fetchone()
        if ride:
            print(f"Debug - Latest ride data: {ride}")
        return ride
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()

def get_coordinates(location):
    """Get coordinates for a location using ORS Geocoding API"""
    url = f"https://api.openrouteservice.org/geocode/search?api_key={ORS_API_KEY}&text={location}, Kenya&country=KE"
    try:
        response = requests.get(url)
        data = response.json()
        if data['features']:
            coordinates = data['features'][0]['geometry']['coordinates']
            return coordinates  # Returns [longitude, latitude]
    except Exception as e:
        print(f"Error getting coordinates for {location}: {e}")
    return None

def calculate_real_distance(pickup, dropoff):
    """Calculate real distance using ORS Directions API"""
    pickup_coords = get_coordinates(pickup)
    dropoff_coords = get_coordinates(dropoff)
    
    if pickup_coords and dropoff_coords:
        url = "https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {
            'Authorization': ORS_API_KEY,
            'Content-Type': 'application/json'
        }
        body = {
            "coordinates": [pickup_coords, dropoff_coords],
            "units": "km"
        }
        
        try:
            response = requests.post(url, json=body, headers=headers)
            data = response.json()
            distance = (data['routes'][0]['summary']['distance'])
            return round(distance, 2)
        except Exception as e:
            print(f"Error calculating distance: {e}")
            return get_fallback_distance(pickup, dropoff)
    return get_fallback_distance(pickup, dropoff)

def get_fallback_distance(pickup, dropoff):
    """Fallback to predefined realistic distances"""
    location_distances = {
        ('naivasha', 'nakuru'): 87,
        ('nyeri', 'mombasa'): 450,
        ('nairobi', 'kisumu'): 340,
        ('nakuru', 'nairobi'): 158,
        ('mombasa', 'nyeri'): 450,
        ('kisumu', 'nairobi'): 340,
        ('nairobi', 'nakuru'): 158,
        ('nairobi', 'mombasa'): 485,
        ('nakuru', 'eldoret'): 172,
        ('nairobi', 'naivasha'): 92,
        ('thika', 'nairobi'): 45,
        ('machakos', 'nairobi'): 63,
        ('nairobi', 'kitui'): 169,
        ('meru', 'nairobi'): 275,
        ('nakuru', 'kisumu'): 185
    }
    
    pickup_lower = pickup.lower().strip()
    dropoff_lower = dropoff.lower().strip()
    
    distance = location_distances.get((pickup_lower, dropoff_lower)) or \
              location_distances.get((dropoff_lower, pickup_lower))
    
    if not distance:
        print(f"No predefined distance for {pickup} to {dropoff}, using estimate")
        return 150  # Default reasonable distance
    
    return distance

def calculate_fare(ride_type, pickup, dropoff):
    base_fare = 600  # Base fare in Ksh
    
    distance = calculate_real_distance(pickup, dropoff)
    print(f"Calculated distance: {distance} km")  # Debug print
    
    ride_type_multiplier = 1.5 if ride_type == "Solo" else 1.2
    
    rate_per_km = 5  # Ksh per kilometer
    fare = base_fare + (distance * rate_per_km) * ride_type_multiplier
    return round(fare, 2), round(distance, 2)

def save_estimated_fare(fare):
    """Save the estimated fare to the database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Update the latest ride request with the estimated fare
        cursor.execute("""
            UPDATE ride_requests 
            SET estimated_fare = ? 
            WHERE id = (SELECT id FROM ride_requests ORDER BY id DESC LIMIT 1)
        """, (fare,))
        
        conn.commit()
        conn.close()
        print(f"Saved fare to database: Ksh {fare}")
    except sqlite3.Error as e:
        print(f"Error saving fare: {e}")

def confirm_fare():
    """Save fare and proceed to payment"""
    try:
        # Save the current fare to the database
        save_estimated_fare(fare)  # fare is from the outer scope
        messagebox.showinfo("Confirmed", "Fare confirmed! Proceeding to payment...")
        root.destroy()
        subprocess.Popen(["python", "ephy/mpesa.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process fare: {e}")

# UI Setup
root = ctk.CTk()
root.title("AI-Powered Fare Estimation")
root.geometry("400x400")

# Create a frame for better organization
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

ride_data = fetch_latest_ride()
if ride_data:
    name = ride_data[1]
    pickup = ride_data[2]
    dropoff = ride_data[3]
    ride_type = ride_data[4]
    
    print(f"Processing ride - Name: {name}, From: {pickup}, To: {dropoff}, Type: {ride_type}")
    
    fare, distance = calculate_fare(ride_type, pickup, dropoff)
    
    # Display ride details
    ctk.CTkLabel(frame, text="Ride Details", font=("Arial", 20, "bold")).pack(pady=10)
    ctk.CTkLabel(frame, text=f"Hello {name},", font=("Arial", 18, "bold")).pack(pady=5)
    ctk.CTkLabel(frame, text=f"Pickup: {pickup}", font=("Arial", 14)).pack(pady=5)
    ctk.CTkLabel(frame, text=f"Drop-off: {dropoff}", font=("Arial", 14)).pack(pady=5)
    ctk.CTkLabel(frame, text=f"Ride Type: {ride_type}", font=("Arial", 14)).pack(pady=5)
    ctk.CTkLabel(frame, text=f"Estimated Distance: {distance} km", font=("Arial", 14)).pack(pady=5)
    ctk.CTkLabel(frame, text=f"💰 AI-Estimated Fare: Ksh {fare}", 
                 font=("Arial", 22, "bold"), text_color="green").pack(pady=10)

    ctk.CTkButton(frame, text="Confirm Fare", command=confirm_fare).pack(pady=20)
else:
    ctk.CTkLabel(frame, text="No ride request found!", font=("Arial", 16, "bold")).pack(pady=20)

root.mainloop()
