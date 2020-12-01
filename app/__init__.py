import os
from flask import Flask, url_for, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_jsglue import JSGlue

from datetime import datetime
from werkzeug.routing import BaseConverter, ValidationError

class DateConverter(BaseConverter):
    """Extracts a ISO8601 date from the path and validates it."""

    regex = r'\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError()

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')


db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
jsglue = JSGlue()

def create_app(config_name):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config_name)

    app.add_template_global(models.UserRole, 'UserRole')
    app.add_template_global(models.RoomType, 'RoomType')

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    app.url_map.converters['date'] = DateConverter

    @app.route('/documentation')
    def documentation():
        return render_template('doc.html')

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                            'favicon.ico',mimetype='image/vnd.microsoft.icon')
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/forbidden')
    def forbidden():
        return render_template('forbidden.html'), 403

    @app.route('/error')
    def error():
        return render_template('error.html')

    @app.errorhandler(404)
    def not_found(error):
        return 'Not Found ...', 404

    # Blueprints
    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/users')

    from .hotels import hotels as hotels_blueprint
    app.register_blueprint(hotels_blueprint, url_prefix='/hotels')

    from .reservations import reservations as reservations_blueprint
    app.register_blueprint(reservations_blueprint, url_prefix='/reservations')

    jsglue.init_app(app)

    return app
