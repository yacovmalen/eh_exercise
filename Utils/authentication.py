
from flask import request
from flask_restful import abort

from config import mongo_client


def is_authenticated(f):
    """Checks whether user's api is valid or raises error 401."""

    def decorator(*args, **kwargs):
        if 'SECURITY_TOKEN_AUTHENTICATION_KEY' not in request.headers or not is_token(request.headers['SECURITY_TOKEN_AUTHENTICATION_KEY']):
            abort(401)
        return f(*args, **kwargs)

    return decorator


def is_token(token):
    response = mongo_client.client.db.get_collection('users').find({'api_token': token})
    return len([res['api_token'] for res in response]) > 0
