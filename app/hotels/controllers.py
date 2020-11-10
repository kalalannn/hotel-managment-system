from flask import request, render_template, session, redirect, url_for, flash, json

from flask_login import current_user, login_user, logout_user, login_required

from . import hotels
from .forms import SearchForm, HotelForm
from ..models import Hotel, User, HotelStars, UserRole
from app import db
from app.helpers import Helper

@hotels.route('/list/', methods=['GET', 'POST'])
def list():
    form = SearchForm()

    # TODO delete!
    # choises = Helper.dictToListOfTuples(Hotel._starses)
    # choises.insert(0, ('',''))
    # form.stars.choices = choises

    # енамы збс
    choices =[(s.value, '*' * s.value) for s in HotelStars]
    choices.insert(0, ('',''))
    form.stars.choices = choices

    _hotels = None
    if request.method == 'GET':
        _hotels = Hotel.query.order_by(Hotel.stars).limit(10).all()
    # POST
    elif form.validate_on_submit():
        query = Hotel.query

        if form.name.data is not None:
            query = query.filter(Hotel.name.like("%{}%".format(form.name.data)))

        if form.stars.data:
            query = query.filter(form.stars.data == Hotel.stars)

        _hotels = query.all()
    # EMPTY FORM
    else:
        _hotels = Hotel.query.limit(10).all()

    return render_template('hotels/list.html', form=form, hotels=_hotels)

@hotels.route('/new/', methods=['GET', 'POST'])          # Only admin
@hotels.route('/edit/<int:hotel_id>', methods=['GET', 'POST']) # Director+
def update(hotel_id=None):
    # print (current_user)
    # print ('Auth: {}'.format(current_user.is_authenticated))
    # return render_template('hotels/update.html', form=HotelForm())
    form = HotelForm()

    # EDIT
    if hotel_id and current_user.role >= UserRole.DIRECTOR.value:
        hotel = Hotel.query.filter_by(id=hotel_id).one()
        form = HotelForm(obj=hotel)
        if current_user.role == UserRole.ADMIN.value:
            # Вот так юзать
            users = User.query.filter_by(role=UserRole.DIRECTOR.value).all()
            form.owner.choices = [(u.id, u.first_name + ' ' +  u.last_name) for u in users]
            # TODO delete!
            # form.owner.choices = Helper.listObjToListOfTuples(Role.users_by_role('DIRECTOR'), \
            #     ' ', "first_name", "last_name")
        else:
            form.director()
            form.owner = '{} {}'.format(hotel.owner.first_name, hotel.owner.last_name)
    # TODO дальше по аналогии
    # NEW
    # elif User.has_role(current_user, 'ADMIN'):
    #     form.stars.choices = Helper.dictToListOfTuples(Hotel._starses)
    #     form.owner.choices = Helper.listObjToListOfTuples(Role.users_by_role('DIRECTOR'), \
    #         ' ', "first_name", "last_name")

    # # POST
    # if form.validate_on_submit():
    #     # EDIT
    #     if hotel_id:
    #         hotel = Hotel.query.filter_by(id=hotel_id).one()
    #         form.populate_obj(hotel)
    #         hotel.save()

    #     # NEW
    #     else:
    #         hotel = Hotel(
    #             form.name.data,
    #             form.description.data,
    #             form.stars.data,
    #             form.address.data,
    #             form.owner.data,
    #         )
    #     return redirect(url_for('hotels.list'))
    return render_template('hotels/update.html', form=form)

# There must be hotel_id to SHOW!
# @hotels.route('/show/', methods=['GET', 'POST'])
# def show():
#     return render_template('hotels/show.html')

# # There also
# @hotels.route('/edit/', methods=['GET', 'POST'])
# def edit():
#     return render_template('hotels/edit.html')