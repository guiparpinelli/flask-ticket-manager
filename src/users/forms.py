from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=6, max=40)])
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=120)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=32)]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=100)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")
