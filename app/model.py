from datetime import datetime
from flask import url_for
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.png', nullable=False)
    password = db.Column(db.String(64), nullable=False)
    businesses = db.relationship('Business', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.username}','{self.email}','{self.image_file}')"

##Used to create a business object
##data returned will be in dictionary format using returnBusiness() function
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    categories = db.relationship('Category', backref='business', lazy=True)
    locations = db.relationship('Location', backref='business', lazy=True)
    reviews = db.relationship('Review', backref='business', lazy=True)

    def __repr__(self):
        return f"Business('{self.id}','{self.name}','{self.user_id}','{self.date_added}')"

##Creates a category object
#Returns a dictionary with id and category to be added to the business
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    category = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Category('{self.id}','{self.business_id}','{self.category}')"
    

##Creates a location object
#Returns a dictionary to be added to the business
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    county = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Location('{self.id}','{self.business_id}','{self.county}','{self.region}','{self.location}')"

##Creates a category object
#Returns a dictionary to be added to the business
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    stars = db.Column(db.Integer, nullable=False, default=3)

    def __repr__(self):
        return f"Review('{self.id}','{self.business_id}','{self.email}','{self.message}','{self.stars}')"
