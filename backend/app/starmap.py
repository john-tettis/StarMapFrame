import os

from flask import jsonify, request, send_file
from flask.wrappers import Response
from PIL import ImageColor

from app import HOST, PATH

from . import blueprint
from shutil import which
from random import randint
import subprocess


def CONFIG(data: list) -> str:
    """Create a config string for starmap module to run in the terminal

    Args:
        `data (request.json)`: it should be `JSON` array with the following keys:\n `['geo', 'background', 'text', 'music', 'customize', 'filename', 'shape', 'mode']`

    Returns:
        `conf (str)`: full configuration string to run on the starmap module using `os.system()`
    """
    conf = "python starmap/starmap.py"
    # Geo Location data
    if 'geo' in data:
        if 'location' in data['geo']:
            lat = data['geo']['location']['lat']
            lng = data['geo']['location']['lng']
            conf += f" -coord \"{lat},{lng}\""
        if 'province' in data['geo']:
            conf += f" -province \"{data['geo']['province']}\""
        if 'city' in data['geo']:
            conf += f" -city \"{data['geo']['city']}\""

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
        if 'circle' in data['background']:
            conf += f" -setCircle \"{data['background']['circle']}\""

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

        if 'wallpaper' in data['customize']:
            conf += f" -wallpaper \"{data['customize']['wallpaper']}\""
    # Filename
    if 'filename' in data:
        conf += f" -o app/images/{ data['filename'] }"

    # Shape
    if 'shape' in data:
        conf += f" -heart {data['shape']}"

    # MODE
    if 'MODE' in data:
        conf += f" -MODE PROD"
    else:
        conf += f" -MODE DEV"

    if 'tracking' in data:
        if data['customize']['frame'] == "#000000":
            conf += f" -tracking \"{data['tracking']}.B\""
        else:
            conf += f" -tracking \"{data['tracking']}.W\""
        if 'roban' in data and data['roban']:
            conf += ".R"
        if 'size' in data['customize']:
            conf += f" -size \"{data['customize']['size']}\""
    else:
        conf += " -tracking \"\""

    return conf
def random_file_name(tracking):
    return tracking + '-' + str(randint(10000, 999999)) + "-export.png"

def do_export_to_png(image: str, tracking: str) -> str:
    image_path = os.path.join(PATH, "images/" + image)
    file_name = random_file_name(tracking)
    file_name_path = os.path.join(PATH, "images/"+file_name)
    os.system(f"svgexport {image_path} {file_name_path} 4x 100%")
    return jsonify(result=True, message="file created!", path=f"{HOST}/download/{file_name}")
    

@blueprint.route("/starmap", methods=['POST'])
def starmap() -> Response:
    """Genrate starmap using `starmap` module. it gets configuration from `CONFIG()` and then it saves the \n
    genrated starmap into `images` folder...

    Returns:
        `Response`: return result True if the file creation is succesfull otherwise it raise an exception
    """
    content = request.json
    if 'paint' in content and content['paint']:
        try:
            os.system(CONFIG(content))
            if os.path.exists(os.path.join(PATH, "images/"+content['filename'])):
                return jsonify(result=True, message="file created!", path=f"{HOST}/download/{content['filename']}")
            else:
                return jsonify(result=False, message="file creation error...", path=os.getcwd())
        except Exception as e:
            return jsonify(result=False, message="something wrong happend here...", error=str(e))
    else:
        if which("svgexport") is not None:
            try:
                os.system(CONFIG(content))
                if os.path.isfile(os.path.join(PATH, "images/" + content['filename'])):
                    return do_export_to_png(content['filename'], content['tracking'])
                else:
                    return jsonify(result=False, message="file creation error...", path=os.getcwd())
            except Exception as e:
                return jsonify(result=False, message="something wrong happend here...", error=str(e))
        else:
            return jsonify(result=False, message="svgexport is not installed...")


@blueprint.route('/starmap/assets/<path>')
def starmap_download_assets(path: str) -> Response:
    """
    starmap module require some images to render correctly. This function make it possible to get static assets it needed...

    Args:
        `path (string)`: filename of the image

    Returns:
        `Response`: returns the actual file if it's available otherwise return a json object with result of `False`
    """
    if os.path.exists(os.path.join(PATH, "assets/"+path)):
        return send_file("assets/" + path, as_attachment=True)
    else:
        return jsonify(result=False, message="file not found")


@blueprint.route('/download/<path>')
def starmap_download_file(path: str) -> Response:
    """download the genrated svg of starmap

    Args:
        `path (str)`: the filename of genrated starmap

    Returns:
        `Response`: returns the actual file if it's available otherwise return a json object with result of `False`
    """
    if os.path.exists(os.path.join(PATH, "images/"+path)):
        return send_file("images/" + path, as_attachment=True)
    else:
        return jsonify(result=False, message="file not found")
