import os
import sqlite3
from bcrypt import checkpw, kdf, gensalt, hashpw
from sqlite3.dbapi2 import Error, OperationalError
from PIL import ImageColor
from datetime import datetime
import bcrypt
from flask import Flask, json, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

HOST = "http://localhost:5000"
PATH = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(PATH, 'db.sqlite3')

ORDERS_TBL = """CREATE TABLE IF NOT EXISTS orders (
id integer PRIMARY KEY,
name text NOT NULL,
mobile text NOT NULL,
address text NOT NULL,
province text NOT NULL,
city text NOT NULL,
post text NOT NULL,
is_paid integer NOT NULL,
is_deliverd integer NOT NULL,
product text NOT NULL,
amount text NOT NULL,
tracking text NOT NULL
);
"""

USERS_TBL = """CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY,
name text NOT NULL,
username text NOT NULL UNIQUE,
password text NOT NULL
);
"""


def get_db():
    db = getattr(app, '_database', None)
    if db is None:
        db = app._database = sqlite3.connect(DATABASE)
        try:
            c = db.cursor()
            c.execute(ORDERS_TBL)
            c.execute(USERS_TBL)
        except Error as e:
            print(e)
    return db


def config_creator(data):
    conf = "python starmap/starmap.py"
    # Geo Location data
    if 'geo' in data:
        if 'location' in data['geo']:
            lat = data['geo']['location']['lat']
            lng = data['geo']['location']['lng']
            conf += f" -coord {lat},{lng}"

        if 'date' in data['geo']:
            conf += f" -date {data['geo']['date']}"

        if 'time' in data['geo']:
            conf += f" -time {data['geo']['time']}"

    if 'background' in data:
        if 'bg' in data['background']:
            conf += f" -bg \"{data['background']['bg']}\""
        if 'x' in data['background']:
            conf += f" -bgPosX \"{data['background']['x']}\""
        if 'y' in data['background']:
            conf += f" -bgPosY \"{data['background']['y']}\""
        if 'opacity' in data['background']:
            conf += f" -bgOpacity {data['background']['opacity']}"
        if 'wallpaper' in data['background']:
            conf += f" -wallpaper \"{data['background']['wallpaper']}\""

    if 'text' in data:
        if 'line1' in data['text'] and isinstance(data['text']['line1']['value'], str):
            conf += f" -line1 \"{data['text']['line1']['value']}\""
            conf += f" -fontFamily1 \"{data['text']['line1']['font']}\""
            conf += f" -fontSize1 {data['text']['line1']['size']}"
            conf += f" -fontColor1 \"{data['text']['line1']['color']}\""

        if 'line2' in data['text'] and isinstance(data['text']['line2']['value'], str):
            conf += f" -line2 \"{data['text']['line2']['value']}\""
            conf += f" -fontFamily2 \"{data['text']['line2']['font']}\""
            conf += f" -fontSize2 {data['text']['line2']['size']}"
            conf += f" -fontColor2 \"{data['text']['line2']['color']}\""

        if 'line3' in data['text'] and isinstance(data['text']['line3']['value'], str):
            conf += f" -line3 \"{data['text']['line3']['value']}\""
            conf += f" -fontFamily3 \"{data['text']['line3']['font']}\""
            conf += f" -fontSize3 {data['text']['line3']['size']}"
            conf += f" -fontColor3 \"{data['text']['line3']['color']}\""

    if 'music' in data:
        conf += f" -qrCode \"{data['music']['qr']}\""

    # Customize Options
    if 'customize' in data:
        if data['customize']['frame']:
            # Hex to RGB colors
            frameColor = "".join(
                str(ImageColor.getrgb(data['customize']['frame'])))
            frameColor = frameColor.strip().replace(
                "(", "").replace(")", "").replace(" ", "")
        if data['customize']['background']:
            # Hex to RGB colors
            backgroundColor = "".join(str(ImageColor.getrgb(
                data['customize']['background'])))
            backgroundColor = backgroundColor.strip().replace(
                "(", "").replace(")", "").replace(" ", "")
            conf += f" -background {backgroundColor}"
        if data['customize']['constellation']:
            conf += f" -constellation {data['customize']['constellation']}"
        if data['customize']['constellationText']:
            conf += f" -constellationText {data['customize']['constellationText']}"
        if data['customize']['dot']:
            conf += f" -showDot {data['customize']['dot']}"
        if data['customize']['star']:
            conf += f" -showStar {data['customize']['star']}"
    # Filename
    if 'filename' in data:
        conf += f" -o app/images/{ data['filename'] }"

    # Shape
    if 'shape' in data:
        conf += f" -heart {data['shape']}"

    return conf


@app.route("/starmap", methods=['POST'])
def starmap():
    content = request.json

    if 'paint' in content:
        try:
            os.system(config_creator(content))
            if os.path.exists(os.path.join(PATH, "images/"+content['filename'])):
                return jsonify(result=True, message="file created!", path=f"{HOST}/download/{content['filename']}")
            else:
                return jsonify(result=False, message="file creation error...", path=os.getcwd())
        except Exception as e:
            return jsonify(result=False, message="something wrong happend here...", error=str(e))
    else:
        return jsonify(result=True, message="i did not paint anything")


@app.route('/uploadBackground', methods=['POST'])
def uploadBg():
    if 'bg' not in request.files:
        return jsonify(result=False, message="There's no file in request...")
    bg = request.files['bg']
    path = os.path.join(PATH, f"backgrounds/{bg.filename}")
    try:
        bg.save(path)
        return jsonify(result=True, path=f"{HOST}/backgrounds/{bg.filename}")
    except OSError as e:
        return jsonify(result=False, message=str(e))


@app.route('/backgrounds/<path>')
def getBg(path):
    if os.path.exists(os.path.join(PATH, 'backgrounds/'+path)):
        return send_file("backgrounds/"+path, as_attachment=True)
    else:
        return jsonify(result=False, message="file not found")


@app.route('/download/<path>')
def downloadFile(path):
    if os.path.exists(os.path.join(PATH, "images/"+path)):
        return send_file("images/" + path, as_attachment=True)
    else:
        return jsonify(result=False, message="file not found")


@app.route('/fonts')
def fontsList():
    return jsonify(result=True, fonts=['Anton', 'Dancing Script', 'Fuggles', 'Karla', 'Qahiri', 'Roboto', 'Roboto', 'Robot Salb', 'Kamran', 'Mikhak', 'Yekan'])


@app.route("/")
def index():
    return "Index"

# Orders
@app.route("/orders", methods=['GET', 'POST'])
def orders():
    db = get_db()
    c = db.cursor()
    if request.method == 'POST':
        data = request.json
        product = data['product']
        c.execute(
            f"INSERT INTO orders (name, mobile, address, province, city, post, is_paid, is_deliverd, product, amount, tracking) VALUES (\"{data['name']}\", \"{data['mobile']}\", \"{data['address']}\", \"{data['province']}\", \"{data['city']}\", \"{data['post']}\", \"{data['is_paid']}\", \"{data['is_deliverd']}\", \"{product}\", \"{data['amount']}\", \"{data['tracking']}\")")
        db.commit()
        return jsonify(result=True, message="inserted", id=c.lastrowid)
    elif request.method == 'GET':
        c.execute("SELECT * FROM orders")
        rows = c.fetchall()
        for item in range(len(rows)):
            rows[item] = {"id": rows[item][0], "name": rows[item]
                          [1], "mobile": rows[item][2], "address": rows[item][3], "province": rows[item][4], "city": rows[item][5], "post": rows[item][6], "is_paid": rows[item][7], "is_deliverd": rows[item][8], "product": rows[item][9], "amount": rows[item][10], "tracking": rows[item][11]}

        return jsonify(result=True, data=rows)
@app.route("/orders/<id>", methods=["DELETE"])
def delete_orders(id):
    db = get_db()
    c = db.cursor()
    c.execute(f"SELECT * FROM orders where id={id}")
    rows = c.fetchall()
    if len(rows) > 0:
        c.execute(f"DELETE FROM orders where id={id}")
        db.commit()
        return jsonify(result=True, message="successfully deleted")
    else:
        return jsonify(result=False, message="there is no order with that id")
@app.route("/orders/<id>", methods=["PUT"])
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


# Auth
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data['username']
    password = data['password'].encode("utf-8")
    db = get_db()
    c = db.cursor()
    try:
        c.execute(f'SELECT * FROM users WHERE username="{username}"')
        row = c.fetchone()
        if row & checkpw(password, row[3].encode('utf-8')):
            return jsonify(result=True, message="logged in successfully")
        else:
            return jsonify(result=False, message="نام کاربری یا رمز عبور صحیح نیست...")
    except OperationalError as e:
        return jsonify(result=False, message="شما در رسپینا اکانت ندارید :(")


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data['name']
    username = data['username']
    password = data['password'].encode('utf-8')

    db = get_db()
    c = db.cursor()
    try:
        hashed = hashpw(password, gensalt(10))
        c.execute(
            f"INSERT INTO users (name, username, password) VALUES (\"{name}\", \"{username}\", \"{hashed}\")")
        db.commit()
        return jsonify(result=True, message="Succefully signed up")
    except OperationalError as e:
        return jsonify(result=False, message="خطایی عجیبی پیش اومده! لطفا بعدا تلاش کنید...", error=str(e))


@app.route("/test", methods=['POST', 'GET'])
def test():
    return jsonify(data=config_creator(request.json))
