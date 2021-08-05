import os

from flask import jsonify, request, send_file

from . import HOST, PATH, blueprint


@blueprint.route("/assets/upload", methods=['POST'])
def assets_upload():
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


@blueprint.route('/assets/get', methods=["POST"])
def assets_list():
    data = request.json
    if 'wallpapers' in data:
        files = os.listdir(os.path.join(PATH, "assets/wallpapers"))
        return jsonify(result=True, files=files, message="wallpapers")
    if 'backgrounds' in data:
        files = os.listdir(os.path.join(PATH, "assets/backgrounds"))
        return jsonify(result=True, files=files, message="backgrounds")
    return jsonify(result=False, message="specify asset type")

@blueprint.route('/assets/get/wallpapers/<path>')
def assets_list_wallpapers(path):
    if os.path.exists(os.path.join(PATH, 'assets/wallpapers/'+path)):
        return send_file("assets/wallpapers/"+path, as_attachment=True)
    else:
        return jsonify(result=False, message="file not found")

@blueprint.route('/assets/get/backgrounds/<path>')
def assets_list_backgrounds(path):
    if os.path.exists(os.path.join(PATH, 'assets/backgrounds/'+path)):
        return send_file("assets/backgrounds/"+path, as_attachment=True)
    else:
        return jsonify(result=False, message="file not found")


@blueprint.route('/assets/delete/<path>', methods=['POST'])
def assets_del_wallpaper(path):
    pass


@blueprint.route('/assets/delete/<path>', methods=['POST'])
def assets_del_background(path):
    pass
