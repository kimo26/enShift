from flask import Flask, render_template, redirect, url_for,flash
from database import db
from models import District, Area, Route, PostOffice, Address
from forms import AddressForm
import os
import requests
import database_utils as db_utils

app = Flask(__name__)

app.config['SECRET_KEY'] = f'{os.urandom(16).hex()}'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kimo26:16062003@localhost/addressinfodb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
@app.route('/', methods=['GET', 'POST'])
def index():
    form = AddressForm()
    address = None
    message=None
    if form.validate_on_submit():
            address, created = db_utils.get_or_create_address(form.street_name.data, form.street_number.data, form.city.data, form.postal_code.data)
            
            if not address:
                message = 'Address does not exist. Try another one.'
            elif created:
                message = 'Address added successfully!'
            else:
                message = 'Address already exists in the database!'
            
            form = AddressForm(formdata=None)
        
            return render_template('index.html', message=message, address=address, form=form)

    return render_template('index.html', form=form)

def create_tables():
    with app.app_context():
        db.create_all()  

if __name__ == '__main__':
    create_tables()  
    app.run(debug=True)  