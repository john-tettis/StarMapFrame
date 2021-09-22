from sqlite3.dbapi2 import Connection, OperationalError
from flask.wrappers import Response

from app.middleware import login_required
from . import blueprint, get_db, to_json
from flask import request, jsonify


@blueprint.route('/discounts', methods=['GET'])
@login_required
def discounts_get() -> Response:
    """List of all discounts available in database

    Returns:
        `Response`: return `result: True` with all discount codes if request is succeed. Otherwise `return: Flase` with a message
    """
    db: Connection = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM discounts")
        rows: list = cursor.fetchall()
        fields = cursor.description
        discounts = to_json(rows, fields)
        return jsonify(result=True, message="Succeed", discounts=discounts)
    except OperationalError as e:
        return jsonify(result=False, message="Something went wrong...", error=str(e))


@blueprint.route('/discounts/', methods=['POST'])
@login_required
def discounts_add() -> Response:
    """Create a discount by giving a discount `code` and `amount`!

    Returns:
        `Response`: `result: True` if the discount creation succeed otherwise return `False`
    """
    data: dict = request.json
    db: Connection = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO discounts (code, amount) VALUES (?, ?)",
                       (data['code'], data['amount']))
        db.commit()
        return jsonify(result=True, message="Succeed")
    except OperationalError as e:
        return jsonify(result=False, message="Something went wrong...", error=str(e))


@blueprint.route('/discounts/<id>', methods=['DELETE'])
@login_required
def discounts_delete(id: int) -> Response:
    """Removes a discount by giving an id

    Args:
        `id (int)`: discount id from database

    Returns:
        `Response`: `result: True` if the discount deleted successfully! otherwise result will be `False`
    """
    db: Connection = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM discounts where id=?", (id))
        db.commit()
    except OperationalError as e:
        return jsonify(result=False, message="Something went wrong...", error=str(e))
    finally:
        return jsonify(result=True, message="Succeed")

@blueprint.route('/discounts/<code>', methods=['POST'])
def discount_available(code: str) -> Response:
    db: Connection = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT * FROM discounts where code=\"{code}\"")
        code = cursor.fetchone()
        return jsonify(result=True, discount=code)
    except OperationalError as e:
        return jsonify(result=False, message="Something went wrong...", error=str(e))

