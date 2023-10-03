from models import District, Area, Route, PostOffice, Address
from database import db
import requests


def fetch_from_api(url,params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            return data['results'][0]
    return None
def get_or_create_address(street_name, street_number, city, postal_code):
    address = Address.query.filter_by(street_name=street_name, street_number=street_number, city=city).first()
    if address:
        return address, False
    else:
        district_number = int(str(postal_code)[0])
        area_number = int(str(postal_code)[:2])
        route_number = int(str(postal_code)[:3])
        post_office_number = int(str(postal_code))

        district = District.query.filter_by(number=district_number).first()
        if not district:
            district = District(number=district_number)
            db.session.add(district)

        area = Area.query.filter_by(number=area_number).first()
        if not area:
            area = Area(number=area_number, district=district)
            db.session.add(area)

        route = Route.query.filter_by(number=route_number).first()
        if not route:
            route = Route(number=route_number, area=area)
            db.session.add(route)

        post_office = PostOffice.query.filter_by(number=post_office_number).first()
        if not post_office:
            post_office = PostOffice(number=post_office_number, route=route)
            db.session.add(post_office)

        searchText = f"{street_name} {street_number} {postal_code} {city}"
        search_url = f"https://api3.geo.admin.ch//rest/services/api/SearchServer"
        params = {
            'lang':'de',
            'searchText':searchText,
            'type':'locations',
            'sr':2056
        }
    
        matching_address = fetch_from_api(search_url,params)
        
        x, y, EGID = matching_address['attrs']['x'], matching_address['attrs']['y'], matching_address['attrs']['featureId']

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
        
        roof_info = fetch_from_api(identify_url,params)
        if roof_info is None:
            return False,None
        sonnendach_id = roof_info['featureId']

        new_address = Address(
            street_name=street_name,
            street_number=street_number,
            city=city,
            post_office=post_office,
            egid=EGID,
            sonnendach_id=sonnendach_id
        )
        db.session.add(new_address)
        db.session.commit()

        if not post_office.bfs:
            mapserver_url = f"https://api3.geo.admin.ch/rest/services/ech/MapServer/ch.bfs.gebaeude_wohnungs_register/{EGID}"
            mapserver_response = requests.get(mapserver_url).json()
            try:
                BFS = mapserver_response['feature']['attributes']['ggdenr']
            except:
                return False,None
            post_office.bfs = BFS
            db.session.commit()

        return new_address, True
