import os
import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask.logging import default_handler


db = SQLAlchemy()
db_migration = Migrate()
bcrypt = Bcrypt()
login = LoginManager()
login.login_view = "users.login"


def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)
    configure_logging(app)
    register_error_pages(app)
    return app


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    db_migration.init_app(app, db)
    bcrypt.init_app(app)
    login.init_app(app)

    # Flask-Login configuration
    from src.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app):
    # Import the blueprints
    from src.users import users_blueprint

    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    app.register_blueprint(users_blueprint)
    # app.register_blueprint(users_blueprint, url_prefix="/users")


def configure_logging(app):
    # Logging Configuration
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)

    app.logger.info("Starting the Flask Ticket Manager App...")


def register_error_pages(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404
