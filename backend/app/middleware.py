from functools import wraps
from flask import redirect, url_for, request

from . import get_db

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in request.headers:
            return redirect(url_for('respina.show_login_required_error', next=request.url))

        token = request.headers.get('token')
        if token:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM tokens where token=\"{token}\"")
            rows = cursor.fetchall()
            if len(rows) > 0:
                return f(*args, **kwargs)
        return redirect(url_for('respina.show_login_required_error', next=request.url))
    return decorated_function