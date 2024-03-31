from web import app, db
from flask import render_template, redirect, url_for, jsonify, flash
from web.forms import RegisterForm, LoginForm
from web.models import User
from flask_login import login_user, logout_user
import requests

progress = 25

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', flash_message=True)

@app.route('/about/<username>')
def about_page(username):
    return f'<h1>This is the about page of {username}'

@app.route('/play')
def play():
    global progress
    progress += 10
    if progress > 100:
        progress = 100
    return redirect(url_for('home_page'))

@app.route('/pause')
def pause():
    return redirect(url_for('home_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()

        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash('Success! You logged in!', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username or password are not correct! Please try again!', category='danger')
    return render_template('login.html', form=form)

@app.route('/testapi')
def test_api():
    try:
        response = requests.get("http://playback:5000/song")

        if(response):
            return jsonify({'message': 'Response valid!'})
        else:
            return jsonify({'message': 'No valid response'})
    except Exception as e:
        return jsonify({'error': f"{e}"})

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(firstname=form.firstname.data, 
                        lastname=form.lastname.data,
                        password=form.password1.data,
                        email=form.email.data)
        
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home_page'))
    
    if form.errors != {}:
        for err_msj in form.errors.values():
            flash(f'Error when creating an user:{err_msj}', category='danger')

    return render_template('register.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))
