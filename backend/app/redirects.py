from os import error
from flask.json import jsonify
from . import blueprint

@blueprint.route("/error/login", )
def show_login_required_error():
    return jsonify(result=False, message="You are not authenticated...", error="Token is not valid")