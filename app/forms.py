from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.model import User

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
    counties=[
        ('Baringo','Baringo County'),
        ('Bomet','Bomet County'),
        ('Bungoma','Bungoma County'),
        ('Busia','Busia County'),
        ('Elgeyo Marakwet','Elgeyo Marakwet County'),
        ('Embu','Embu County'),
        ('Garissa','Garissa County'),
        ('Homa Bay','Homa Bay County'),
        ('Isiolo','Isiolo County'),
        ('Kajiado','Kajiado County'),
        ('Kakamega','Kakamega County'),
        ('Kericho','Kericho County'),
        ('Kiambu','Kiambu County'),
        ('Kilifi','Kilifi County'),
        ('Kirinyaga','Kirinyaga County'),
        ('Kisii','Kisii County'),
        ('Kisumu','Kisumu County'),
        ('Kitui','Kitui County'),
        ('Kwale','Kwale County'),
        ('Laikipia','Laikipia County'),
        ('Lamu','Lamu County'),
        ('Machakos','Machakos County'),
        ('Makueni','Makueni County'),
        ('Mandera','Mandera County'),
        ('Meru','Meru County'),
        ('Migori','Migori County'),
        ('Marsabit','Marsabit County'),
        ('Mombasa','Mombasa County'),
        ('Muranga','Muranga County'),
        ('Nairobi','Nairobi County'),
        ('Nakuru','Nakuru County'),
        ('Nandi','Nandi County'),
        ('Narok','Narok County'),
        ('Nyamira','Nyamira County'),
        ('Nyandarua','Nyandarua County'),
        ('Nyeri','Nyeri County'),
        ('Samburu','Samburu County'),
        ('Siaya','Siaya County'),
        ('Taita Taveta','Taita Taveta County'),
        ('Tana River','Tana River County'),
        ('Tharaka Nithi','Tharaka Nithi County'),
        ('Trans Nzoia','Trans Nzoia County'),
        ('Turkana','Turkana County'),
        ('Uasin Gishu','Uasin Gishu County'),
        ('Vihiga','Vihiga County'),
        ('Wajir','Wajir County'),
        ('West Pokot','West Pokot County')]
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    name = StringField('Business Name', validators=[DataRequired()])
    description = TextAreaField('Business Description', render_kw={"rows": 5, "cols": 11},
        validators=[DataRequired()])
    category = StringField('Categories(Separate with a comma)', validators=[DataRequired()])
    county = SelectField('Select County', choices=counties, validators=[DataRequired()])
    region = StringField('Region within county', validators=[DataRequired()])
    location = TextAreaField('Exact Location in the Region', render_kw={"rows":3, "cols":10}, validators=[DataRequired()])
    submit = SubmitField('Register Business')

class UpdateBusinessForm(FlaskForm):
    counties=[
        ('Baringo','Baringo County'),
        ('Bomet','Bomet County'),
        ('Bungoma','Bungoma County'),
        ('Busia','Busia County'),
        ('Elgeyo Marakwet','Elgeyo Marakwet County'),
        ('Embu','Embu County'),
        ('Garissa','Garissa County'),
        ('Homa Bay','Homa Bay County'),
        ('Isiolo','Isiolo County'),
        ('Kajiado','Kajiado County'),
        ('Kakamega','Kakamega County'),
        ('Kericho','Kericho County'),
        ('Kiambu','Kiambu County'),
        ('Kilifi','Kilifi County'),
        ('Kirinyaga','Kirinyaga County'),
        ('Kisii','Kisii County'),
        ('Kisumu','Kisumu County'),
        ('Kitui','Kitui County'),
        ('Kwale','Kwale County'),
        ('Laikipia','Laikipia County'),
        ('Lamu','Lamu County'),
        ('Machakos','Machakos County'),
        ('Makueni','Makueni County'),
        ('Mandera','Mandera County'),
        ('Meru','Meru County'),
        ('Migori','Migori County'),
        ('Marsabit','Marsabit County'),
        ('Mombasa','Mombasa County'),
        ('Muranga','Muranga County'),
        ('Nairobi','Nairobi County'),
        ('Nakuru','Nakuru County'),
        ('Nandi','Nandi County'),
        ('Narok','Narok County'),
        ('Nyamira','Nyamira County'),
        ('Nyandarua','Nyandarua County'),
        ('Nyeri','Nyeri County'),
        ('Samburu','Samburu County'),
        ('Siaya','Siaya County'),
        ('Taita Taveta','Taita Taveta County'),
        ('Tana River','Tana River County'),
        ('Tharaka Nithi','Tharaka Nithi County'),
        ('Trans Nzoia','Trans Nzoia County'),
        ('Turkana','Turkana County'),
        ('Uasin Gishu','Uasin Gishu County'),
        ('Vihiga','Vihiga County'),
        ('Wajir','Wajir County'),
        ('West Pokot','West Pokot County')]
    name = StringField('Business Name')
    description = TextAreaField('Business Description', render_kw={"rows": 5, "cols": 11})
    category = StringField('Categories(Separate with a comma)')
    county = SelectField('Select County', choices=counties)
    region = StringField('Region within county')
    location = TextAreaField('Exact Location in the Region', render_kw={"rows":3, "cols":10})
    submit = SubmitField('Update Business Profile')
