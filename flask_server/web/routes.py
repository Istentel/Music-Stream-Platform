from web import app
from flask import session, render_template, redirect, url_for, jsonify, flash
from auth_svc.auth import register_user_api, login_user_api, validate_token
from web.forms import RegisterForm, LoginForm, SearchForm
import requests, base64

@app.route('/')
@app.route('/home')
def home_page():
    try:
        if not session.get("token"):
            return redirect(url_for('login_page'))

        email, err = validate_token(session["token"])

        if err:
            return err

        songs_response = requests.get(f'http://playback:5000/api/songs/{email}')

        if songs_response.status_code != 200:
            return 'Failed to fetch songs data'
        
        songs = songs_response.json()

        # Decode base64-encoded image data
        for song in songs:
            if 'image' in song:
                image_data = base64.b64decode(song['image'])
                song['image'] = f"data:image/png;base64,{base64.b64encode(image_data).decode()}"
        

        return render_template('home.html', logged_in=True, email=email, songs=songs, flash_message=True)
    
    except KeyError as e:
        flash(e, category='danger')
        return redirect(url_for("login_page"))
    
@app.route('/favourite')
def favourite_page():
    try:
        if not session.get("token"):
            return redirect(url_for('login_page'))
        
        email, err = validate_token(session["token"])

        if err:
            return err
        
        songs_response = requests.get(f'http://playback:5000/api/songs/{email}')

        if songs_response.status_code != 200:
            return 'Failed to fetch songs data'
        
        songs = songs_response.json()

        songs = [song for song in songs if song.get('favourite', True)]

        # Decode base64-encoded image data
        for song in songs:
            if 'image' in song:
                image_data = base64.b64decode(song['image'])
                song['image'] = f"data:image/png;base64,{base64.b64encode(image_data).decode()}"
        

        return render_template('favourite.html', logged_in=True, email=email, songs=songs, flash_message=True)
        
    except KeyError as e:
        flash(e, category='danger')
        return redirect(url_for("login_page"))


@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/search', methods=['POST'])
def search():
    if not session.get("token"):
            return redirect(url_for('login_page'))

    email, err = validate_token(session["token"])

    if err:
        return err
    
    form = SearchForm()

    if form.validate_on_submit():
        post_searched = form.searched.data.lower()

        songs_response = requests.get(f'http://playback:5000/api/songs/{email}')

        if songs_response.status_code != 200:
            return 'Failed to fetch songs data'

        songs = songs_response.json()

        songs = [song for song in songs if post_searched in song['name'].lower()]

        # Decode base64-encoded image data
        for song in songs:
            if 'image' in song:
                image_data = base64.b64decode(song['image'])
                song['image'] = f"data:image/png;base64,{base64.b64encode(image_data).decode()}"

        return render_template('search.html', form=form, searched=post_searched, logged_in=True, email=email, songs=songs, flash_message=True)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        response = login_user_api(form.email.data, form.password.data)

        if response and response.status_code == 200:
            token = response.json().get('token')
            session["token"] = token
            flash('Success! You logged in!', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username or password are not correct! Please try again!', category='danger')
    return render_template('login.html', logged_in=False, form=form)

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

        if response and response.status_code == 201:
            token = response.json().get('token')
            session["token"] = token
            flash(f'Success! User {new_user["firstname"]} {new_user["lastname"]} created succesfully!', category='success')
            return redirect(url_for('home_page'))
        else:
            return jsonify({'message': 'No valid response'}), 204
    
    if form.errors != {}:
        for err_msj in form.errors.values():
            flash(f'Error when creating an user:{err_msj}', category='danger')

    return render_template('register.html', form=form)

@app.route('/logout')
def logout_page():
    session["token"] = None
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))
