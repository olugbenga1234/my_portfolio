from flask import Blueprint, render_template, request, jsonify, json, redirect, flash, url_for, Markup
from flask_login import login_required, current_user
from src.routes.auth import UpdateAccountForm
from src.extensions import db
from src.models import Donated, User
from src.models import User
import secrets
import smtplib
import os
from flask import Flask
from PIL import Image
from flask_mail import Mail
from email.message import EmailMessage

app = Flask(__name__)

main = Blueprint('main', __name__)


# home
@main.route('/')
@main.route('/index.html')
def index():

    return render_template('index.html')


