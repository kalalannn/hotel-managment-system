from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Email, Length, EqualTo
from ..models import User, UserRole


class UserForm(FlaskForm):
    first_name = StringField('First name', validators=[Required(), Length(1, 64)])
    last_name= StringField('Last name', validators=[Required(), Length(1, 64)])
    email = StringField('Email', validators=[Email(), Required()])
    role = SelectField('Role', validators=[Required()],
        choices=[(r.value, r.name.capitalize()) for r in UserRole if r != UserRole.ANON])

class UserSearchForm(FlaskForm):
    first_name = StringField('First name', validators=[Length(1, 64)])
    last_name= StringField('Last name', validators=[Length(1, 64)])
    email = StringField('Email')
    role = SelectField('Role')

    def __init__(self, *args, **kwargs):
        super(UserSearchForm, self).__init__(*args, **kwargs)

        option_all = tuple((0, 'All'))
        choices = [(r.value, r.name.capitalize()) for r in UserRole if r != UserRole.ANON]
        choices.append(option_all)
        self.role.choices = choices
