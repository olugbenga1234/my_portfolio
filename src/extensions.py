#from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


import os

#login_manager = LoginManager()
db = SQLAlchemy()
app = Flask(__name__)
