from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import Required

class SearchForm(FlaskForm):
    name    = StringField('Name')
    stars   = SelectField('Stars')
    submit  = SubmitField('Search')

class HotelForm(FlaskForm):
    name       = StringField('Name',        validators=[Required()])
    stars      = SelectField('Stars',       validators=[Required()])
    address    = StringField('Address',     validators=[Required()])
    owner      = SelectField('Owner',       validators=[Required()])
    description= StringField('Description', validators=[Required()])
    submit     = SubmitField('Create')

    def director(self):
        self.owner = StringField('Owner', readonly="readonly")
        self.name.readonly = 'readonly'
        self.stars.readonly = 'readonly'
