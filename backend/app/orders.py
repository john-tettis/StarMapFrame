
from sqlite3.dbapi2 import OperationalError

import requests
from flask import jsonify, redirect, request
from flask.wrappers import Response

from app.middleware import login_required

from . import HOST, FRONTEND, blueprint, get_db, to_json


@blueprint.route("/orders", methods=['GET', 'POST'])
def orders_list() -> Response:
    """Insert order into database if the `request.method` is `POST`. otherwise with a `GET` request it returns all of the orders available in the database

    Returns:
        `Response`: `reuslt: True` if request is succeed otherwise `result: Flase`
    """
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        data = request.json
        cursor.execute(
            "INSERT INTO orders (name, mobile, address, province, city, post, is_paid, is_deliverd, is_printed, product, amount, tracking, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (data['name'], data['mobile'], data['address'], data['province'], data['city'], data['post'], data['is_paid'], data['is_deliverd'], 0, str(data['product']), data['amount'], data['tracking'], data['timestamp']))
        db.commit()
        return jsonify(result=True, message="inserted", id=cursor.lastrowid)
    elif request.method == 'GET':
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        fields = cursor.description
        orders = to_json(rows, fields)
        return jsonify(result=True, data=orders)
    return jsonify(result=False, message="Request method is not allowed!")


@blueprint.route("/orders/<id>", methods=["DELETE"])
@login_required
def orders_del(id: int) -> Response:
    """Removes a order from database with it's `id`. To validate `DELETE` you should pass token in your `request.cookies`

    Args:
        id (int): order id

    Returns:
        Response: `result: True` if the order delete succeed otherwise `result: False`
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM orders where id={id}")
    rows = cursor.fetchall()
    if len(rows) > 0:
        cursor.execute(f"DELETE FROM orders where id={id}")
        db.commit()
        return jsonify(result=True, message="successfully deleted")
    else:
        return jsonify(result=False, message="there is no order with that id")


@blueprint.route("/orders/edit/<id>", methods=["POST"])
def orders_update_product(id: int) -> Response:
    data = request.json
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            f"UPDATE orders SET product=\"{data['product']}\" WHERE id={id}")
        db.commit()
        return jsonify(result=True, message="OK!")
    except OperationalError as e:
        return jsonify(result=False, message="NOT OK!", error=str(e))


@blueprint.route("/orders/setPrinted/<id>", methods=["POST"])
@login_required
def orders_update_print_status(id: int) -> Response:
    db = get_db()
    cursor = db.cursor()
    data = request.json
    try:
        cursor.execute(
            f"UPDATE orders SET is_printed={data['status']} WHERE id={id}")
        db.commit()
        return jsonify(result=True, message="OK!")
    except OperationalError as e:
        return jsonify(result=False, message="NOT OK!", error=str(e))


@blueprint.route("/orders/verify/<id>/<amount>", methods=["POST"])
def order_payment_verify(id: int, amount: int) -> Response:
    data = request.json
    headers = {
        "Authorization": "Bearer a6a01a56fb0505ee3e808f597958ba488ef93ffc2743b60c80dc55a3f348f43b",
        "Content-Type": "application/json"
    }

    response = requests.post(url="https://api.payping.ir/v2/pay/verify/", headers=headers, data={
        "refId": data['refid'],
        "amount": amount
    })

    if response.status_code == 200:
        if orders_update_payment_status(id=id):
            return redirect(location=FRONTEND + "/verify?status=true&updated=true", code=204)
        return redirect(location=FRONTEND + "/verify?status=true&updated=false", code=409)
    return redirect(location=FRONTEND + "/verify?status=false&updated=false", code=400)


def orders_update_payment_status(id: int) -> bool:
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT * from orders WHERE id={id}")
        row = cursor.fetchone()
        if row:
            cursor.execute(f"UPDATE orders SET is_paid=1 WHERE id={id}")
            db.commit()
            return True
        else:
            return False
    except OperationalError as e:
        return False
