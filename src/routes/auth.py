from flask import Blueprint, render_template, request, redirect, url_for, Flask, flash, Markup
from flask_login import login_user, logout_user, current_user
#from flask_admin import Admin
from werkzeug.security import check_password_hash
from flask_mail import Mail
from src.extensions import db
from src.models import User, Donated, Products, Category, JsonEncodedDict, CustomerOrder
import smtplib
from email.message import EmailMessage
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError
import email_validator
from flask_wtf.file import FileField, FileAllowed
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

auth = Blueprint('auth', __name__)

SECRET_KEY = '4b4474b4h47n474n474n47447n474n47'


#function for register
@auth.route('/register', methods=['GET', 'POST'])
@auth.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        address = request.form.get('address')
        state = request.form.get('state')
        lga = request.form.get('lga')
        phone = request.form.get('phone')
        bvn = request.form.get('bvn')
        unhashed_password = request.form.get('password')
        usertype = request.form.get('usertype')

        
#check if username exists
        checkusername = User.query.filter_by(username=username).first()

        if checkusername:
            flash(Markup(' Username already exists. Already have an account?<a href="login.html" style="color: yellow; font-weight: 900;"> Login In</a>'), 'error')
            return redirect(url_for('auth.register'))

#check if email already exists
        checkuseremail = User.query.filter_by(email=email).first()

        if checkuseremail:
            flash(Markup(' Email already exists. Already have an account?<a href="login.html" style="color: yellow; font-weight: 500;"> Login In</a>'), 'error')
            return redirect(url_for('auth.register'))


        new_user = User(lastname=lastname,
                    firstname=firstname,
                    username=username,
                    unhashed_password=unhashed_password,
                    email=email,
                    address=address,
                    state=state,
                    lga=lga,
                    phone=phone,
                    bvn=bvn,
                    usertype=usertype
                    )
                    
        db.session.add(new_user)
        db.session.commit()

        #email message
        msg = EmailMessage()
        msg['Subject'] = 'Donate A Seed - Confirmation Email'
        msg['From'] = "donateaseedoffcial@gmail.com"
        msg['To'] = email
        msg.set_content('')
        msg.add_alternative("""\
        <h1 style="color: #000; font-weight: 600; text-align: center;">Confirmation Email for your Application On Donate A Seed</h1>
        <br>
        <p style="color: #222; font-weight: 300;">Hi {}, Your email {} was used for applying on <b>Donate A Seed</b> as a <b>{}</b>.
        <br>
        <p>your username is : {}</p>
        We will review your application and send your results to {} <br>
        Please ignore this email if you did not apply on our platform. </p>

        <br>For any enquiries reply to this email and we will get back to you as soon as possible.
        <br><br><br>
        Regards,<br>
        Donate A Seed
        """.format(firstname,email,usertype,username,email), subtype='html')

        #email sending function
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("donateaseedoffcial@gmail.com", "donateaseed1234")
            smtp.send_message(msg)

        flash(' Registered successfully, please check your email ' + email, 'success')

        return redirect(url_for('auth.login'))

    return render_template('register.html')





#function for login
@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/login.html', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(Markup(' Already Logged In, click<a href="logout.html" style="color: yellow; font-weight: 900;"> HERE </a> to Logout.' ), 'error')

        return redirect(url_for('main.profile'))

    elif request.method == 'POST':
        username = request.form.get("username", False)
        password = request.form['password']
        remember = True if request.form.get('remember') else False

#validate details
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash(Markup(' Could not Login, Please check your login details and try again! Or click <a href="register.html" style="color: yellow; font-weight: 900;"> HERE </a> to register.' ), 'error')

        else:
            login_user(user, remember=remember)
            return redirect(url_for('main.profile'))

    return render_template('login.html')

#logout user
@auth.route('/logout')
@auth.route('/logout.html')
def logout():
    logout_user()
    flash('Logged Out successfully', 'success')
    return redirect(url_for('auth.login'))



#update account form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), length(min=5, max=20)])
    
    email = StringField('Email',
                    validators=[DataRequired(), Email()])
    
    picture = FileField('update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That Username is taken')

    def vaildate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken')

