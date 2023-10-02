from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class AddressForm(FlaskForm):
    street_name = StringField('Street Name', validators=[DataRequired(), Length(min=2, max=255)])
    street_number = StringField('Street Number', validators=[DataRequired(), Length(min=1, max=20)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=255)])
    postal_code = IntegerField('Postal Code', validators=[DataRequired()])
    submit = SubmitField('Submit')