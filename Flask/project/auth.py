import re
from flask import Blueprint, render_template,request,flash,redirect,url_for
from . import db
from flask_login import login_user, login_required,logout_user,current_user
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/',methods=['GET' , 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password= request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in Successfully!", category='sucess')
                login_user(user,remember=True)
                return redirect(url_for('views.index'))
            else:
                flash("Incorrect Password!", category='error')
        else:
            flash("User Not Found", category='error')
    return render_template('login.html',user=current_user)
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET' , 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        phone = request.form.get('telephone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist!", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 4 character",category="error")
        elif len(name) < 2:
            flash("Name must be greater than 3 character",category="error")
        elif len(phone) != 10:
            flash("Phone number must be of 10 digits",category="error")
        elif password1 != password2:
            flash("Password don't match",category="error")
        elif int(password1) < 7:
            flash("Password is too short",category="error")
        else:
            new_user = User(email = email, name = name, phone = phone, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user,remember=True)
            flash("Accounted Created Successfully", category="sucess")
            return redirect(url_for('views.index'))
    return render_template('signup.html', user=current_user) 