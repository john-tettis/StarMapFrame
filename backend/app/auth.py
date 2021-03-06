import secrets
from sqlite3.dbapi2 import OperationalError

from bcrypt import checkpw, gensalt, hashpw
from flask import json, jsonify, request
from flask.wrappers import Response

from . import blueprint, get_db


@blueprint.route("/login", methods=["POST"])
def login() -> Response:
    data = request.json
    username = data['username']
    password = data['password'].encode("utf-8")
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(f'SELECT * FROM users WHERE username="{username}"')
        row = cursor.fetchone()
        if row and checkpw(password, row[3]):
            token = secrets.token_hex(16)
            cursor.execute(
                "INSERT INTO tokens (userID, token) VALUES (?, ?)", (row[0], token))
            db.commit()
            return jsonify(result=True, message="logged in successfully", token=token)
        else:
            return jsonify(result=False, message="نام کاربری یا رمز عبور صحیح نیست...")
    except OperationalError as e:
        return jsonify(result=False, message="شما در رسپینا اکانت ندارید :(")


@blueprint.route("/register", methods=["POST"])
def register() -> Response:
    data = request.json
    name = data['name']
    username = data['username']
    password = data['password'].encode('utf-8')

    db = get_db()
    cursor = db.cursor()
    try:
        hashed = hashpw(password, gensalt(10))
        query = "INSERT INTO users (name, username, password) VALUES (?, ?, ?)"
        cursor.execute(query, (name, username, hashed))
        db.commit()
        return jsonify(result=True, message="Succefully signed up")
    except OperationalError as e:
        return jsonify(result=False, message="خطایی عجیبی پیش اومده! لطفا بعدا تلاش کنید...", error=str(e))

@blueprint.route("/token/<token>", methods=["GET"])
def check_token(token: str) -> Response:
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT * FROM tokens WHERE token=\"{token}\"")
        rows = cursor.fetchall()
        if(len(rows) > 0):
            return jsonify(result=True, message="valid")
        else:
            return jsonify(result=False, message="not valid token", rows=rows)
    except OperationalError as e:
        return jsonify(result=False, message="operational error", error=str(e))