from flask import Flask
#from flask_migrate import Migrate
from .commands import create_tables
from .extensions import db, login_manager
from .models import Review, User
from .routes.main import main
from .routes.dash import dash
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'dash.login'
    login_manager.login_message = "Please login to access this page"
    login_manager.login_message_category = "error"

    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(user_id)

    admin = Admin(app, name='Dashboard')


    admin.add_view(ModelView(Review, db.session))
    admin.add_view(ModelView(User, db.session))

    app.register_blueprint(main)
    app.register_blueprint(dash)
    # app.register_blueprint(store)
    # app.register_blueprint(admin)

    app.cli.add_command(create_tables)

    #migrate = Migrate(app, db)

    return app
