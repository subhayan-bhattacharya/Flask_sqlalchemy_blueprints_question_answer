from flask_wtf import FlaskForm
from wtforms.validators import InputRequired,Length
from wtforms import StringField,PasswordField

class RegisterForm(FlaskForm):
    username = StringField("Name",validators=[InputRequired(),Length(max=20)])
    password = PasswordField("Password",validators=[InputRequired(),Length(max=20)])

class LoginForm(FlaskForm):
    username = StringField("Name",validators=[InputRequired(),Length(max=20)])
    password = PasswordField("Password",validators=[InputRequired(),Length(max=20)])