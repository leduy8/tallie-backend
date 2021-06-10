from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')