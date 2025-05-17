import pytest
from backend.server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_credentials():
    creds = {
        'name': 'test_user_1',
        'password': 'test_pass_1',
    }
    return creds.copy()

def test_login(client, sample_credentials):
    response = client.post('/login', json=sample_credentials).get_json()
    assert response['success'] == True

    sample_credentials['password'] = 'wrong_pass'
    response = client.post('/login', json=sample_credentials).get_json()
    assert response['success'] == False

    sample_credentials['name'] = 'no_user'
    response = client.post('/login', json=sample_credentials).get_json()
    assert response['success'] == False