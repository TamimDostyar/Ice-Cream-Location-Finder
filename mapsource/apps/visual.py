import folium
import requests
from geopy.geocoders import Nominatim

# Initialize the geolocator
loc = Nominatim(user_agent="GetLoc")

# Geocode Decorah, Iowa to get location data
getLoc = loc.geocode("Decorah, Iowa")

# Extract latitude and longitude from the location data
latitude = getLoc.latitude
longitude = getLoc.longitude

# Google Places API key
api_key = "YOUR_GOOGLE_PLACES_API_KEY"

# Search for ice cream shops in Decorah
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
params = {
    "location": f"{latitude},{longitude}",
    "radius": 5000,  # radius in meters
    "type": "food",
    "keyword": "ice cream",
    "key": api_key,
}

response = requests.get(url, params=params)
places = response.json().get("results", [])

# Create a Folium map centered on Decorah
myLocation = folium.Map(location=[latitude, longitude], zoom_start=14)

# Add each ice cream shop to the map
for place in places:
    lat = place["geometry"]["location"]["lat"]
    lng = place["geometry"]["location"]["lng"]
    name = place["name"]
    folium.Marker(
        location=[lat, lng],
        popup=name,
        icon=folium.Icon(icon="cloud"),
    ).add_to(myLocation)

# Save the map to an HTML file
myLocation.save("mapsource/templates/maps.html")

print(f"Map with {len(places)} ice cream shops has been created.")
