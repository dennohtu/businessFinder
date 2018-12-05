import os ##Save image to disk
import secrets #Give image random name
from PIL import Image ##Resize image
from flask import render_template, url_for, flash, redirect, request, abort, request
from app import app, db, bcrypt
#Using FlaskForm to create forms...makes work much easier to do and maintain
from .forms import RegistrationForm, LoginForm, RegBusinessForm, UpdateAccountForm, CompleteBusinessProfile, WriteReviewForm
##Handles all data
from .model import User, Business, Category, Location, Review
from flask_login import login_user, current_user, logout_user, login_required

##Home page, apps landing page endpoint
@app.route("/", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    app = {
        "title":"Business Finder",
        "heading": "Home"
    }
    data = Business.query.all()
    return render_template("index.html", app=app, data=data)

##About page endpoint
@app.route('/about', methods=['GET'])
def about():
    body = "This site was founded by Dennis Mureithi in 2018. It aims at connecting consumers and businesses by creating an easy platform for searching for what they desire. This site is not the actual business!"
    app = {
        "title":"About us",
        "body" : body
    }
    return render_template('about.html', app=app, locations=locAndCat()[1], categories=locAndCat()[0])

##Register user endpoint
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
    return render_template("signup.html", app=app, form=form, locations=locAndCat()[1], categories=locAndCat()[0])

##Login User endpoint
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
    return render_template("signin.html", app=app, form=form, locations=locAndCat()[1], categories=locAndCat()[0])

#Method to save image to filesystem
#Returns image name to save to database
def save_prof_pic(form_picture):
    #Random name to give to image
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    pic_name = random_hex + f_ext
    path = os.path.join(app.root_path, 'static/profile_pics', pic_name)
    ##Resize image to 125x125 pixels (icon size)
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    ##Save resized image
    img.save(path)

    return pic_name

##User account Endpoint, Account editing done heree
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    app = {
        "title":"Account Page",
        "heading":"My Account",
        "image_file":url_for('static', filename='profile_pics/'+current_user.image_file)
    }
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            pic_file = save_prof_pic(form.profile_pic.data)
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', app=app, form=form, locations=locAndCat()[1], categories=locAndCat()[0])

#logout Endpoint
@app.route('/signout', methods=['POST', 'GET'])
def signout():
    logout_user()
    return redirect(url_for('signin'))

#Register new Business Endpoint
#Successful registration transfers user to page to add location and categories
@app.route('/new/business', methods=['POST', 'GET'])
@login_required
def newBiz():
    app = {
        "title": "New Business",
        "heading": "Create New Business",
        "legend": "New Business"
    }
    form = RegBusinessForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        description = form.description.data
        business = Business(name=name, description=description, owner=current_user)
        db.session.add(business)
        db.session.commit()
        return redirect(url_for('completeBizProfile', biz_id=business.id))
    elif request.method == 'GET':
        form.email.data = current_user.email
    return render_template('create_business.html', app=app, form=form, locations=locAndCat()[1], categories=locAndCat()[0])

##Endpoint to add categories and location
@app.route('/business/<int:biz_id>/completeprofile', methods=['POST', 'GET'])
@login_required
def completeBizProfile(biz_id):
    data = Business.query.get_or_404(biz_id)
    app = {
        "title": "Business Profile"
    }
    form = CompleteBusinessProfile()
    if form.validate_on_submit():
        category = form.category.data
        county = form.county.data
        region = form.region.data
        location = form.location.data
        #Explode values of category into list
        catList = category.split(",")
        for cat in catList:
            category = Category(category=cat, business=data)
            db.session.add(category)
        loc = Location(business=data, county=county, region=region, location=location)
        db.session.add(loc)
        db.session.commit()
        flash("New Business successfully created", 'success')
        return redirect(url_for('index'))
    return render_template('complete_business.html', app=app, form=form, locations=locAndCat()[1], categories=locAndCat()[0])

##Get business by id endpoint, displays all information related to the business
@app.route('/business/<int:biz_id>', methods=['POST', 'GET'])
def business(biz_id):
    data = Business.query.get_or_404(biz_id)
    category = Category.query.filter_by(business_id=biz_id).all()
    location = Location.query.filter_by(business_id=biz_id).all()
    review = Review.query.filter_by(business_id=biz_id).all()
    app = {
        "title": "Business Profile",
        "heading": "Business Info"
    }
    return render_template('business_info.html', app=app, post=data, categoriess=category, locationss=location, reviews=review, locations=locAndCat()[1], categories=locAndCat()[0])

#Update business endpoint
#One has to be logged iin to access this page
@app.route('/business/<int:biz_id>/update', methods=['POST', 'GET'])
@login_required
def updateBusiness(biz_id):
    app = {
        "title": "Update Business Profile",
        "legend": "Update Business"
    }
    biz_data = Business.query.get_or_404(biz_id)
    biz_cat = Category.query.filter_by(business_id=biz_id).all()
    biz_loc = Location.query.filter_by(business_id=biz_id).all()
    ##Fetch db categories and location counties and add to a list
    dbList = []
    counties = []
    ##Append category
    for categ in biz_cat:
        dbList.append(categ.category)
    ##Append location
    #This will be used to see if a location exists, if it doesn't, new is created
    for county in biz_loc:
        counties.append(county.county)
    if biz_data.owner != current_user:
        abort(403)
    #Forms to be used in this page
    form = RegBusinessForm()
    compForm = CompleteBusinessProfile()
    if form.validate_on_submit():
        #if business name in db and one in form field dont match, name is updated in db
        if biz_data.name != form.name.data:
            biz_data.name = form.name.data
        biz_data.description = form.description.data
        #If county in form field is in the list of counties, the location object is updated, 
        #Otherwise new location is created
        if compForm.county.data in counties: 
            for location in biz_loc:
                if location.county == compForm.county.data:
                    location.county = compForm.county.data
                    location.region = compForm.region.data
                    location.location = compForm.location.data
        else:
            location = Location(business=biz_data, county=compForm.county.data, region=compForm.region.data, location=compForm.location.data)
            db.session.add(location)
        ##End of location update
        category = compForm.category.data
        #Explode values of category into list
        catList = category.split(",")
        ##Use to compare if category value exists, if not, is added
        for cat in catList:
            if cat not in dbList:
                category = Category(category=cat, business=biz_data)
                db.session.add(category)
        db.session.commit()
        flash("Business profile updated", 'success')
        return redirect(url_for('business', biz_id=biz_data.id))
    elif request.method == 'GET':
        ##Populate database info in fields
        form.email.data = biz_data.owner.email
        form.name.data = biz_data.name
        form.description.data = biz_data.description
        compForm.category.data = ",".join(dbList)
        for location in biz_loc:
            compForm.county.data = location.county
            compForm.region.data = location.region
            compForm.location.data = location.location
    return render_template('create_business.html', app=app, form=form, comp_form=compForm)

##This endpoint deletes business categories and locations specifically
@app.route('/business/<int:biz_id>/<category>/<int:cat_id>/delete', methods=['POST', 'GET'])
@login_required
def updateBusinessInfo(biz_id, category, cat_id):
    if category == 'category':
        to_delete = Category.query.get_or_404(cat_id)
    elif category == 'location':
        to_delete = Location.query.get_or_404(cat_id)
    db.session.delete(to_delete)
    db.session.commit()
    flash('Business Info successfully updated', 'success')
    return redirect(url_for('business', biz_id=biz_id))

##Delete Business Endpoint. Business and all associated data are deleted
@app.route('/business/<int:biz_id>/delete', methods=['POST'])
@login_required
def deleteBusiness(biz_id):
    app = {
        "title": "Delete Business"
    }
    biz_data = Business.query.get_or_404(biz_id)
    biz_cat = Category.query.filter_by(business_id=biz_id).all()
    biz_loc = Location.query.filter_by(business_id=biz_id).all()
    if biz_data.owner != current_user:
        abort(403)
    db.session.delete(biz_data)
    for category in biz_cat:
        db.session.delete(category)
    for location in biz_loc:
        db.session.delete(location)
    db.session.commit()
    flash('Business deleted!', 'success')
    return redirect(url_for('index'))

##Write new review
@app.route('/business/<int:biz_id>/review/<int:rev_id>', methods=['POST', 'GET'])
@login_required
def review(biz_id, rev_id):
    app = {
        "title":"Write review"
    }
    if rev_id != 0:
        rev_data = Review.query.get(rev_id)
    biz_data = Business.query.get(biz_id)
    if biz_data.owner == current_user:
        abort(403)
    form = WriteReviewForm()
    if form.validate_on_submit():
        email = form.email.data
        message = form.message.data
        if rev_id == 0:
            review = Review(business=biz_data, email=email, message=message)
            db.session.add(review)
        else:
            rev_data.email = form.email.data
            rev_data.message = form.message.data
        db.session.commit()
        flash("Review added successfully", 'success')
        return redirect(url_for('business', biz_id=biz_id))
    elif request.method == 'GET':
        form.email.data = current_user.email
        if rev_id !=0:
            form.message.data = rev_data.message
    return render_template('review.html', app=app, form=form)

#Update/delete existing review
@app.route('/business/review/<int:rev_id>/<action>', methods=['POST', 'GET'])
@login_required
def updateReview(rev_id, action):
    app = {
        "title":"Update review"
    }
    rev_data = Review.query.get_or_404(rev_id)
    if rev_data.email != current_user.email:
        abort(403)
    if action == 'delete':
        db.session.delete(rev_data)
        db.session.commit()
        flash('deleted!', 'success')
        return redirect(url_for('business', biz_id=rev_data.business_id))
    elif action == 'update':
        return redirect(url_for('review', biz_id=rev_data.business_id, rev_id=rev_id))

###Return location and categories to display on the sidebar
def locAndCat():
    locations = Location.query.all()
    categories = Category.query.all()
    ##Append categories to a list
    cat_list = []
    for category in categories:
        if category.category not in cat_list:
            cat_list.append(category.category)
    ##append counties to a list
    loc_list = []
    for location in locations:
        if location.county not in loc_list:
            loc_list.append(location.county)
    return [cat_list, loc_list]

##Search businesses by name/category/location
@app.route("/business/search/<category>", methods=["POST"])
def search(category):
    app = {
        "title":"Search",
        "heading": "Search Results"
    }
    businesses = searchItem(category)
    return render_template('index.html', app=app, data=businesses)

##Private method that returns a list of businesses
def searchItem(category):
    businesses = []
    if category == 'location':
        county = request.form["location"]
        #Get all locations with the county
        locations = Location.query.filter_by(county=county).all()
        biz_ids = []
        for location in locations:
            biz_ids.append(location.business_id)
        ##Get businesses by id and append to list
        for id in biz_ids:
            businesses.append(Business.query.get(id))
    elif category == 'category':
        category = request.form['category']
        #Get all categories that match
        categories = Category.query.filter_by(category=category).all()
        biz_ids = []
        for cat in categories:
            biz_ids.append(cat.business_id)
        ##Get businesses by ids
        for id in biz_ids:
            businesses.append(Business.query.get(id))
    elif category == 'name':
        name = request.form['search']
        #search businesses by name
        return Business.query.filter_by(name=name).all()
    return businesses 
