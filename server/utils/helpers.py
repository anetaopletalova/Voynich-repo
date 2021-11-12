from functools import wraps

import flask
import jwt
from flask import request, jsonify, current_app

from server.db.models import User


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        # token = None

        headers = flask.request.headers
        bearer = headers.get('Authorization')  # Bearer YourTokenHere
        token = bearer.split()[1]

        # if 'x-access-tokens' in request.authorization:
        #     token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator
