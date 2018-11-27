from flask import render_template, url_for, flash, redirect
from app import app
#Using FlaskForm to create forms...makes work much easier to do and maintain
from .forms import RegistrationForm, LoginForm, RegBusinessForm
##Handles all data
from .database import User, Business, Category
##Session handler
from .session import Session
##encrypts passwords
from flask_bcrypt import Bcrypt

##Empty user dict
user_data = dict()
##Empty business dict
business_data = dict()
##Bcrypt instance to hash paswords
bcrypt = Bcrypt(app)

@app.context_processor
def logedin():
    return dict(loggedIn=Session.isLoggedIn())

@app.route("/")
@app.route("/index")
def index():
    app = {
        "title":"Business Finder",
        "heading": "Home"
    }
    return render_template("index.html", app=app)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    app = {
        "title":"Signup",
        "heading":"Create Account"
    }
    form = RegistrationForm()
    #if data passes validation,
    #Is added to a sublist then added to the user_data
    #A redirect is made to the login page with success message
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        email = form.email.data
        username = form.username.data
        user = User(email, username, hashed_pw)
        user_list = {email:user}
        user_data.update(user_list)
        flash(f'Account for {email} created', 'success')
        return redirect(url_for('signin'))
    return render_template("signup.html", app=app, form=form)
    
@app.route("/signin", methods=['GET', 'POST'])
def signin():
    app = {
        "title":"Sign In",
        "heading":"Login"
    }
    #Check if user is already logged in
    #Redirects if is logged in
    if Session.isLoggedIn() is True:
        flash(f"Logged In",'success')
        return redirect(url_for('index'))
    form = LoginForm()
    #If data passes validation,
    #Email given is used to search for a key with matching email
    #If a match is found, the hashed password stored in the user object is compared
    #using bcrypt's check_password_hash for a
    #match in passwords
    #If a the passwords match, user is redirected to home page with success message
    #If passwords don't match, or email is not found in any of the sublists,
    #If remember Me is ticked, cookie created for the user until he logs out
    #Error message displayed on the login page
    if form.validate_on_submit():
        email = form.email.data
        remember = form.remember.data
        if user_data.get(email) is not None:
            user = user_data[email]
            password = user.printPassword()
            if bcrypt.check_password_hash(password, form.password.data):
                if remember is True:
                    pass
                Session.createSession(user.printUsername())
                flash(f"Successfully Logged in", 'success')
                return redirect(url_for('index'))
            else:
                flash(f"Incorrect username or password", 'danger')
                return redirect(url_for('signin')) 
        else:
            flash(f"Incorrect username or password", 'danger') 
    return render_template("signin.html", app=app, form=form)

@app.route('/signout')
def signout():
    if Session.isLoggedIn():
        Session.dropSession()
    
    return redirect(url_for('signin'))
@app.route('/post/business', methods=['POST', 'GET'])
def newBiz():
    ##Getting business Ids
    if not business_data:
        counter = 1
    else:
        counter = int(list(business_data.keys())[-1]) + 1
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

        #Create new business instance
        biz = Business(name, email, description)
        #Explode values of category into list
        catList = category.split(",")
        #Loop through list creating categories and adding them to business
        catid = 1
        for category in catList:
            cat = Category(catid, category)
            biz.addItem('category', cat.returnCategory())
            catid = catid + 1
        business_data.update({counter:biz.returnBusiness()})
        flash(f"New business {name} created", 'success')
        #Incomplete hence will fail
        redirect(url_for('location'))
    return render_template('create_business.html', app=app, form=form)