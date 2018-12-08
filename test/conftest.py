import pytest
from app import app

@pytest.fixture(scope='module')
def test_client(request):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dennoh:admin@localhost/business_finder_dennohtu_test'
    app.config['WTF_CSRF_ENABLED'] = False
    app_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield app_client
    ctx.pop()