from models import District, Area, Route, PostOffice, Address
from database import db
import requests
from api_utils import fetch_from_api



def add_to_db(item):
    db.session.add(item)
    db.session.commit()

def update_db():
    db.session.commit()

def retrieve_from_db(model, **filters):
    return model.query.filter_by(**filters).first()

def get_or_create_address(street_name, street_number, city, postal_code):
    address = retrieve_from_db(Address, street_name=street_name, street_number=street_number, city=city)
    if address:
        return address, False
    else:
        district = retrieve_from_db(District, number=int(str(postal_code)[0]))
        if not district:
            district = District(number=int(str(postal_code)[0]))
            add_to_db(district)

        area = retrieve_from_db(Area, number=int(str(postal_code)[:2]))
        if not area:
            area = Area(number=int(str(postal_code)[:2]), district=district)
            add_to_db(area)

        route = retrieve_from_db(Route, number=int(str(postal_code)[:3]))
        if not route:
            route = Route(number=int(str(postal_code)[:3]), area=area)
            add_to_db(route)

        post_office = retrieve_from_db(PostOffice, number=int(postal_code))
        if not post_office:
            post_office = PostOffice(number=int(postal_code), route=route)
            add_to_db(post_office)

        searchText = f"{street_name} {street_number} {postal_code} {city}"
        search_url = f"https://api3.geo.admin.ch//rest/services/api/SearchServer"
        params = {
            'lang': 'de',
            'searchText': searchText,
            'type': 'locations',
            'sr': 2056
        }

        matching_address = fetch_from_api(search_url, params)

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

        roof_info = fetch_from_api(identify_url, params)
        if roof_info is None:
            return None, False

        sonnendach_id = roof_info['featureId']

        new_address = Address(
            street_name=street_name,
            street_number=street_number,
            city=city,
            post_office=post_office,
            egid=EGID,
            sonnendach_id=sonnendach_id
        )
        add_to_db(new_address)

        if not post_office.bfs:
            mapserver_url = f"https://api3.geo.admin.ch/rest/services/ech/MapServer/ch.bfs.gebaeude_wohnungs_register/{EGID}"
            mapserver_response = requests.get(mapserver_url).json()
            try:
                BFS = mapserver_response['feature']['attributes']['ggdenr']
            except:
                return None, False
            post_office.bfs = BFS
            update_db()

        return new_address, True