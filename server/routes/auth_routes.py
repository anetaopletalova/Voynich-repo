import datetime
import json

import jwt
from flask import Blueprint, request, jsonify, make_response, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from server.db.database import db
from server.db.models import User

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        email=data.get('email'),
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})


@auth.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('user does not exist', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    if check_password_hash(user.password, auth.password):
        key = current_app.config['SECRET_KEY']
        date = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode({'public_id': user.id, 'exp': date}, key)
        response = jsonify({'token': token, 'user_id': user.id, 'email': user.email})
        response.headers.add("Access-Control-Allow-Origin", "*")
        # response.headers.add('Access-Control-Allow-Headers', "*")
        # response.headers.add('Access-Control-Allow-Methods', "*")
        return response

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
