from flask import jsonify, request
from app import db
from app.api import bp
from .errors import bad_request, not_found
from ..models import User
from ..middlewares import token_required


@bp.route('/users', methods=['POST'])
def user_register():
    data = request.get_json() or {}

    if 'username' not in data or 'email' not in data or 'name' not in data or 'phone' not in data or 'password' not in data:
        return bad_request('Not enough infomation for registering')

    if User.query.filter_by(username=data['username']).first():
        return bad_request('Username is already taken')

    if User.query.filter_by(email=data['email']).first():
        return bad_request('Email is already taken')

    user = User(
        username=data['username'],
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify(user.get_user_info()), 201


@bp.route('/users/<id>')
def user_lookup(id):
    user = User.query.filter_by(id=id).first()
    return jsonify(user.get_user_info())


@bp.route('/users/me')
@token_required
def user_profile(decoded):
    user = User.query.filter_by(id=decoded['id']).first()
    return jsonify(user.get_user_info())


@bp.route('/users/me', methods=['PUT'])
@token_required
def user_update(decoded):
    data = request.get_json() or {}
    user = User.query.filter_by(id=decoded['id']).first()

    if not user:
        return not_found('User\'s not found')

    if 'email' not in data or 'name' not in data or 'phone' not in data or 'password' not in data  or 'address' not in data or 'bio' not in data:
        return bad_request('Please input all fields for user\'s update')

    user.name = data['name']
    user.phone = data['phone']
    user.address = data['address']
    user.bio = data['bio']
    if user.email != data['email']:
        user.email_activated = False
    user.email = data['email']
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify(user.get_user_info())