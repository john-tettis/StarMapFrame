
from sqlite3.dbapi2 import OperationalError

import json
import base64
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
            "INSERT INTO orders (name, mobile, address, province, city, post, is_paid, is_deliverd, is_printed, product, amount, tracking, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (data['name'], data['mobile'], data['address'], data['province'], data['city'], data['post'], data['is_paid'], data['is_deliverd'], 0, json.dumps(data['product']), data['amount'], data['tracking'], data['timestamp']))
        db.commit()
        return jsonify(result=True, message="inserted", id=cursor.lastrowid)
    elif request.method == 'GET':
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        fields = cursor.description
        orders = to_json(rows, fields)
        for order in orders:
            order = json.loads(order['product'])
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
        print(json.dumps(data['product']))
        cursor.execute("UPDATE orders SET product=? WHERE id=?", (json.dumps(data['product']), id))
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


@blueprint.route("/orders/pay/<id>/<amount>/<phone>/<name>", methods=["POST"])
def order_payment(id: int, amount: int, phone: str, name: str) -> Response:
    returnUrl = f"https://sky.respina.store/api/orders/verify/{id}/{amount}"
    headers = {
        "Authorization": "Bearer a6a01a56fb0505ee3e808f597958ba488ef93ffc2743b60c80dc55a3f348f43b",
        "Content-Type": "application/json"
    }
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(f"select * from orders where id={id}")
        rows = cursor.fetchall()
        fields = cursor.description
        order = to_json(rows, fields)
        product = base64.b64encode(json.dumps(order[0]['product']).encode('utf-8'))
        print(product)
    except OperationalError as e:
        return jsonify(result=False, message="Can not find the order", error=str(e))
    if id and amount:
        response = requests.post(url="https://api.payping.ir/v2/pay",
                                headers=headers, json={"amount": amount, "returnUrl": returnUrl, "payerIdentity": phone, "payerName": name, "description": str(product)})
        if response.status_code == 200:
            data = json.loads(response.text)
            code: str = data['code']
            if orders_set_payment_code(id=id, code=code):
                payping_url = "https://api.payping.ir/v2/pay/gotoipg/" + code
                return jsonify(result=True, url=payping_url)
            
            return jsonify(result=False, error="code is not set to database")
        return jsonify(result=False, error="something wrong happend")
    return jsonify(result=False, error="id or amount is not set...")

@blueprint.route("/orders/verify/<id>/<amount>", methods=["POST"])
def order_payment_verify(id: int, amount: int) -> Response:
    data = request.form
    if 'refid' not in data:
        return jsonify(result=False, error="refid is not in request")

    # Sending payment verify request
    headers = {
        "Authorization": "Bearer a6a01a56fb0505ee3e808f597958ba488ef93ffc2743b60c80dc55a3f348f43b",
        "Content-Type": "application/json"
    }
    response = requests.post(url="https://api.payping.ir/v2/pay/verify/", headers=headers, json={
        "refId": str(data['refid']),
        "amount": int(amount)
    })

    if response.status_code == 200:
        if orders_update_payment_status(id=id):
            return redirect(location=FRONTEND + "/verify?status=true&updated=true", code=301)
        return redirect(location=FRONTEND + "/verify?status=true&updated=false", code=500)
    return jsonify(result=False, error=json.loads(response.content))


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

def orders_set_payment_code(id: int, code: str) -> bool:
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(f"UPDATE orders SET payment_code=\"{code}\" WHERE id={id}")
        db.commit()
        return True
    except OperationalError as e:
        return False
