from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SubmitField, MultipleFileField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=100)])
    author = StringField('Author', validators=[DataRequired(), Length(min=3, max=100)])
    price = FloatField(validators=[DataRequired()])
    quantity = IntegerField(validators=[DataRequired()])
    description = TextAreaField(validators=[DataRequired(), Length(max=2000)])
    category = SelectField('Category', validators=[DataRequired()], choices=[])
    images = MultipleFileField()
    submit = SubmitField('Save')


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])