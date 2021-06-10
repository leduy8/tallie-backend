from app import app, db 
from ..models import User


@app.route('/api/users', methods=['POST'])
def user_register():
    pass


@app.route('/api/users/<id>')
def user_lookup(id):
    pass


@app.route('/api/users/me')
def user_profile():
    pass


@app.route('/api/users/me', methods=['PUT'])
def user_update():
    pass


@app.route('/api/auth', methods=['POST'])
def user_login():
    pass


@app.route('/api/auth/validate')
def user_validation():
    pass


