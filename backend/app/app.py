import os
from PIL import ImageColor
from datetime import datetime
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

HOST = "http://localhost:5000"
PATH = os.path.dirname(os.path.abspath(__file__))


def config_creator(data):
    conf = "python starmap/starmap.py"
    # Geo Location data
    if 'geo' in data:
        if 'location' in data['geo']:
            lat = data['geo']['location']['lat']
            lng = data['geo']['location']['lng']
            conf += f" -coord {lat},{lng}"

        if 'date' in data['geo']:
            date = datetime.utcfromtimestamp(
                int(data['geo']['date'])).strftime('%d.%m.%Y')
            conf += f" -date {date}"

        if 'time' in data['geo']:
            conf += f" -time {data['geo']['time']}"

    if 'text' in data:
        if 'line1' in data['text'] and isinstance(data['text']['line1']['value'], str):
            conf += f" -line1 \"{data['text']['line1']['value']}\""
            conf += f" -fontFamily1 \"{data['text']['line1']['font']}\""
            conf += f" -fontSize1 {data['text']['line1']['size']}"

        if 'line2' in data['text'] and isinstance(data['text']['line2']['value'], str):
            conf += f" -line2 \"{data['text']['line2']['value']}\""
            conf += f" -fontFamily2 \"{data['text']['line2']['font']}\""
            conf += f" -fontSize2 {data['text']['line2']['size']}"
        if 'line3' in data['text'] and isinstance(data['text']['line3']['value'], str):
            conf += f" -line3 \"{data['text']['line3']['value']}\""
            conf += f" -fontFamily3 \"{data['text']['line3']['font']}\""
            conf += f" -fontSize3 {data['text']['line3']['size']}"

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


@app.route('/download/<path>')
def downloadFile(path):
    if os.path.exists(os.path.join(PATH, "images/"+path)):
        return send_file("images/" + path, as_attachment=True)
    else:
        return jsonify(result=False, message="file not found")


@app.route("/")
def index():
    return "Index"


@app.route("/test", methods=['POST', 'GET'])
def test():
    return jsonify(data=config_creator(request.json))
