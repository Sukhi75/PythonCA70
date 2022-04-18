from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


inscriptionauth = Blueprint('inscriptionauth', __name__)


@inscriptionauth.route('/Login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('User Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('inscriptionviews.Home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email ID does not exist.', category='error')

    return render_template("Login.html", user=current_user)


@inscriptionauth.route('/Logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('inscriptionauth.Login'))


@inscriptionauth.route('/Sign_Up', methods=['GET', 'POST'])
def Sign_Up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('This Email id already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account is created!', category='success')
            return redirect(url_for('inscriptionviews.Home'))

    return render_template("Sign_Up.html", user=current_user)
