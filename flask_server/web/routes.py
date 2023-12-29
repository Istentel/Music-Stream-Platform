from web import app
from flask import render_template
from web.forms import RegisterForm

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/about/<username>')
def about_page(username):
    return f'<h1>This is the about page of {username}'

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.errors != {}:
        for err_msj in form.errors.values():
            print(f'Error when creating an user:{err_msj}')
    if form.validate_on_submit():
        new_user = ''
    return render_template('register.html', form=form)

