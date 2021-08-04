import os

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from app import blueprint

from . import HOST, PATH

app = Flask(__name__)
app.register_blueprint(blueprint)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/deleteWallpaper/<path>', methods=['POST'])
def deleteWallpaper(path):
    pass


@app.route('/deleteBackground/<path>', methods=['POST'])
def deleteBackground(path):
    pass

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

@app.route("/uploadAssets", methods=['POST'])
def uploadAssets():
    if 'background' in request.files:
        bg = request.files['background']
        path = os.path.join(PATH, f"assets/backgrounds/{bg.filename}")
        try:
            bg.save(path)
            return jsonify(result=True, path=f"{HOST}/assets/backgrounds/{bg.filename}")
        except OSError as e:
            return jsonify(result=False, message=str(e))
    if 'wallpaper' in request.files:
        bg = request.files['wallpaper']
        path = os.path.join(PATH, f"assets/wallpapers/{bg.filename}")
        try:
            bg.save(path)
            return jsonify(result=True, path=f"{HOST}/assets/wallpaper/{bg.filename}")
        except OSError as e:
            return jsonify(result=False, message=str(e))
    return jsonify(result=False, message="NO DATA!")


@app.route('/backgrounds/<path>')
def getBg(path):
    if os.path.exists(os.path.join(PATH, 'backgrounds/'+path)):
        return send_file("backgrounds/"+path, as_attachment=True)
    else:
        return jsonify(result=False, message="file not found")

@app.route('/assets/get', methods=["POST"])
def assetsList():
    data = request.json
    if 'wallpapers' in data:
        files = os.listdir(os.path.join(PATH, "assets/wallpapers"))
        return jsonify(result=True, files=files, message="wallpapers")
    if 'backgrounds' in data:
        files = os.listdir(os.path.join(PATH, "assets/backgrounds"))
        return jsonify(result=True, files=files, message="backgrounds")
    return jsonify(result=False, message="specify asset type")

@app.route('/assets/get/wallpapers/<path>')
def wallpaperAssets(path):
    if os.path.exists(os.path.join(PATH, 'assets/wallpapers/'+path)):
        return send_file("assets/wallpapers/"+path, as_attachment=True)
    else:
        return jsonify(result=False, message="file not found")

@app.route('/assets/get/backgrounds/<path>')
def backgroundAssets(path):
    if os.path.exists(os.path.join(PATH, 'assets/backgrounds/'+path)):
        return send_file("assets/backgrounds/"+path, as_attachment=True)
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
