import jwt
from flask import Blueprint, request, jsonify, make_response, current_app
from flask_accepts import responds, accepts
from werkzeug.exceptions import Unauthorized
from werkzeug.security import generate_password_hash, check_password_hash
from server.db.database import db
from server.db.models import User
from server.schema.auth import UserLoginSchema, UserSchema, UserSignUpSchema
from server.utils.helpers import generate_token

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
@accepts(UserSignUpSchema)
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    # TODO difference between data.get() and data[]
    new_user = User(
        email=data.get('email'),
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})


@auth.route('/login', methods=['POST'])
@responds(schema=UserLoginSchema(), status_code=200)
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        # BadRequests instead of make_response??
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response('user does not exist', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    if check_password_hash(user.password, auth.password):
        token = generate_token(user.id, 'access')
        refresh_token = generate_token(user.id, 'refresh')

        response = jsonify({'token': token, 'refresh_token': refresh_token, 'user': UserSchema().dump(user)})
        return response

    raise Unauthorized('could not verify.')


@auth.route('/refresh', methods=['POST'])
@responds(schema=UserLoginSchema(), status_code=200)
def refresh_token():
    req = request.get_json()
    refresh_tok = req["refresh_token"]
    data = jwt.decode(refresh_tok, current_app.config['SECRET_KEY'], 'HS256')
    user = User.query.filter_by(id=data['uid']).first()
    token = generate_token(user.id, 'access')
    new_refresh_token = generate_token(user.id, 'refresh')
    # response = jsonify({'token': token, 'refresh_token': new_refresh_token, 'user': current_user})
    response = jsonify({'token': token, 'refresh_token': refresh_token, 'user': UserSchema().dump(user)})
    return response
