
from sqlite3.dbapi2 import OperationalError

from flask import jsonify, request

from . import get_db

from . import blueprint


@blueprint.route("/orders", methods=['GET', 'POST'])
def orders():
    db = get_db()
    c = db.cursor()
    if request.method == 'POST':
        data = request.json
        c.execute(
            "INSERT INTO orders (name, mobile, address, province, city, post, is_paid, is_deliverd, is_printed, product, amount, tracking, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (data['name'], data['mobile'], data['address'], data['province'], data['city'], data['post'], data['is_paid'], data['is_deliverd'], 0, str(data['product']), data['amount'], data['tracking'], data['timestamp']))
        db.commit()
        return jsonify(result=True, message="inserted", id=c.lastrowid)
    elif request.method == 'GET':
        c.execute("SELECT * FROM orders")
        rows = c.fetchall()
        for item in range(len(rows)):
            rows[item] = {"id": rows[item][0], "name": rows[item]
                          [1], "mobile": rows[item][2], "address": rows[item][3], "province": rows[item][4], "city": rows[item][5], "post": rows[item][6], "is_paid": rows[item][7], "is_deliverd": rows[item][8], "is_printed": rows[item][9], "product": rows[item][10], "amount": rows[item][11], "tracking": rows[item][12], "timestamp": rows[item][13]}

        return jsonify(result=True, data=rows)


@blueprint.route("/orders/<id>", methods=["DELETE"])
def delete_orders(id):
    cookies = request.cookies
    if 'token' in cookies:
        db = get_db()
        c = db.cursor()
        c.execute(f"SELECT * FROM tokens where token=\"{cookies['token']}\"")
        tokens = c.fetchall()
        if len(tokens) > 0:
            c.execute(f"SELECT * FROM orders where id={id}")
            rows = c.fetchall()
            if len(rows) > 0:
                c.execute(f"DELETE FROM orders where id={id}")
                db.commit()
                return jsonify(result=True, message="successfully deleted")
            else:
                return jsonify(result=False, message="there is no order with that id")
        else:
            return jsonify(result=False, message="You are not authenticated")
    else:
        return jsonify(result=False, message="You are not authenticated")


@blueprint.route("/orders/<id>", methods=["PUT"])
def update_orders(id):
    data = request.json
    db = get_db()
    c = db.cursor()
    if 'updatePaymentStatus' in data:
        try:
            c.execute(f"SELECT * from orders WHERE id={id}")
            row = c.fetchone()
            if row:
                c.execute(f"UPDATE orders SET is_paid=1 WHERE id={id}")
                db.commit()
                return jsonify(result=True, message="updated!")
            else:
                return jsonify(result=False, message="there is no order")
        except OperationalError as e:
            return jsonify(result=False, message="update status failed")
    else:
        return jsonify(result=False)


@blueprint.route("/orders/edit/<id>", methods=["POST"])
def edit_order(id):
    data = request.json
    db = get_db()
    c = db.cursor()
    try:
        c.execute(
            f"UPDATE orders SET product=\"{data['product']}\" WHERE id={id}")
        db.commit()
        return jsonify(result=True, message="OK!")
    except OperationalError as e:
        return jsonify(result=False, message="NOT OK!", error=str(e))


@blueprint.route("/orders/setPrinted/<id>", methods=["POST"])
def print_status(id):
    db = get_db()
    c = db.cursor()
    data = request.json
    try:
        c.execute(
            f"UPDATE orders SET is_printed={data['status']} WHERE id={id}")
        db.commit()
        return jsonify(result=True, message="OK!")
    except OperationalError as e:
        return jsonify(result=False, message="NOT OK!", error=str(e))
