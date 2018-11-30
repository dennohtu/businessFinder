import pytest
from app import app

@pytest.fixture(scope='module')
def test_client(request):
    app_client = app.test_client()

    ctx = app.app_context()
    ctx.push()
    yield app_client
    ctx.pop()