import datetime
from functools import wraps
import jwt
from flask import request, jsonify, current_app, make_response
from server.db.models import User


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        headers = request.headers
        bearer = headers.get('Authorization')

        if not bearer:
            return make_response('not valid', 401)

        token = bearer.split()[1]

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], 'HS256')
            current_user = User.query.filter_by(id=data['uid']).first()
        except:
            return make_response('token is invalid', 401)

        return f(current_user, *args, **kwargs)

    return decorator


def generate_token(user_id, token_type):
    if token_type not in ('access', 'refresh'):
        raise ValueError

    key = current_app.config['SECRET_KEY']

    return jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(
        hours=(1 if token_type == 'access' else 168)),
                       'uid': user_id,
                       'type': token_type
                       },
                      key,
                      algorithm='HS256')


# def object_as_dict(obj):
#     return {c.key: getattr(obj, c.key)
#             for c in inspect(obj).mapper.column_attrs}

def as_dict(model):
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}
