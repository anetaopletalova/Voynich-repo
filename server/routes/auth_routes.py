import jwt
from flask import Blueprint, request, jsonify, make_response, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from server.db.database import db
from server.db.models import User
from server.utils.helpers import generate_token

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


@auth.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('user does not exist', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    if check_password_hash(user.password, auth.password):
        token = generate_token(user.id, 'access')
        refresh_token = generate_token(user.id, 'refresh')

        response = jsonify({'token': token, 'refresh_token': refresh_token, 'user_id': user.id, 'email': user.email})
        return response

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


@auth.route('/refresh', methods=['POST'])
def refresh_token():
    req = request.get_json()
    refresh_tok = req["refresh_token"]
    data = jwt.decode(refresh_tok, current_app.config['SECRET_KEY'], 'HS256')
    current_user = User.query.filter_by(id=data['uid']).first()
    token = generate_token(current_user.id, 'access')
    new_refresh_token = generate_token(current_user.id, 'refresh')
    # TODO add user here to be able to login
    response = jsonify({'token': token, 'refresh_token': new_refresh_token})
    return response
