from flask import Blueprint, render_template, request, send_file, jsonify, json, redirect, flash, url_for, Markup
#from flask_login import login_required, current_user
#from src.routes.auth import UpdateAccountForm
from src.extensions import db
from flask_admin import Admin
from src.models import Review
import secrets
import smtplib
import os
from flask import Flask
from PIL import Image
from flask_mail import Mail
from flask_admin.contrib.sqla import ModelView
from email.message import EmailMessage
from flask_login import UserMixin

app = Flask(__name__)

main = Blueprint('main', __name__)

mine = 'olugbengaakeredolu1234@gmail.com'


#Function for upload picture#
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, '../static/img/pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn

# home
@main.route('/')
@main.route('/index.html')
def index():

    return render_template('index.html')


# contact
@main.route('/contact', methods=['GET', 'POST'])
@main.route('/contact.html', methods=['GET', 'POST'])
def contact():
    my_number = '+4917687834465'

    my_email = 'olugbengaakeredolu1234@gmail.com'

    if request.method == 'POST':
        message = request.form.get('message')
        email = request.form.get('email')
        phone = request.form.get('phone')
        name = request.form.get('name')
        subject = request.form.get('subject')

        # email message
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = mine
        msg['To'] = mine
        msg.set_content('')
        msg.add_alternative("""\
            <h1 style="color: #000; font-weight: 100; text-align: center;">
            <br>
            
            Message from {}
            </h1>
            subject: {}
            <br>
            message: {}
            <br>
            name: {}
            <br>
            phone: {}
            <br>
        
        """.format(email, subject, message, name, phone), subtype='html')

        # email sending function
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("officialolugbengaakeredolu@gmail.com", "justarandomguycr7")
            smtp.send_message(msg)

        flash('Message sent', 'success')

        return redirect(url_for('main.contact'))

   # else:
        #flash('Error Ocurred', 'error')

    return render_template('contact.html', my_email=my_email, my_number=my_number)


# about
@main.route('/about', methods=['GET', 'POST'])
@main.route('/about.html', methods=['GET', 'POST'])
def about():
    reviews = Review.query.all()
    # amount = db.session.query(Review).filter_by()
    
    return render_template('about.html', reviews=reviews)


# portfolio
@main.route('/portfolio')
@main.route('/portfolio.html')
def portfolio():

    return render_template('portfolio.html')


# download cv
@main.route('/download')
def download_file():
    # file_fn
    path = os.path.join(
        app.root_path, '../upload/my_cv.docx')
    return send_file(path, as_attachment=True)


# add review
@main.route('/addreview', methods=['GET', 'POST'])
def addreview():
    if request.method == 'POST':
        name = request.form.get('name')
        review = request.form.get('review')
        platform = request.form.get('platform')
        reference = request.form.get('ref')
        company = request.form.get('company')
       

        add_review = Review(
            name=name,
            review=review,
            platform=platform,
            reference=reference,
            company=company
            
        )

        db.session.add(add_review)
        db.session.commit()

        subject = 'Important | Review Added'

        # email message
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = mine
        msg['To'] = mine
        msg.set_content('')
        msg.add_alternative("""\
            <h3 style="color: #000; font-weight: 100; text-align: center;">
            <br>
            
            A Review by {} has been added <br>
            Check as soon as possible.
            <br>
            Company name: {}
           
            <br>
        
        """.format(name,company), subtype='html')

        # email sending function
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("officialolugbengaakeredolu@gmail.com", "justarandomguycr7")
            smtp.send_message(msg)

        flash('Thank you! Feedback will be displayed once reviewed.', 'success')
        return redirect(url_for('main.about'))


