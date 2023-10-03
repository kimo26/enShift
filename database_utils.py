from models import District, Area, Route, PostOffice, Address
from database import db
import api_utils as api
from exceptions import DatabaseError, RecordNotFoundError
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def add_to_db(item):
    """
    Add a given item to the database.

    Args:
    - item (db.Model): The database model instance to be added.

    Raises:
    - DatabaseError: If there's an error while adding the item to the database.
    """
    try:
        db.session.add(item)
        db.session.commit()
        logging.info(f'Successfully added {item} to the database.')
    except Exception as e:
        logging.error(f'Error adding to database: {str(e)}')
        raise DatabaseError(f"Error adding to database: {str(e)}")

def update_db():
    """
    Commit changes to the database.

    Raises:
    - DatabaseError: If there's an error while updating the database.
    """
    try:
        db.session.commit()
        logging.info('Successfully updated the database.')
    except Exception as e:
        logging.error(f'Error updating database: {str(e)}')
        raise DatabaseError(f"Error updating database: {str(e)}")


def retrieve_from_db(model, **filters):
    """
    Retrieve a record from the database based on the provided filters.

    Args:
    - model (db.Model): The database model to query.
    - **filters: Filters to apply to the query.

    Returns:
    - db.Model: The retrieved database model instance.

    Raises:
    - RecordNotFoundError: If no record is found based on the provided filters.
    """
    record = model.query.filter_by(**filters).first()
    if not record:
        logging.warning(f"{model.__name__} not found with filters: {filters}")
        raise RecordNotFoundError(f"{model.__name__} not found with filters: {filters}")
    logging.info(f"Successfully retrieved {model.__name__} with filters: {filters}")
    return record

def get_or_create(model, defaults=None, **kwargs):
    """
    Get an existing record from the database or create a new one if it doesn't exist.

    Args:
    - model (db.Model): The database model to query or create.
    - defaults (dict, optional): Default values to use when creating a new record.
    - **kwargs: Filters to apply to the query or values to use when creating a new record.

    Returns:
    - db.Model: The retrieved or created database model instance.
    """
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        logging.info(f"Found existing {model.__name__} with parameters: {kwargs}")
        return instance
    else:
        params = dict(kwargs)
        params.update(defaults or {})
        instance = model(**params)
        add_to_db(instance)
        logging.info(f"Created new {model.__name__} with parameters: {params}")
        return instance

def get_or_create_address(street_name, street_number, city, postal_code):
    """
    Retrieve an address from the database or create it if it doesn't exist.

    This function first checks if the given address exists in the database.
    If it does, it returns the address and a flag indicating that the address was not created.
    If the address doesn't exist, it creates the necessary postal hierarchy (district, area, route, post office)
    and the address itself, then returns the new address and a flag indicating that the address was created.

    Parameters:
    - street_name (str): The name of the street.
    - street_number (str): The number of the building on the street.
    - city (str): The name of the city.
    - postal_code (int or str): The postal code of the address.

    Returns:
    - Address: The retrieved or newly created address.
    - bool: A flag indicating whether the address was created (True) or retrieved (False).

    Raises:
    - DatabaseError: If there's an issue with the database operations.
    - APIError: If there's an issue fetching data from the external API.
    """
    try:
        # Start a new transaction
        db.session.begin()

        address = retrieve_from_db(Address, street_name=street_name, street_number=street_number, city=city)
        if address:
            logging.info(f"Address found for {street_name} {street_number}, {city}, {postal_code}")
            return address, False
        else:
            logging.info(f"Creating new address for {street_name} {street_number}, {city}, {postal_code}")
            # ... [rest of the code]

            # Commit the transaction
            db.session.commit()

            logging.info(f"Successfully created address for {street_name} {street_number}, {city}, {postal_code}")
            return new_address, True

    except Exception as e:
        logging.error(f"Error in get_or_create_address: {str(e)}")
        # Rollback the transaction in case of any errors
        db.session.rollback()
        raise e