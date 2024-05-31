from dotenv import load_dotenv
import os
import googlemaps
from datetime import datetime

load_dotenv()

MAPS_API_KEY = os.environ.get('MAPS_API_KEY')

# Initialize Google Maps client
gmaps = googlemaps.Client(key=MAPS_API_KEY)


def fetch_place_details(place_name):
    geocode_result = gmaps.geocode(place_name)
    if not geocode_result:
        return None

    place_id = geocode_result[0]['place_id']
    place_details = gmaps.place(place_id=place_id)['result']

    details = {
        "name": place_details.get("name"),
        "address": place_details.get("formatted_address"),
        "phone_number": place_details.get("formatted_phone_number", None),
        "rating": place_details.get("rating", -1),
        "reviews": place_details.get("reviews", []),
        "latitude": place_details.get("geometry", {}).get("location", {}).get("lat"),
        "longitude": place_details.get("geometry", {}).get("location", {}).get("lng"),
        "geometry_type": place_details.get("geometry", {}).get("location_type"),
        "place_id": place_id,
        "types": place_details.get("types", []),
        "permanently_closed": place_details.get("permanently_closed", False),
        "price_level": place_details.get("price_level", "No price level available"),
        "opening_hours": place_details.get("opening_hours", {}).get("weekday_text", [])
    }
    return details


def fetch_vicinity_details(location, radius=1000, service_types=None):
    if service_types is None:
        service_types = ['restaurant']

    all_places = {}
    for service_type in service_types:
        # Perform a nearby search for each type of service
        places_result = gmaps.places_nearby(
            location=location, radius=radius, type=service_type)

        places = []
        for place in places_result.get('results', []):
            places.append({
                "name": place.get('name'),
                "address": place.get('vicinity'),
                "rating": place.get('rating', -1),
                "place_id": place.get('place_id'),
                "url": place.get('url', "No URL available"),
                "open_now": place.get('opening_hours', {}).get('open_now', False),
                "permanently_closed": place.get('permanently_closed', False)
            })
        all_places[service_type] = places

    return all_places
