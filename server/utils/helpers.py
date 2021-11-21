from functools import wraps
import jwt
from flask import request, jsonify, current_app

from server.db.models import User


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        headers = request.headers
        bearer = headers.get('Authorization')  # Bearer YourTokenHere

        if not bearer:
            return jsonify({'message': 'a valid token is missing'})

        token = bearer.split()[1]

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], 'HS256')
            current_user = User.query.filter_by(id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator
