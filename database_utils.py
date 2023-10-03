from models import District, Area, Route, PostOffice, Address
from database import db
import api_utils as api
from exceptions import DatabaseError, RecordNotFoundError


def add_to_db(item):
    try:
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        raise DatabaseError(f"Error adding to database: {str(e)}")

def update_db():
    try:
        db.session.commit()
    except Exception as e:
        raise DatabaseError(f"Error updating database: {str(e)}")

def retrieve_from_db(model, **filters):
    record = model.query.filter_by(**filters).first()
    if not record:
        raise RecordNotFoundError(f"{model.__name__} not found with filters: {filters}")
    return record
def get_or_create(model, defaults=None, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        params = dict(kwargs)
        params.update(defaults or {})
        instance = model(**params)
        add_to_db(instance)
        return instance
    
def get_or_create_address(street_name, street_number, city, postal_code):
        
    address = retrieve_from_db(Address, street_name=street_name, street_number=street_number, city=city)
    if address:
        return address, False
    else:
        district = get_or_create(District, number=int(str(postal_code)[0]))
        area = get_or_create(Area, defaults={'district': district}, number=int(str(postal_code)[:2]))
        route = get_or_create(Route, defaults={'area': area}, number=int(str(postal_code)[:3]))
        post_office = get_or_create(PostOffice, defaults={'route': route}, number=int(postal_code))


        matching_address = api.fetch_address_from_geo_admin(street_name, street_number, postal_code, city)
        x, y, EGID = matching_address['attrs']['x'], matching_address['attrs']['y'], matching_address['attrs']['featureId']

        roof_info = api.fetch_roof_info_from_geo_admin(x, y)
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
            building_info = api.fetch_building_info_from_geo_admin(EGID)
            BFS = building_info['feature']['attributes']['ggdenr']
            post_office.bfs = BFS
            update_db()

        return new_address, True