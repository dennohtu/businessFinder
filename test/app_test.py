##First, test the static links for succesful responses
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