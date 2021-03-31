from flask_login import UserMixin, login_required, login_manager, current_user
from werkzeug.security import generate_password_hash
from .extensions import db, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import date, datetime
import json
from werkzeug.security import generate_password_hash
# from flask_admin.contrib.sqla import ModelView


# roles_users = db.Table('roles_users',
#         db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#         db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


# class Role(db.Model, RoleMixin):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(80), unique=Tru
#     description = db.Column(db.String(255))


# User Account Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200))
    username = db.Column(db.String(20), unique=True)
    # roles = db.relationship('Role', secondary=roles_users,
    #                         backref=db.backref('users', lazy='dynamic'))

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot view unhashed password')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(
            unhashed_password, method='sha256')

    def __repr__(self):
        return '<User %r>' % self.username


# review model
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
    approved = db.Column(db.String, default='no', nullable=False)
    company = db.Column(db.String(300), nullable=True)
    image_file = db.Column(
        db.String(200), nullable=False, default='default.png')
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
