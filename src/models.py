from werkzeug.security import generate_password_hash
from .extensions import db, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import date, datetime
import json

# User Account Model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(500), nullable=False)
    review = db.Column(db.String(900), nullable=False)
    reference = db.Column(db.String(200), nullable=False)
    #lastname = db.Column(db.String(100))
    #email = db.Column(db.String(200), unique=True)
    #phone = db.Column(db.String(100), nullable=True)
    platform = db.Column(db.String)
    company = db.Column(db.String(300), nullable=True)
    image_file = db.Column(db.String(200), nullable=False, default='default.png')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)



        