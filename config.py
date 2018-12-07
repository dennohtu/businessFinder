import os

DEBUG = True
TESTING = True ##Testing environment for pytest
##Secret key to handle cookie encryption
SECRET_KEY = '9e08f244b77f44ca910461519b2e0ed6'
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql:///business_finder'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']