from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Email, Length, EqualTo
from ..models import User, UserRole, Hotel

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email(), Required(message='Forgot your email address?')])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')

class UserForm(FlaskForm):
    email = StringField('Email', validators=[Email(), Required(message='Forgot your email address?')])
    first_name = StringField('First name', validators=[Required(), Length(1, 64)])
    last_name= StringField('Last name', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required(), EqualTo('confirm_password', message='Passwords must match.')])
    confirm_password = PasswordField('Confirm password', validators=[Required()])
    role = SelectField('Role', coerce=int, validators=[Required()])
    recept_hotel_id = SelectField('Recept Hotel', coerce=int)
    submit = SubmitField('New User')

    def admin(self):
        self.role.choices = [(r.value, r.name) for r in UserRole]
        choices = [(h.id, h.name) for h in Hotel.filter(Hotel.query).order_by(Hotel.id).all()]
        choices.insert(0, ('0',''))
        self.recept_hotel_id.choices = choices

    def director(self, current_user):
        self.role.choices = [(r.value, r.name) for r in UserRole if r in (UserRole.CUSTOMER, UserRole.RECEPTIONIST)]
        choices = [(h.id, h.name) for h in Hotel.subordinates_editable(Hotel.query, current_user).order_by(Hotel.id).all()]
        choices.insert(0, ('0',''))
        self.recept_hotel_id.choices = choices

    def anon(self):
        del self.role
        del self.recept_hotel_id

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('Email already registered.')

class EditUserForm(UserForm):
    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.submit.label.text = 'Update User'
        del self.password
        del self.confirm_password

    def validate_email(self, email_field):
        return True


class NewPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[Required()])
    new_password = PasswordField('New password', validators=[Required(), EqualTo('confirm_new_password', message='Passwords must match.')])
    confirm_new_password = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Change password')

class UserSearchForm(FlaskForm):
    first_name = StringField('First name', validators=[Length(0, 64)])
    last_name= StringField('Last name', validators=[Length(0, 64)])
    email = StringField('Email')
    role = SelectField('Role', coerce=int)
    submit = SubmitField('Search')

    def admin(self):
        choices = [(r.value, r.name.capitalize()) for r in UserRole]
        choices.insert(0, (0,''))
        self.role.choices = choices

    def director(self):
        choices = [(r.value, r.name.capitalize()) for r in UserRole if r in (UserRole.CUSTOMER, UserRole.RECEPTIONIST)]
        choices.insert(0, (0,''))
        self.role.choices = choices
