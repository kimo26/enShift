import requests
def fetch_from_api(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            return data['results'][0]
    return None

def fetch_address_from_geo_admin(street_name, street_number, postal_code, city):
    search_url = "https://api3.geo.admin.ch//rest/services/api/SearchServer"
    params = {
        'lang': 'de',
        'searchText': f"{street_name} {street_number} {postal_code} {city}",
        'type': 'locations',
        'sr': 2056
    }
    return fetch_from_api(search_url, params)

def fetch_roof_info_from_geo_admin(x, y):
    identify_url = "https://api3.geo.admin.ch/rest/services/api/MapServer/identify"
    params = {
        'geometryType': 'esriGeometryPoint',
        'returnGeometry': 'true',
        'layers': 'all:ch.bfe.solarenergie-eignung-daecher',
        'geometry': f"{y},{x}",
        'tolerance': 0,
        'order': 'distance',
        'lang': 'de',
        'sr': 2056
    }
    return fetch_from_api(identify_url, params)

def fetch_building_info_from_geo_admin(EGID):
    mapserver_url = f"https://api3.geo.admin.ch/rest/services/ech/MapServer/ch.bfs.gebaeude_wohnungs_register/{EGID}"
    return fetch_from_api(mapserver_url, {})