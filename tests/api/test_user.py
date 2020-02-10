import json


from url_shortener.api import users
from url_shortener.models import User, RevokedToken
from url_shortener.extensions import db


def test_user_register(app):
    with app.test_client() as client:
        response = register_user(client, 'luis', 'luis@gmail.com', 'pass123')
        data = json.loads(response.data.decode())
        assert response.status_code == 200
        assert data['success']
        assert data.get('access_token')
        assert data.get('refresh_token')

        user = db.session.query(User).first()
        assert user.username == 'luis'
        assert user.email == 'luis@gmail.com'
        assert user.check_password('pass123')


def test_user_register_duplicate(app):
    with app.test_client() as client:
        register_user(client, 'luis', 'luis@gmail.com', 'pass123')
        response = register_user(client, 'luis', 'luis@yahoo.com', 'pass345')
        data = json.loads(response.data.decode())
        assert not data['success']
        assert data['message'] == "User 'luis' already exists"


def test_user_login(app):
    with app.test_client() as client:
        reg_response = register_user(client, 'luis', 'luis@gmail.com', 'pass123')
        reg_data = json.loads(reg_response.data.decode())
        login_response = login_user(client, 'luis', 'pass123')
        login_data = json.loads(login_response.data.decode())

        assert login_data['success']
        assert reg_data['access_token'] != login_data['access_token']
        assert reg_data['refresh_token'] != login_data['refresh_token']


def test_user_login_missing_user(app):
    with app.test_client() as client:
        response = client.post(
            '/login',
            data=json.dumps(dict(
                username='max',
                password='pass123'
            )),
            content_type='application/json'
        )

        data = json.loads(response.data.decode())
        assert not data['success']
        assert data['message'] == "User 'max' does not exist"


def test_user_login_invalid_password(app):
    with app.test_client() as client:
        register_user(client, 'luis', 'luis@gmail.com', 'pass123')
        response = client.post(
            '/login',
            data=json.dumps(dict(
                username='luis',
                password='pass345'
            )),
            content_type='application/json'
        )

        data = json.loads(response.data.decode())
        assert not data['success']
        assert data['message'] == "Incorrect password"


def test_logout_access_token(app):
    with app.test_client() as client:
        response = register_user(client, 'luis', 'luis@gmail.com', 'pass123')
        access_token = json.loads(response.data.decode())['access_token']
        response = client.post(
            '/logout/access',
            headers={"Authorization": f"Bearer {access_token}"}
        )

        data = json.loads(response.data.decode())
        assert data['success']


def test_logout_refresh_token(app):
    with app.test_client() as client:
        response = register_user(client, 'luis', 'luis@gmail.com', 'pass123')
        refresh_token = json.loads(response.data.decode())['refresh_token']
        response = client.post(
            '/logout/refresh',
            headers={"Authorization": f"Bearer {refresh_token}"}
        )

        data = json.loads(response.data.decode())
        assert data['success']


def test_access_token_refresh(app):
    with app.test_client() as client:
        response = register_user(client, 'luis', 'luis@gmail.com', 'pass123')
        old_access_token = json.loads(response.data.decode())['access_token']
        refresh_token = json.loads(response.data.decode())['refresh_token']

        response = client.post(
            '/token/refresh',
            headers={"Authorization": f"Bearer {refresh_token}"}
        )
        data = json.loads(response.data.decode())

        assert data['success']
        assert data['access_token'] != old_access_token


###################################################################################################
# Helper functions
###################################################################################################
def register_user(client, username, email, password):
    response = client.post(
        '/registration',
        data=json.dumps(dict(
            username=username,
            email=email,
            password=password
        )),
        content_type='application/json',
    )
    return response


def login_user(client, username, password):
    response = client.post(
        '/login',
        data=json.dumps(dict(
            username=username,
            password=password
        )),
        content_type='application/json'
    )
    return response
