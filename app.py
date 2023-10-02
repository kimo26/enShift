# Importing necessary libraries
from flask import Flask, render_template, redirect, url_for,flash
from database import db
from models import District, Area, Route, PostOffice, Address
from forms import AddressForm
import os

app = Flask(__name__)


# Database Configuration
# Setting up the connection to the PostgreSQL database
app.config['SECRET_KEY'] = f'{os.urandom(16).hex()}'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kimo26:16062003@localhost/addressinfodb'
# Disabling track_modifications to suppress warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/add_address', methods=['GET', 'POST'])
def add_address():
    form = AddressForm()
    if form.validate_on_submit():
        postal_code = form.postal_code.data

        # Extract district, area, route, and post office number from postal code
        
        district_number = int(str(postal_code)[0])
        area_number = int(str(postal_code)[1])
        route_number = int(str(postal_code)[2])
        post_office_number = int(str(postal_code)[3])
        print(district_number,area_number,route_number,post_office_number)

        # Check if district exists, if not create it
        district = District.query.filter_by(number=district_number).first()
        if district is None:
            district = District(number=district_number)
            db.session.add(district)

        # Check if area exists, if not create it
        area = Area.query.filter_by(number=area_number).first()
        if area is None:
            area = Area(number=area_number, district=district)
            db.session.add(area)

        # Check if route exists, if not create it
        route = Route.query.filter_by(number=route_number).first()
        if route is None:
            route = Route(number=route_number, area=area)
            db.session.add(route)

        # Check if post office exists, if not create it
        post_office = PostOffice.query.filter_by(number=post_office_number).first()
        if post_office is None:
            post_office = PostOffice(number=post_office_number, route=route)
            db.session.add(post_office)

        # Now create the address
        new_address = Address(
            street_name=form.street_name.data,
            street_number=form.street_number.data,
            city=form.city.data,
            post_office=post_office  # Link the Address to the PostOffice instance
        )
        db.session.add(new_address)
        db.session.commit()
        flash('Address added successfully!', 'success')
        return redirect(url_for('index'))  # Redirect to the home page after successful submission

    return render_template('add_address.html', form=form)


@app.route('/')
def index():
    # Query the database for all addresses
    addresses = Address.query.all()
    return render_template('index.html', addresses=addresses)


# Explanation of Intent: 
# This function is intended to create all the database tables based on the models defined.
def create_tables():
    with app.app_context():
        db.create_all()  # Creating all tables
with app.app_context():
    db.drop_all()  # Drop all tables
    db.create_all()  # Create all tables based on the models

# Running the Flask application if this script is run directly
if __name__ == '__main__':
    create_tables()  # Creating tables before running the app
    app.run(debug=True)  # Running the app in debug mode for real-time code updates

# TODO: 
# - Implement API endpoints
# - Add authentication and authorization
# - Handle potential exceptions and errors
