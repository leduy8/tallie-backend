from flask import render_template, request
from app import db
from app.errors import bp
from app.api.errors import bad_request as api_bad_request, internal_server_error as api_internal_server_error


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def not_found(error):
    if wants_json_response:
        return api_bad_request()
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_internal_server_error()
    return render_template('errors/500.html'), 500