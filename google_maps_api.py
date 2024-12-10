import requests
import os
from typing import Dict, Any

def sort_locations(data, min_rating=3.5, min_total_ratings=200):
    # Filter locations with rating above min_rating and valid total ratings
    filtered_locations = {
        name: info for name, info in data.items() 
        if isinstance(info.get('rating'), (int, float)) and 
           info['rating'] >= min_rating and 
           isinstance(info.get('total_ratings'), int) and
              info['total_ratings'] >= min_total_ratings
    }
    
    # Sort locations by total ratings in descending order and get top 10
    top_locations = sorted(
        filtered_locations.items(), 
        key=lambda x: x[1]['total_ratings'], 
        reverse=True
    )
    
    return top_locations


class GoogleMapsVisitorRetriever:
    def __init__(self, api_key: str, top_k = 5):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        self.top_k = top_k

    def get_place_details(self, place_name: str, location: Dict[str, float]) -> Dict[str, Any]:
        """
        Retrieve place details including ratings and visitor information
        
        :param place_name: Name of the location
        :param location: Dictionary with 'lat' and 'lon' keys
        :return: Place details dictionary
        """
        params = {
            'key': self.api_key,
            'query': f'{place_name}',
            'location': f"{location['lat']},{location['lon']}",
            'radius': 1000  # Search within 1km radius
        }

        response = requests.get(self.base_url, params=params)
        return response.json()

    def process_locations(self, locations):
        """
        Process multiple locations from OpenStreetMap data
        
        :param locations: List of location dictionaries
        :return: Dictionary of visitor data
        """
        visitor_data = {}
        for location in locations:
            if 'name' in location['tags']:
                name = location['tags']['name']
                try:
                    details = self.get_place_details(
                        name, 
                        {'lat': location['lat'], 'lon': location['lon']}
                    )
                    
                    # Extract first result if available
                    result = details.get('results', [{}])[0]
                    
                    visitor_data[name] = {
                        'rating': result.get('rating', 'N/A'),
                        'total_ratings': result.get('user_ratings_total', 'N/A'),
                        'address': result.get('formatted_address', 'N/A'),
                        'longitude': location['lon'],
                        'latitude': location['lat']
                    }
                except Exception as e:
                    visitor_data[name] = {'error': str(e)}
        visitor_data = sort_locations(visitor_data)
        return visitor_data