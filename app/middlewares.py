import jwt
from functools import wraps
from flask import request, jsonify, current_app
from app.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return f(data, *args, **kwargs)
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

    return decorated