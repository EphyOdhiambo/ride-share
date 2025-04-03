import time
import folium
import requests
import threading
import openrouteservice
import webview  # To display the map inside a Tkinter window
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderInsufficientPrivileges, GeocoderTimedOut
import tkinter as tk
from tkinter import simpledialog

# 🔹 OpenRouteService API Key
ORS_API_KEY = "5b3ce3597851110001cf6248b22dc99cd40441b8abd8e36ef278e9c4"

# 🔹 Function to get coordinates from Nominatim (OpenStreetMap)
def get_coordinates(location):
    """ Convert location name to latitude & longitude with error handling """
    try:
        geolocator = Nominatim(user_agent="my_geolocation_app")
        time.sleep(1)  # Prevents rate-limiting
        location_data = geolocator.geocode(location, timeout=10)
        if location_data:
            return (location_data.latitude, location_data.longitude)
        else:
            print(f"❌ Error: Could not find coordinates for '{location}'")
            return None
    except GeocoderInsufficientPrivileges:
        print("❌ Geocoder Error: 403 Forbidden (Nominatim blocked your IP).")
        return None
    except GeocoderTimedOut:
        print("⚠️ Geocoder Timeout: Retrying...")
        return get_coordinates(location)
    except Exception as e:
        print(f"❌ Geocoding Error: {e}")
        return None

# 🔹 Function to get route from OpenRouteService
def get_route(pickup_coords, dropoff_coords):
    """ Fetches a route between two points using OpenRouteService """
    try:
        client = openrouteservice.Client(key=ORS_API_KEY)
        route = client.directions(
            coordinates=[(pickup_coords[1], pickup_coords[0]), (dropoff_coords[1], dropoff_coords[0])],
            profile='driving-car',
            format='geojson'
        )
        return route['features'][0]['geometry']['coordinates']  # Returns route points (lon, lat)
    except Exception as e:
        print(f"❌ Route Fetching Error: {e}")
        return None

# 🔹 Function to animate route
def animate_route(pickup, dropoff):
    """ Generates a live animated route with a blinking marker """

    pickup_coords = get_coordinates(pickup)
    dropoff_coords = get_coordinates(dropoff)

    if not pickup_coords or not dropoff_coords:
        print("❌ Error: Could not retrieve coordinates. Exiting...")
        return

    print(f"✅ Pickup: {pickup} → {pickup_coords}")
    print(f"✅ Dropoff: {dropoff} → {dropoff_coords}")

    # Get the route from OpenRouteService
    route_coords = get_route(pickup_coords, dropoff_coords)

    if not route_coords:
        print("❌ Error: Could not fetch the route.")
        return

    # Create folium map centered at pickup location
    m = folium.Map(location=pickup_coords, zoom_start=13)

    # Add static pickup and dropoff markers
    folium.Marker(pickup_coords, popup="Pickup", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(dropoff_coords, popup="Dropoff", icon=folium.Icon(color="red")).add_to(m)

    # Draw the route with a thick blue line
    folium.PolyLine(locations=[(lat, lon) for lon, lat in route_coords], color="blue", weight=6).add_to(m)

    # Moving marker
    moving_marker = folium.Marker(pickup_coords, popup="Moving...", icon=folium.Icon(color="blue"))
    m.add_child(moving_marker)

    # Save initial map
    m.save("animated_map.html")

    def update_map():
        """ Update the map dynamically without freezing the UI """
        num_steps = len(route_coords)

        for i in range(num_steps):
            lat, lon = route_coords[i][1], route_coords[i][0]
            moving_marker.location = (lat, lon)

            # Alternate colors for blinking effect
            if i % 2 == 0:
                moving_marker.icon = folium.Icon(color="blue")  # Visible
            else:
                moving_marker.icon = folium.Icon(color="white")  # Invisible

            # Save updated map
            m.save("animated_map.html")
            time.sleep(0.5)  # Controls animation speed

        print("✅ Animation complete!")

    # Run animation in a separate thread to prevent UI freezing
    threading.Thread(target=update_map, daemon=True).start()

    # Open the map in a WebView (inside Tkinter window)
    webview.create_window("Live Ride Animation", "animated_map.html")
    webview.start()

# 🔹 Create UI for user input
def start_ui():
    root = tk.Tk()
    root.title("Ride Details")

    tk.Label(root, text="Enter Pickup Location:").pack(pady=5)
    pickup_entry = tk.Entry(root, width=40)
    pickup_entry.pack(pady=5)

    tk.Label(root, text="Enter Dropoff Location:").pack(pady=5)
    dropoff_entry = tk.Entry(root, width=40)
    dropoff_entry.pack(pady=5)

    def start_ride():
        pickup_location = pickup_entry.get()
        dropoff_location = dropoff_entry.get()
        root.destroy()
        animate_route(pickup_location, dropoff_location)

    start_button = tk.Button(root, text="Start Ride", command=start_ride, bg="green", fg="white")
    start_button.pack(pady=10)

    root.mainloop()

# 🔹 Run the script
if __name__ == "__main__":
    start_ui()
