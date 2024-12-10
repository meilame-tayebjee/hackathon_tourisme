import os
import overpy
import argparse

from .overpass_api_request import queryOverpassAPI
from .google_maps_api import GoogleMapsVisitorRetriever
from .route_optimizer import optimize_route

def launch(api_key, start_lat, start_lon, radius=20, top_k=5):

    api = overpy.Overpass()
    res = queryOverpassAPI(api, [start_lat, start_lon], radius = radius)

    # Usage example
    retriever = GoogleMapsVisitorRetriever(api_key, top_k=top_k)
    # Assume 'locations' is the list from the original data
    visitor_frequencies = retriever.process_locations(res)

    visitor_frequencies.append(('start', {'latitude':start_lat, 'longitude':start_lon, 
    'rating':None, 'total_ratings':None, 'address':None, 'distance_till_next':None}))

    print(visitor_frequencies)

    final_route = optimize_route(visitor_frequencies)

    return final_route

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--api_key",
        type=str,
    )
    parser.add_argument(
        "--starting_lat",
        type=float,
    )
    parser.add_argument(
        "--starting_lon",
        type=float,
    )
    parser.add_argument(
        "--radius",
        type=float,
        default=20,
    )
    parser.add_argument(
        "--top_k",
        type=int,
        default=5,
    )

    args = parser.parse_args()
    api_key = args.api_key
    start_lat = args.starting_lat
    start_lon = args.starting_lon
    radius = args.radius
    top_k = args.top_k

    final_route = launch(api_key, start_lat, start_lon, radius, top_k)
    print(final_route)
