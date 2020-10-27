from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
Bootstrap(app)

# It is important that you import your models after initializing the db object, 
# since in your models.py you also need to import the db object from this module.
from .models import *
db.drop_all()
db.create_all()

# Example data for database
from .models_data import load_models_data
load_models_data()

@app.route('/')
def index():
    return render_template('base.html')

@app.errorhandler(404)
def not_found(error):
    return 'Not Found ...', 404

# Blueprints
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)