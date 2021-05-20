from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, IntegerField, FloatField, SubmitField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=50)])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio', validators=[Length(max=250)])
    address = StringField('Address', validators=[DataRequired(), Length(max=150)])
    submit = SubmitField('Done')

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=50)])
    price = FloatField(validators=[DataRequired()])
    quantity = IntegerField(validators=[DataRequired()])
    description = TextAreaField(validators=[DataRequired(), Length(max=80)])
    image = FileField(validators=[FileRequired()])
    submit = SubmitField('Save')
