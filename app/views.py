from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
#Using FlaskForm to create forms...makes work much easier to do and maintain
from .forms import RegistrationForm, LoginForm, RegBusinessForm, UpdateBusinessForm
##Handles all data
from .model import User, Business, Category, Location
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/index")
def index():
    app = {
        "title":"Business Finder",
        "heading": "Home"
    }
    return render_template("index.html", app=app, data=dict())

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash('Logged in, please logout to register or login as another user','info')
        return redirect(url_for('index'))
    app = {
        "title":"Signup",
        "heading":"Create Account"
    }
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        email = form.email.data
        username = form.username.data
        user = User(username=username, email=email, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created, you can login now', 'success')
        return redirect(url_for('signin'))
    return render_template("signup.html", app=app, form=form)
    
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        flash('Logged in, please logout to register or login as another user','info')
        return redirect(url_for('index'))
    app = {
        "title":"Sign In",
        "heading":"Login"
    }

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        remember = form.remember.data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Welcome {email}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Failed. Please check username and password', 'danger')
    return render_template("signin.html", app=app, form=form)

@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('signin'))


@app.route('/post/business', methods=['POST', 'GET'])
@login_required
def newBiz():
    app = {
        "title": "New Business",
        "heading": "Create New Business"
    }
    form = RegBusinessForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        description = form.description.data
        category = form.category.data
        county = form.county.data
        region = form.region.data
        location = form.location.data

        #Explode values of category into list
        catList = category.split(",")
        
        return redirect(url_for('index'))
    return render_template('create_business.html', app=app, form=form)

@app.route('/update/business/<int:id>', methods=['POST', 'GET'])
def updateBusiness(id):
    data = business_data[id]
    app = {
        "title": "Update Business",
        "heading": "Update Business"
    }
    form = UpdateBusinessForm()
    if form.validate_on_submit():
        pass
        flash(f'validation successful', 'success')
    return render_template('update_business.html', app=app, form=form)