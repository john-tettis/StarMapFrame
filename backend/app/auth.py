import secrets
from sqlite3.dbapi2 import OperationalError

from bcrypt import checkpw, gensalt, hashpw
from flask import jsonify, request

from . import blueprint, get_db


@blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data['username']
    password = data['password'].encode("utf-8")
    db = get_db()
    c = db.cursor()
    try:
        c.execute(f'SELECT * FROM users WHERE username="{username}"')
        row = c.fetchone()
        if row and checkpw(password, row[3]):
            token = secrets.token_hex(16)
            c.execute(
                "INSERT INTO tokens (userID, token) VALUES (?, ?)", (row[0], token))
            return jsonify(result=True, message="logged in successfully", token=token)
        else:
            return jsonify(result=False, message="نام کاربری یا رمز عبور صحیح نیست...")
    except OperationalError as e:
        return jsonify(result=False, message="شما در رسپینا اکانت ندارید :(")


@blueprint.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data['name']
    username = data['username']
    password = data['password'].encode('utf-8')

    db = get_db()
    c = db.cursor()
    try:
        hashed = hashpw(password, gensalt(10))
        query = "INSERT INTO users (name, username, password) VALUES (?, ?, ?)"
        c.execute(query, (name, username, hashed))
        db.commit()
        return jsonify(result=True, message="Succefully signed up")
    except OperationalError as e:
        return jsonify(result=False, message="خطایی عجیبی پیش اومده! لطفا بعدا تلاش کنید...", error=str(e))
