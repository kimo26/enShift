# Importing necessary library and modules
from database import db

# Defining the District model
class District(db.Model):
    __tablename__ = 'district'  # Setting the table name
    number = db.Column(db.Integer, primary_key=True, nullable=False)  # District number as primary key
    name = db.Column(db.String(255), nullable=True)  # District name
    areas = db.relationship('Area', back_populates='district')  # Relationship to Area model

    # Explanation of Intent: This model represents a postal district, which is the highest level in the postal hierarchy.

# Defining the Area model
class Area(db.Model):
    __tablename__ = 'area'  # Setting the table name
    number = db.Column(db.Integer, primary_key=True, nullable=False)  # Area number as primary key
    name = db.Column(db.String(255), nullable=True)  # Area name
    district_number = db.Column(db.Integer, db.ForeignKey('district.number'), nullable=False)  # Foreign key to District model
    district = db.relationship('District', back_populates='areas')  # Relationship to District model
    routes = db.relationship('Route', back_populates='area')  # Relationship to Route model

    # Explanation of Intent: This model represents a postal area within a district, which is a subdivision of a postal district.

# Defining the Route model
class Route(db.Model):
    __tablename__ = 'route'  # Setting the table name
    number = db.Column(db.Integer, primary_key=True, nullable=False)  # Route number as primary key
    name = db.Column(db.String(255), nullable=True)  # Route name
    area_number = db.Column(db.Integer, db.ForeignKey('area.number'), nullable=False)  # Foreign key to Area model
    area = db.relationship('Area', back_populates='routes')  # Relationship to Area model
    post_offices = db.relationship('PostOffice', back_populates='route')  # Relationship to PostOffice model

    # Explanation of Intent: This model represents a postal route within an area, which is a subdivision of a postal area.

# Defining the PostOffice model
class PostOffice(db.Model):
    __tablename__ = 'post_office'  # Setting the table name
    number = db.Column(db.Integer, primary_key=True, nullable=False)  # Post office number as primary key
    bfs = db.Column(db.String(10), nullable=True)  # Post office name
    route_number = db.Column(db.Integer, db.ForeignKey('route.number'), nullable=False)  # Foreign key to Route model
    route = db.relationship('Route', back_populates='post_offices')  # Relationship to Route model
    addresses = db.relationship('Address', back_populates='post_office')  # Relationship to Address model

    # Explanation of Intent: This model represents a post office within a route, which is a subdivision of a postal route.

# Defining the Address model
class Address(db.Model):
    __tablename__ = 'address'  # Setting the table name
    id = db.Column(db.Integer, primary_key=True, nullable=False)  # Address ID as primary key
    street_name = db.Column(db.String(255), nullable=False)  # Street name
    street_number = db.Column(db.String(20), nullable=False)  # Street number
    city = db.Column(db.String(255), nullable=False)  # City name
    egid = db.Column(db.String(255),nullable=True)
    sonnendach_id = db.Column(db.String(255), nullable=True)
    post_office_number = db.Column(db.Integer, db.ForeignKey('post_office.number'), nullable=False)  # Foreign key to PostOffice model
    post_office = db.relationship('PostOffice', back_populates='addresses')  # Relationship to PostOffice model

    # Explanation of Intent: This model represents an address within a post office's jurisdiction, which is the lowest level in the postal hierarchy.
