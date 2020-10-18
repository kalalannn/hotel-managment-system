from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
# from flask_moment import Moment
# from datetime import datetime

app = Flask(__name__)
# app.config.from_object('config')
db = SQLAlchemy(app)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('base.html')

@app.errorhandler(404)
def not_found(error):
    return 'Not Found ...', 404