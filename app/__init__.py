from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
# from flask_datepicker import datepicker

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
# dp = datepicker()

def create_app(config_name):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config_name)
    app.add_template_global(models.UserRole, 'UserRole')

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    # dp.init_app(app)

    app.add_template_global(models.RoomType, 'RoomType')

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
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .hotels import hotels as hotels_blueprint
    app.register_blueprint(hotels_blueprint, url_prefix='/hotels')

    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix='/profile')

    from .dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')

    return app
