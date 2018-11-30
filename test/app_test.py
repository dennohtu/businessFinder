

def test_index(test_client):
    home = test_client.get('/')
    assert home.status_code == 200
    assert b'' in home.data

def test_signup(test_client):
    signup = test_client.get('/new/business', follow_redirects=True)
    assert signup.status_code == 200