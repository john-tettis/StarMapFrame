import os

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from . import HOST, PATH, blueprint, FONTS

app = Flask(__name__)
app.register_blueprint(blueprint)

app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/uploadBackground', methods=['POST'])
def upload_user_background():
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
def get_user_backgrounds(path):
    if os.path.exists(os.path.join(PATH, 'backgrounds/'+path)):
        return send_file("backgrounds/"+path, as_attachment=True)
    else:
        return jsonify(result=False, message="file not found")


@app.route('/fonts')
def fonts_list():
    return jsonify(result=True, fonts=FONTS)


@app.route("/")
def index():
    return "Index"
