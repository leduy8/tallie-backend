from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email, Length


class ProfileForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired(), Length(min=6, max=50)])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio', validators=[Length(max=250)])
    address = StringField('Address', validators=[DataRequired(), Length(max=150)])
    # avatar = FileField()
    submit = SubmitField('Done')


class PaymentForm(FlaskForm):
    card_number = StringField('Card number', validators=[DataRequired(), Length(min=14, max=14)])
    card_owner_name = StringField('Name', validators=[DataRequired(), Length(min=3, max=100)])
    start_date = DateField('Start date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End date', validators=[DataRequired()], format='%Y-%m-%d')
    cvc = StringField('CVC', validators=[DataRequired(), Length(min=3, max=3)])
    submit = SubmitField('Save')