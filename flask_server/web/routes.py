from web import app
from flask import render_template, redirect, url_for, jsonify, flash
from web.db_api import register_user_api, login_user_api
from web.forms import RegisterForm, LoginForm
import requests, base64

@app.route('/')
@app.route('/home')
def home_page():
    songs_response = requests.get('http://playback:5000/api/songs')

    if songs_response.status_code != 200:
        return 'Failed to fetch songs data'
    
    songs = songs_response.json()

    # Decode base64-encoded image data
    for song in songs:
        if 'image' in song:
            image_data = base64.b64decode(song['image'])
            song['image'] = f"data:image/png;base64,{base64.b64encode(image_data).decode()}"
    

    return render_template('home.html', songs=songs, flash_message=True)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        response = login_user_api(form.email.data, form.password.data)

        if response and response.status_code == 200:
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
        new_user = {'firstname': form.firstname.data, 'lastname': form.lastname.data, 'password': form.password1.data, 'email': form.email.data}
        
        response = register_user_api(new_user)

        if response:
            flash(f'Success! User {new_user["firstname"]} + {new_user["lastname"]} created succesfully!', category='success')
            return render_template('home.html')
        else:
            return jsonify({'message': 'No valid response'}) 
    
    if form.errors != {}:
        for err_msj in form.errors.values():
            flash(f'Error when creating an user:{err_msj}', category='danger')

    return render_template('register.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))
