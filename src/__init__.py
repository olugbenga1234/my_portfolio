from flask import Flask
#from flask_migrate import Migrate
from .commands import create_tables
from .extensions import db, login_manager
from .models import User, Donated, Products, Category
from .routes.main import main
from .routes.auth import auth
#from .routes.admin import admin
#from .routes.store import store
import os


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please login to access this page"
    login_manager.login_message_category = "error"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    #app.register_blueprint(store)
   # app.register_blueprint(admin)

    app.cli.add_command(create_tables)

    #migrate = Migrate(app, db)

    return app

