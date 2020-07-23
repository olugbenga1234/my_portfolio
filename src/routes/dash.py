from flask import Blueprint, render_template, request, send_file, jsonify, json, redirect, flash, url_for, Markup
from flask_login import login_user, logout_user, current_user, login_required
from src.extensions import db
from src.models import Review
import secrets
import smtplib
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask
#from flask_admin import Admin, BaseView, expose
#from flask.ext.admin import Admin
#from flask_admin.contrib.sqla import ModelView
#from PIL import Image
#from flask_mail import Mail
#from email.message import EmailMessage

app = Flask(__name__)

#admin = Admin(app)
db = SQLAlchemy(app)

dash = Blueprint('dash', __name__)


#display review



# delete review
@dash.route('/del/<int:id>', methods=['GET', 'POST'])
def delreview(id):
    delete = Review.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(delete)
        db.session.commit
        flash(f'Review id:{delete.id} has been deleted', 'success')
        return redirect(url_for('dash.mydash'))
    flash('can not delete the review ', 'error')
    return redirect(url_for('dash.mydash'))
