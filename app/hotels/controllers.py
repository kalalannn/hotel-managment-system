from flask import request, render_template, session, redirect, url_for, flash

# from flask_login import login_user, logout_user, login_required

from . import hotels
from .forms import SearchForm, NewHotelForm
from ..models import Hotel, User
from app import db

@hotels.route('/list/', methods=['GET', 'POST'])
def list():
    form = SearchForm()
    if form.validate_on_submit:
        pass

    return render_template('hotels/list.html', form=form)

@hotels.route('/new/', methods=['GET', 'POST'])
def new():
    form = NewHotelForm()
    if form.validate_on_submit:
        pass

    return render_template('hotels/new.html', form=form)

# There must be hotel_id to SHOW!
# @hotels.route('/show/', methods=['GET', 'POST'])
# def show():
#     return render_template('hotels/show.html')

# # There also
# @hotels.route('/edit/', methods=['GET', 'POST'])
# def edit():
#     return render_template('hotels/edit.html')