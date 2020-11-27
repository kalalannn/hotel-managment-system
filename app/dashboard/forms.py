from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField
from wtforms.validators import Required, Email, Length
from datetime import datetime, timedelta
from wtforms.fields.html5 import EmailField
from ..models import User, UserRole


class UserForm(FlaskForm):
    first_name = StringField('First name', validators=[Required(), Length(1, 64)])
    last_name= StringField('Last name', validators=[Required(), Length(1, 64)])
    email = EmailField('Email', validators=[Email(), Required()])
    date_from = DateField('Start date', validators=[Required()])
    date_to = DateField('End date', validators=[Required()])
