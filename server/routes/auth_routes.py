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

    if check_password_hash(user.password, auth.password):
        key = current_app.config['SECRET_KEY']
        vdate = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode({'public_id': user.id, 'exp': vdate}, key)
        return jsonify(token)

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
