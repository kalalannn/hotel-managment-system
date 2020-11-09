from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config_name)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def not_found(error):
        return 'Not Found ...', 404

    # Blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .hotels import hotels as hotels_blueprint
    app.register_blueprint(hotels_blueprint, url_prefix='/hotels')

    return app
