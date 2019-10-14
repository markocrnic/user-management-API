import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../app'))

from interface import app
from flask import json


# Test usermanagement adminlogin successfully
def test_usermanagement_adminlogin_succsessful():
    response = app.test_client().post('/usermanagement/adminlogin/', json={
        "username": "mcrnic",
        "password": "password"
    })

    assert response.status_code == 200


# Test usermanagement adminlogin unsuccessfully user does not exist
def test_usermanagement_adminlogin_unsuccsessful_user_doesnt_exist():
    response = app.test_client().post('/usermanagement/adminlogin/', json={
        "username": "notexisting",
        "password": "passwords"
    })

    assert response.status_code == 401 and json.loads(response.get_data(as_text=True)) == {'msg': 'User with that username does not exist.'}


# Test usermanagement adminlogin unsuccessfully user not admin
def test_usermanagement_adminlogin_unsuccsessful_user_not_admin():
    response = app.test_client().post('/usermanagement/adminlogin/', json={
        "username": "igajic",
        "password": "password"
    })

    assert response.status_code == 401 and json.loads(response.get_data(as_text=True)) == {'msg': 'Authorization error. User is not administrator!'}


# Test usermanagement adminlogin unsuccessfully invalid credentials
def test_usermanagement_adminlogin_unsuccsessful_invalid_credentials():
    response = app.test_client().post('/usermanagement/adminlogin/', json={
        "username": "mcrnic",
        "password": "passwords"
    })

    assert response.status_code == 401 and json.loads(response.get_data(as_text=True)) == {'msg': 'Authorization error. Credentials do not match!'}


# Test usermanagement login successfully
def test_usermanagement_login_succsessful():
    response = app.test_client().post('/usermanagement/login/', json={
        "username": "mcrnic",
        "password": "password"
    })

    assert response.status_code == 200


# Test usermanagement login unsuccessfully user does not exist
def test_usermanagement_login_unsuccsessful_user_doesnt_exist():
    response = app.test_client().post('/usermanagement/login/', json={
        "username": "notexisting",
        "password": "passwords"
    })

    assert response.status_code == 401 and json.loads(response.get_data(as_text=True)) == {'msg': 'User with that username does not exist.'}


# Test usermanagement login unsuccessfully invalid credentials
def test_usermanagement_login_unsuccsessful_invalid_credentials():
    response = app.test_client().post('/usermanagement/login/', json={
        "username": "mcrnic",
        "password": "passwords"
    })

    assert response.status_code == 401 and json.loads(response.get_data(as_text=True)) == {'msg': 'Authorization error. Credentials do not match!'}


# Test usermanagement register unsuccessfully
def test_usermanagement_register_unsuccsessful():
    response = app.test_client().post('/usermanagement/register/', json={
        "username": "mcrnic",
        "password": "passwords",
        "email": "marko.crnic@devoteam.com"
    })

    assert response.status_code == 403
