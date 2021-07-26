from sqlalchemy import text

from . import app, client, database
from .test_db import insert_user

_app = app
_client = client


def setup_function():
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("TRUNCATE user"))
    database.execute(text("TRUNCATE suggestion_post"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))

    insert_user(database)


def teardown_function():
    pass


def test_sign_up_user(client):
    login_id = 'test01'
    name = 'test'
    data = {'login_id': login_id, 'name': name, 'password': 'asdf1234', "confirm_pw": 'asdf1234'}
    res = client.post('/user', json=data)

    try:
        assert res.ok
    except AssertionError:
        print(res)
        raise AssertionError

    res_data = res.json()
    assert res_data['login_id'] == login_id
    assert res_data['name'] == name


def test_user_login(client):
    res = client.post('/user/me/login', data={"login_id": 'USER4', "user_pw": '000000'})

    try:
        assert res.ok
    except AssertionError:
        print(res.json())
        raise AssertionError

    res_data = res.json()
    assert res_data['user'] is not None
    
    cookie = res.headers.get('Set-Cookie')

    assert 'HttpOnly' in cookie
    assert 'tk' in cookie
    assert 'rftk' in cookie


def test_refresh_access_token(client):
    # 토큰 발행
    res_login = client.post('/user/me/login', data={"login_id": 'USER4', "user_pw": '000000'})

    cookie = res_login.headers.get('Set-Cookie')
    (access_token_cookie, refresh_token_cookie) = cookie.split(',')
    access_token = access_token_cookie.split(';')[0].split('=')[1]

    # 쿠키에 담아 요청
    res_refresh = client.post('/user/me/token')
    try:
        assert res_refresh.ok
    except AssertionError:
        print(res_refresh)
        raise AssertionError

    cookie = res_refresh.headers.get('Set-Cookie')
    refreshed_access_token = cookie.split(';')[0].split('=')[1]

    assert 'HttpOnly' in cookie
    assert 'tk' in cookie
    try:
        assert refreshed_access_token != access_token
    except AssertionError:
        print(refreshed_access_token)
        print(access_token)
        raise AssertionError


def test_update_me(client):
    edit_user = {
        'email': 'test@test.test',
        'user_pw': '000000'
    }

    res = client.put('/user/me', json=edit_user)

    try:
        assert res.ok
    except AssertionError:
        print(res)
        raise AssertionError

    res_data = res.json()
    assert res_data['email'] == edit_user['email']
