from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError

class RegisterForm(FlaskForm):
    
    # def validate_email(self, email_to_check):
    #     email = User.query.filter_by(email=email_to_check.data).first()
    #     if email:
    #         raise ValidationError('Email already exists!')

    firstname = StringField(label='First Name:', validators=[Length(min=2, max=50), DataRequired()])
    lastname = StringField(label='Last Name:', validators=[Length(min=2, max=50), DataRequired()])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')