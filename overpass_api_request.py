import overpy
import json


def queryOverpassAPI(api, entry_point, radius):
    radius_km = int(radius * 1e3)
    res = api.query(f"[out:json];node(around:{radius_km},{entry_point[0]}, {entry_point[1]})[tourism][tourism != 'hotel'][tourism != 'restaurant'][tourism != 'guest_house'][tourism != 'hostel'][wheelchair]; out;")
    parsed_res = parse_overpy_result(res)
    return parsed_res


def parse_overpy_result(res):
    results = []

    # Iterate through all nodes in the result
    for node in res.nodes:
        formatted_node = {
            "type": "node",
            "id": float(node.id),
            "lat": float(node.lat),
            "lon": float(node.lon),
            "tags": node.tags  # Tags are already a dictionary in Overpy
        }
        results.append(formatted_node)

    return results