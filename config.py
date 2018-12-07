import os

DEBUG = True
TESTING = True ##Testing environment for pytest
##Secret key to handle cookie encryption
SECRET_KEY = '9e08f244b77f44ca910461519b2e0ed6'
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgres://idgpqqmnrirjmj:6e6828faeb52f1b5207bf1a01f5934d86912dcd9e3769da6e2ac436360c3e75d@ec2-54-227-249-201.compute-1.amazonaws.com:5432/d5opu981qotjc0'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']