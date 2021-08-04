import os

from flask import jsonify, request
from PIL import ImageColor

from app import HOST, PATH

from . import blueprint


def CONFIG(data):
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

    return conf


@blueprint.route("/starmap", methods=['POST'])
def starmap():
    content = request.json

    if 'paint' in content:
        try:
            os.system(CONFIG(content))
            if os.path.exists(os.path.join(PATH, "images/"+content['filename'])):
                return jsonify(result=True, message="file created!", path=f"{HOST}/download/{content['filename']}")
            else:
                return jsonify(result=False, message="file creation error...", path=os.getcwd())
        except Exception as e:
            return jsonify(result=False, message="something wrong happend here...", error=str(e))
    else:
        return jsonify(result=True, message="i did not paint anything")
