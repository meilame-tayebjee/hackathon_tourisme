import math
from itertools import permutations
class RouteOptimizer:
    @staticmethod
    def haversine_distance(loc1, loc2):
        """Calculate geographical distance between two locations."""
        R = 6371  # Earth radius in kilometers
        lat1, lon1 = loc1['latitude'], loc1['longitude']
        lat2, lon2 = loc2['latitude'], loc2['longitude']
        
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = (math.sin(dLat/2)**2 + 
             math.cos(math.radians(lat1)) * 
             math.cos(math.radians(lat2)) * 
             math.sin(dLon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R*c

    @classmethod
    def nearest_neighbor_route(cls, locations):
        """Optimize route using Nearest Neighbor algorithm, starting from 'start'."""
        # Separate start location
        start = next(loc for loc in locations if loc[0] == 'start')
        other_locations = [loc for loc in locations if loc[0] != 'start']
        
        route = [start]  # Start with 'start' location
        unvisited = other_locations.copy()
        
        while unvisited:
            current = route[-1][1]
            nearest = min(unvisited, key=lambda loc: cls.haversine_distance(current, loc[1]))
            route.append(nearest)
            unvisited.remove(nearest)
        
        return route

    @classmethod
    def calculate_total_route_distance(cls, route):
        """Calculate total route distance."""
        res = [cls.haversine_distance(route[i][1], route[i+1][1]) 
                   for i in range(len(route)-1)]
        res.append(0)
        return res

def optimize_route(locations):
    # Ensure 'start' is in the locations
    if not any(loc[0] == 'start' for loc in locations):
        raise ValueError("No 'start' location found in the input locations")
    
    # Full permutation approach (for small number of locations), 
    # but always keep 'start' as the first location
    start = next(loc for loc in locations if loc[0] == 'start')
    if len(locations) <= 7:  # Increased to account for 'start'
        # Get non-start locations
        non_start_locations = [loc for loc in locations if loc[0] != 'start']
        
        # Generate all permutations of non-start locations
        best_route = min(
            [[start] + list(perm) for perm in permutations(non_start_locations)], 
            key=lambda route: sum(RouteOptimizer.haversine_distance(route[i][1], route[i+1][1]) 
                                  for i in range(len(route)-1))
        )
    else:
        # Nearest neighbor for larger sets
        best_route = RouteOptimizer.nearest_neighbor_route(locations)
    
    # Create detailed route information
    route_info = []
    distance_per_step = RouteOptimizer.calculate_total_route_distance(best_route)
    total_distance = sum(distance_per_step)
    
    for location in best_route:
        # Find original location details
        original_entry = location[0]
        original_details = location[1]
        
        route_info.append({
            'name': original_entry,
            'rating': original_details.get('rating'),
            'total_ratings': original_details.get('total_ratings'),
            'address': original_details.get('address'),
            'distance_till_next': distance_per_step.pop(0)
        })
    
    return {
        'optimized_route': route_info,
        'total_distance': total_distance
    }