from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Email, Length, EqualTo
from ..models import User, UserRole

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(), Required(message='Forgot your email address?')])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Email(), Required(message='Forgot your email address?')])
    first_name = StringField('First name', validators=[Required(), Length(1, 64)])
    last_name= StringField('Last name', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required(), EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField('Confirm password', validators=[Required()])
    role = SelectField('Role', validators=[Required()])
    submit = SubmitField('Register')

    def admin(self):
        self.role.choices = [(r.value, r.name) for r in UserRole]

    def director(self):
        self.role.choices = [(r.value, r.name) for r in UserRole if r in (UserRole.CUSTOMER, UserRole.RECEPTIONIST)]

    def others(self):
        del self.role

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('Email already registered.')


class NewPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[Required()])
    new_password = PasswordField('New password', validators=[Required(), EqualTo('confirm_new_password', message='Passwords must match.')])
    confirm_new_password = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Change password')

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('Email already registered.')


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
    submit = SubmitField('Search')

    def __init__(self, *args, **kwargs):
        super(UserSearchForm, self).__init__(*args, **kwargs)

        choices = [(r.value, r.name.capitalize()) for r in UserRole if r != UserRole.ANON]
        choices.insert(0, ('',''))
        self.role.choices = choices
