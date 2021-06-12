import jwt
from functools import wraps
from flask import request, current_app
from app.api.errors import unauthorized


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']

        if not token:
            return unauthorized('Token is missing!')
            
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return f(data, *args, **kwargs)
        except:
            return unauthorized('Token is invalid!')

    return decorated