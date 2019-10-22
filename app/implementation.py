import json
import requests
import jwt
import datetime
from passlib.hash import sha256_crypt
from api_management import getpath
from schema import Schema, And, Use

user_get_request = getpath('users/')

headers = {'content-type': 'application/json'}
secret = 'planthealthcare'


def checkLogin(request, adminFlag):
    try:
        username = request.json['username']
        password = request.json['password']

        get_user = requests.get(user_get_request + username)

        status = get_user.status_code

        if status == 204:
            return {'msg': 'User with that username does not exist.'}, 401
        elif status != 200:
            return {'msg': 'User-management API is not available.'}, 500

        data = get_user.json()

        if adminFlag:
            if data['admin'] == 'False':
                return {'msg': 'Authorization error. User is not administrator!'}, 401

        if sha256_crypt.verify(password, data['password']):
            print('Passwords match!')
            response = create_response(data)
            encoded_jwt = jwt.encode(response, secret, algorithm='HS256').decode('utf-8')

            return {'token': str(encoded_jwt)}

        else:
            print('Passwords do not match!')
            return {'msg': 'Authorization error. Credentials do not match!'}, 401

    except Exception as e:
        print(e)
        return {"msg": "Something went wrong while authenticating user."}, 500


def checkRegister(request):
    try:
        try:
            schema = getSchema()
            schema.validate(request.json)
        except Exception as e:
            return {'msg': 'Data is not valid.'}, 403

        validated_data = request.json

        get_user = requests.get(user_get_request + validated_data['username'])
        status = get_user.status_code

        if status == 200:
            return {'msg': 'User with that username already exist. Please choose another one.'}, 422

        send_user = requests.post(user_get_request, headers=headers, data=json.dumps(validated_data))

        status_code = send_user.status_code
        if status_code == 201:
            return {'msg': 'User registered successfully'}, 201
        else:
            return {'msg': 'User registration failed successfully'}, 500

    except Exception as e:
        print(e)
        return {"msg": "Something went wrong while registering user."}, 500


def create_response(data):
    new_data = {}
    new_data['user_id'] = data['user_id']
    new_data['first_name'] = data['first_name']
    new_data['last_name'] = data['last_name']
    new_data['username'] = data['username']
    new_data['email'] = data['email']
    new_data['admin'] = data['admin']
    new_data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=2)

    return new_data


def getSchema():
    return Schema({'first_name': And(str, len),
                   'last_name': And(str, len),
                   'username': And(str, len),
                   'email': And(str, len),
                   'admin': And(Use(bool)),
                   'password': And(str, len)})
