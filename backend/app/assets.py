import os

from flask import jsonify, request, send_file
from flask.wrappers import Response

from . import HOST, PATH, blueprint
from app.middleware import login_required


@blueprint.route("/assets/upload", methods=['POST'])
@login_required
def assets_upload() -> Response:
    """Upload backgrounds & wallpapers into assets folder...\n
    For example: you have to have one of the following in your `request.files`. you can do it in frontend using javascript like the code below:
    ```js
        const formData = new FormData();
        formData.append('wallpaper', imageFile)
    ```

    Returns:
        `Response`: return `result: True` if the uploading process succeed! otherwise return `result: False`
    """
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
def assets_list() -> Response:
    """Get filenames list in each directory. you should send json object like below:
    ```json
        {
            "wallpaper": true
        }
    ```

    Returns:
        `Response`: return `result: True` if the request succeed and there are all filenames into `files` property of Response JSON..otherwise return the `result: False`
    """
    data = request.json
    if 'wallpapers' in data:
        files = os.listdir(os.path.join(PATH, "assets/wallpapers"))
        return jsonify(result=True, files=files, message="wallpapers")
    if 'backgrounds' in data:
        files = os.listdir(os.path.join(PATH, "assets/backgrounds"))
        return jsonify(result=True, files=files, message="backgrounds")
    return jsonify(result=False, message="specify asset type")


@blueprint.route('/assets/get/wallpapers/<path>')
def assets_list_wallpapers(path: str) -> Response:
    """list of all wallpapers inside assets folder

    Args:
        `path (str)`: filename of the asset

    Returns:
        `Response`: reutn actual file if the file exists in the `assets/wallpapers` directory
    """
    if os.path.exists(os.path.join(PATH, 'assets/wallpapers/'+path)):
        return send_file("assets/wallpapers/"+path, as_attachment=True)
    else:
        return jsonify(result=False, message="file not found")


@blueprint.route('/assets/get/backgrounds/<path>')
def assets_list_backgrounds(path: str) -> Response:
    """list of all backgrounds inside assets folder

    Args:
        `path (str)`: filename of the asset

    Returns:
        `Response`: reutn actual file if the file exists in the `assets/backgrounds` directory
    """
    if os.path.exists(os.path.join(PATH, 'assets/backgrounds/'+path)):
        return send_file("assets/backgrounds/"+path, as_attachment=True)
    else:
        return jsonify(result=False, message="file not found")


@blueprint.route('/assets/delete/<path>', methods=['POST'])
@login_required
def assets_del_wallpaper(path: str) -> Response:
    pass


@blueprint.route('/assets/delete/<path>', methods=['POST'])
@login_required
def assets_del_background(path: str) -> Response:
    pass
