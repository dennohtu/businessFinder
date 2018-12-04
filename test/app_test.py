from app import db, bcrypt
from app.model import User, Business, Category, Location, Review

##Test database models if they work
##We will drop the database, create a new one and add test data to test
def test_models_create_db(test_client):
    ##Create database
    db.create_all()
    #Queries should return empty lists
    assert User.query.all() == []
    assert Business.query.all() == []
    assert Category.query.all() == []
    assert Location.query.all() == []
    assert Review.query.all() == []

def test_insert_data(test_client):
    ##New user
    db.session.add(User(username="testUser1", email="test@user@g.com",
     password=bcrypt.generate_password_hash("test").decode('utf-8')))
    db.session.add(User(username="testUser2", email="test2@user@g.com",
     password=bcrypt.generate_password_hash("test").decode('utf-8')))
    db.session.add(User(username="testUser3", email="test3@user@g.com",
     password=bcrypt.generate_password_hash("test").decode('utf-8')))
    ##New Business
    db.session.add(Business(owner=User.query.get(1), name="Business1",
     description="Some description"))
    db.session.add(Business(owner=User.query.get(2), name="Business2",
     description="Some description"))
    db.session.add(Business(owner=User.query.get(3), name="Business3",
     description="Some description"))
    ##Add location
    db.session.add(Location(business=Business.query.get(1), county='Kiambu',
     region='Lari', location='Some location'))
    db.session.add(Location(business=Business.query.get(2), county='Nairobi',
     region='Ruiru', location='Membley'))
    db.session.add(Location(business=Business.query.get(3), county='Kajiado',
     region='Some region', location='Some location'))
    ##Add Category
    db.session.add(Category(business=Business.query.get(1), category='Some category'))
    db.session.add(Category(business=Business.query.get(2), category='Some category'))
    db.session.add(Category(business=Business.query.get(3), category='Some category'))
    ##Add review
    db.session.add(Review(business=Business.query.get(1), email='test@user.com',
     message='Some message'))
    db.session.add(Review(business=Business.query.get(2), email='test1@user.com',
     message='Some message'))
    db.session.add(Review(business=Business.query.get(3), email='test2@user.com',
     message='Some message'))
    db.session.commit()


##Test the static links for succesful responses
#User involved pages
def test_home(test_client):
    home = test_client.get('/')
    assert home.status_code == 200

def test_about(test_client):
    about = test_client.get('/about')
    assert about.status_code == 200
    assert b'This site was founded by Dennis Mureithi in 2018' in about.data

def test_auth_pages(test_client):
    signup = test_client.get('/signup')
    assert signup.status_code == 200

    signin = test_client.get('/signin')
    assert signin.status_code == 200

def test_account(test_client):
    account = test_client.get('/account', follow_redirects=True)
    assert account.status_code == 200

def test_signout(test_client):
    signout = test_client.get('/signout', follow_redirects=True)
    assert signout.status_code == 200

##Business involved pages
def test_create_business_link(test_client):
    createAcc = test_client.get('/new/business', follow_redirects=True)
    assert createAcc.status_code == 200

def test_models_drop_db(test_client):
    ##Create database
    db.drop_all()
