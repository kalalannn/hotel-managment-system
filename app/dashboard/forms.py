from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField
from wtforms.validators import Required, Email, Length
from datetime import datetime, timedelta
from wtforms.fields.html5 import EmailField
from ..models import User, UserRole, ReservationStatus


class UserForm(FlaskForm):
    email = EmailField('Email', validators=[Email(), Required()])
    first_name = StringField('First name', validators=[Required(), Length(1, 64)])
    last_name= StringField('Last name', validators=[Required(), Length(1, 64)])
    create_date_from = DateField('Start date', validators=[Required()])
    create_date_to = DateField('End date', validators=[Required()])

class StatusForm(FlaskForm):
    status = SelectField('Status', validators=[Required()],
        choices=[(s.value, ' '.join(s.name.split('_')).capitalize()) for s in ReservationStatus if s != ReservationStatus.CANCELED])
    payment = SelectField('Payment', validators=[Required()],
        choices=[(0, 'Unpaid'), (1, 'Blocked'), (2, 'Paid')])
    edit_date_from = DateField('Start date', validators=[Required()])
    edit_date_to = DateField('End date', validators=[Required()])