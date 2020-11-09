from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, SelectField
from wtforms.validators import Required, Email, Length, EqualTo
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(), Required(message='Forgot your email address?')])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[Required(), Length(1, 64)])
    last_name= StringField('Last name', validators=[Required(), Length(1, 64)])
    email = StringField('Email', validators=[Email(), Required(message='Forgot your email address?')])
    password = PasswordField('Password', validators=[Required(), EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField('Confirm password', validators=[Required()])
    role = SelectField('Role', validators=[Required()])
    submit = SubmitField('Register')

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