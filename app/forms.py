from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create account')

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
    category = StringField('Categories(Separate with a comma)', validators=[DataRequired()])
    submit = SubmitField('Continue')
