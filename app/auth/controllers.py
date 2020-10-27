from flask import request, render_template, session, redirect, url_for

from . import auth
# Import needed forms and models
from .forms import LoginForm
from ..models import User
# Import database object
from app import db


# Set the route and accepted methods
# Important! call it like url_for('auth.signin')
@auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    return '....lolollol...'

    # If sign in form is submitted
    # form = LoginForm(request.form)

    # # Verify the sign in form
    # if form.validate_on_submit():
    #     user = session.query(User).filter_by(email=form.email.data).first()
    #     session.close()
    #     print(user)

    #     # if user and check_password_hash(user.password, form.password.data):
    #     if user and user.password == form.password.data:
    #         # session['user_id'] = user.id
    #         flash('Welcome %s' % user.first_name)
    #         return redirect(url_for('auth.home'))

    #     flash('Wrong email or password', 'error-message')
    # return render_template("auth/signin.html", form=form)

@auth.route('/home/', methods=['GET'])
def home():
    return 'lalalla'
    # if session['user_id']:
    # user = session.query(User).first()
    # if user:
    #     return render_template("auth/home.html", user=user)
    # else:
    #     return redirect(url_for('auth.signin'))