from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField, PasswordField, TextAreaField, DecimalField, RadioField,
    DateField, SelectMultipleField, IntegerField, ValidationError, SelectField
    )
from wtforms.validators import InputRequired, Email, Length
from datetime import date

class BasicForm(FlaskForm):
    link = StringField('Website Link')
    # source = SelectField('Type of source',
    #     choices=[(0, 'Journalism'), (1, 'Research'), (2, 'Other')],
    #     validators=[InputRequired()], coerce=int)

class FormatForm(FlaskForm):
    style = RadioField('Citation Style',
        choices=[(0, 'MLA'), (1, 'Chicago')],
        validators=[InputRequired()],
        default='0',
        coerce=int)

class AdvancedForm(FlaskForm):
    # Author.
    # Title of source.
    # Title of container,
    # Other contributors,
    # Version,
    # Number,
    # Publisher,
    # Publication date,
    # Location.
    pass

class ManualForm(FlaskForm):
    author_first = StringField("Primary Author, Firstname")
    author_sur = StringField("Primary Author, Lastname")
    title = StringField("Title")
    container = StringField("Source Name")
    contributor_first = StringField("Contributor, Firstname")
    contributor_sur = StringField("Contributor, Lastname")
    version = StringField("Version")
    number = StringField("Number")
    publisher = StringField("Name of Publisher")
    pubdate = DateField("Date Published (YYYY-MM-DD)", format='%Y-%m-%d', default=date.today())
    location = StringField("URL or Page Number")
    accessdate = DateField("Date Published (YYYY-MM-DD)", format='%Y-%m-%d', default=date.today())
