import os
from flask import Flask, request, jsonify
import overpy
import openai
import math

# Assurez-vous de mettre votre clé OpenAI ici ou dans vos variables d'environnement
openai.api_key = os.environ.get("OPENAI_API_KEY", "VOTRE_CLE_API_OPENAI")

app = Flask(__name__)

def queryOverpassAPI(api, entry_point, radius):
    radius_km = int(radius * 1e3)
    # Ici, on recherche les nodes "tourism" (mais pas hotel/restaurant/guest_house/hostel) et qui ont wheelchair
    query = f"""
    [out:json];
    node(around:{radius_km},{entry_point[0]},{entry_point[1]})
    [tourism][tourism != 'hotel'][tourism != 'restaurant'][tourism != 'guest_house'][tourism != 'hostel']
    [wheelchair];
    out;
    """
    res = api.query(query)
    return res

def parse_overpy_result(res):
    results = []
    for node in res.nodes:
        formatted_node = {
            "type": "node",
            "id": float(node.id),
            "lat": float(node.lat),
            "lon": float(node.lon),
            "tags": node.tags
        }
        results.append(formatted_node)
    return results

def build_prompt(startLat, startLon, pois):
    # Générer un prompt pour OpenAI à partir des POI récupérés
    # Le prompt demandera un ordre cohérent minimisant la distance étape par étape.
    prompt = f"""
Tu es un assistant. On te donne une position de départ (latitude, longitude) et une liste de points d'intérêt (avec nom, lat, lon).
Ta tâche : Déterminer l'ordre de visite le plus logique pour minimiser la distance à chaque étape, en commençant par la position de départ.

Position de départ:
Lat: {startLat}
Lon: {startLon}

Points d'intérêt:
"""
    for i, poi in enumerate(pois, start=1):
        name = poi['tags'].get('name', f"POI {i}")
        lat = poi['lat']
        lon = poi['lon']
        prompt += f"{i}. {name} ({lat}, {lon})\n"

    prompt += """
Donne-moi l'ordre des lieux sous la forme d'une liste ordonnée avec les noms des lieux.
"""
    return prompt

def call_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Tu es un assistant utile."},
                  {"role": "user", "content": prompt}],
        max_tokens=1500,
        temperature=0
    )
    return response.choices[0].message.content

@app.route('/api/itinerary', methods=['POST'])
def get_itinerary():
    data = request.get_json()
    startLat = data.get('startLat')
    startLon = data.get('startLon')
    radius = data.get('radius', 5)  # rayon par défaut 5 km si non fourni

    if not startLat or not startLon:
        return jsonify({"error": "startLat and startLon required"}), 400

    try:
        startLat = float(startLat)
        startLon = float(startLon)
        radius = float(radius)
    except ValueError:
        return jsonify({"error": "Invalid coordinates or radius"}), 400

    # Query Overpass
    api = overpy.Overpass()
    res = queryOverpassAPI(api, (startLat, startLon), radius)
    pois = parse_overpy_result(res)

    if not pois:
        return jsonify({"error": "No POI found"}), 404

    # Construire le prompt pour OpenAI
    prompt = build_prompt(startLat, startLon, pois)
    # Appel à OpenAI
    route = call_openai(prompt)

    return jsonify({"route": route})

if __name__ == '__main__':
    # Lancer le serveur Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
