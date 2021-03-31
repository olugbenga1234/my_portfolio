from flask import Blueprint, render_template, request, send_file, jsonify, json, redirect, flash, url_for, Markup
from flask_login import login_user, logout_user, current_user, login_required, UserMixin
from src.extensions import db
from src.models import Review, User
#import secrets
import smtplib
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
# from flask_admin import Admin, BaseView, expose
# from flask.ext.admin import Admin
# from flask_admin.contrib.sqla import ModelView
# from PIL import Image
# from flask_mail import Mail
# from email.message import EmailMessage

app = Flask(__name__)

# admin = Admin(app)
db = SQLAlchemy(app)

dash = Blueprint('dash', __name__)

# Setup Flask-Security
# user_datastore = SQLAlchemyUserDatastore(db, User, Role, Review)
# security = Security(app, user_datastore)


# login
@dash.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get("username", False)
        password = request.form['password']

        # validate details
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash(Markup('Incorrect details'), 'error')
            return redirect(url_for('dash.login'))

        else:
            login_user(user, remember=remember)
            return redirect(url_for('/admin'))

    return render_template('login.html')


#admin page
# @dash.route('/admin/', methods=['GET', 'POST'])
# @login_required
# def admin():

#     return render_template('login.html')

