from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.model import User, Business
from flask_login import current_user

#Counties list for creating and updating business
counties=[
        ('Baringo','Baringo'),
        ('Bomet','Bomet'),
        ('Bungoma','Bungoma'),
        ('Busia','Busia'),
        ('Elgeyo Marakwet','Elgeyo Marakwet'),
        ('Embu','Embu'),
        ('Garissa','Garissa'),
        ('Homa Bay','Homa Bay'),
        ('Isiolo','Isiolo'),
        ('Kajiado','Kajiado'),
        ('Kakamega','Kakamega'),
        ('Kericho','Kericho'),
        ('Kiambu','Kiambu'),
        ('Kilifi','Kilifi'),
        ('Kirinyaga','Kirinyaga'),
        ('Kisii','Kisii'),
        ('Kisumu','Kisumu'),
        ('Kitui','Kitui'),
        ('Kwale','Kwale'),
        ('Laikipia','Laikipia'),
        ('Lamu','Lamu'),
        ('Machakos','Machakos'),
        ('Makueni','Makueni'),
        ('Mandera','Mandera'),
        ('Meru','Meru'),
        ('Migori','Migori'),
        ('Marsabit','Marsabit'),
        ('Mombasa','Mombasa'),
        ('Muranga','Muranga'),
        ('Nairobi','Nairobi'),
        ('Nakuru','Nakuru'),
        ('Nandi','Nandi'),
        ('Narok','Narok'),
        ('Nyamira','Nyamira'),
        ('Nyandarua','Nyandarua'),
        ('Nyeri','Nyeri'),
        ('Samburu','Samburu'),
        ('Siaya','Siaya'),
        ('Taita Taveta','Taita Taveta'),
        ('Tana River','Tana River'),
        ('Tharaka Nithi','Tharaka Nithi'),
        ('Trans Nzoia','Trans Nzoia'),
        ('Turkana','Turkana'),
        ('Uasin Gishu','Uasin Gishu'),
        ('Vihiga','Vihiga'),
        ('Wajir','Wajir'),
        ('West Pokot','West Pokot')]

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken, please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken, please choose a different one')
            

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegBusinessForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    name = StringField('Business Name', validators=[DataRequired()])
    description = TextAreaField('Business Description', render_kw={"rows": 5, "cols": 11},
        validators=[DataRequired()])
    submit = SubmitField('Continue')

##This form is used to add business categories and locations
class CompleteBusinessProfile(FlaskForm):
    category = StringField('Categories(Separate with a comma)', validators=[DataRequired()])
    county = SelectField('Select County (Selecting a new county creates new location)', choices=counties, validators=[DataRequired()])
    region = StringField('Region within county', validators=[DataRequired()])
    location = TextAreaField('Exact Location in the Region', render_kw={"rows":3, "cols":10}, validators=[DataRequired()])
    submit = SubmitField('Finish')

##Updates user account
class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    profile_pic = FileField('Update profile picture', validators=[FileAllowed(['png','jpg','jpeg'])])
    submit = SubmitField('Update Details')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken, please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken, please choose a different one')
            