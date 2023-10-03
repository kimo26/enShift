import requests

def fetch_from_api(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            return data['results'][0]
    return None

def fetch_matching_address(searchText):
    search_url = "https://api3.geo.admin.ch//rest/services/api/SearchServer"
    params = {
        'lang': 'de',
        'searchText': searchText,
        'type': 'locations',
        'sr': 2056
    }
    return fetch_from_api(search_url, params)

def fetch_roof_info(x, y):
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
