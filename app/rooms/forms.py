from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required
#from wtforms_components import read_only
#from wtforms.widgets import TextArea

from ..models import User, UserRole, Address, RoomCategory

class RoomCategoryForm(FlaskForm):
    category_price = StringField('Category Price')

    category = QuerySelectField('Category',      \
        get_label = lambda t: "{}".format(t.type), \
        validators=[Required()])

    add_category        = SubmitField('Add Category')

    def __init__(self, *args, **kwargs):
        super(RoomCategoryForm, self).__init__(*args, **kwargs)
        self.obj = kwargs['obj']
    
    def __repr__(self):
        return 'category={}'.format(self.category)
    def addCategory(self):
        self.category.query_factory = lambda: RoomCategory.query.distinct("type")


class RoomForm(FlaskForm):
    room_category = QuerySelectField('Category',      \
        get_label = lambda t: "{}".format(t.type), \
        validators=[Required()])

    number_of_beds  = StringField('Number of beds')
    numbers_from = StringField('Numbers from')
    numbers_to = StringField('Numbers to')

    addRoom         = SubmitField('Add Room')
    
    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.obj = kwargs['obj']

    def __repr__(self):
        return 'room_category={}'.format(self.room_category)
    
    def add_room(self):
        self.room_category.query_factory = lambda: RoomCategory.query.filter_by(hotel_id=self.obj.id).distinct("type")