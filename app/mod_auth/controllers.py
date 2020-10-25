# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
# from werkzeug import check_password_hash #, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.forms import LoginForm

# Import module models (i.e. User)
from app.models import User, Session

# db session
session = Session()

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():

    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():
        user = session.query(User).filter_by(email=form.email.data).first()
        session.close()
        print(user)

        # if user and check_password_hash(user.password, form.password.data):
        if user and user.password == form.password.data:
            # session['user_id'] = user.id
            flash('Welcome %s' % user.first_name)
            return redirect(url_for('auth.home'))

        flash('Wrong email or password', 'error-message')
    return render_template("auth/signin.html", form=form)

@mod_auth.route('/home/', methods=['GET'])
def home():
    # if session['user_id']:
    user = session.query(User).first()
    if user:
        return render_template("auth/home.html", user=user)
    else:
        return redirect(url_for('auth.signin'))