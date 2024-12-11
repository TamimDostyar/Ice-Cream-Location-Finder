import requests

API_KEY = "ZYCLMu7E4I28mgvHbILO4nJyehGiEu63YpxN1ig3ftP4P3P8V3b7Rw7xr38gd_gfNGI6CHtCl59wVfmLVNF0oht5HMK9G2gGhTYCNFi1hUUhxBxj1GZhJ25XK5NYZ3Yx"

YELP_API_URL = "https://api.yelp.com/v3/businesses/search"

def fetch_ice_cream_shops(location, term, radius, sort_by, limit):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    params = {
        "location": location,
        "term": term,
        "radius": radius,
        "sort_by": sort_by,
        "limit": limit
    }
    
    try:
        response = requests.get(YELP_API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Yelp API: {e}")
        return None

if __name__ == "__main__":
    location = "Decorah"
    term = "ice cream"
    radius = 20000
    sort_by = "best_match"
    limit = 20

    shops = fetch_ice_cream_shops(location, term, radius, sort_by, limit)
    if shops:
        print("Ice Cream Shops Found:")
        for business in shops.get("businesses", []):
            name = business.get("name", "N/A")
            address = ", ".join(business["location"].get("display_address", []))
            rating = business.get("rating", "N/A")
            image_url = business.get("image_url", "No Image Available")

            print(f"Name: {name}")
            print(f"Address: {address}")
            print(f"Rating: {rating} stars")
            print(f"Image URL: {image_url}")
            print("-" * 40)
