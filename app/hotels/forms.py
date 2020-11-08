from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import Required

STARS_SELECT = [
    ('5', '*****'),
    ('4', '****'),
    ('3', '***'),
    ('2', '**'),
    ('1', '*'),
]

class SearchForm(FlaskForm):
    name    = StringField('Name')
    stars   = SelectField('Stars', choices = STARS_SELECT)
    submit  = SubmitField('Search')

class NewHotelForm(FlaskForm):
    name       = StringField('Name',        validators=[Required()])
    description= StringField('Description', validators=[Required()])
    stars      = SelectField('Stars',       validators=[Required()], choices=STARS_SELECT)
    address    = StringField('Address',     validators=[Required()])
    submit     = SubmitField('Create')
