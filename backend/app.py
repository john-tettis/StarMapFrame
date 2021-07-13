import os
from PIL import ImageColor
from datetime import datetime
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*": {"origins": "*"}})


def config_creator(data):
    conf = "python starmap/starmap.py"
    # Geo Location data
    if data['geo']:
        if data['geo']['location']:
            lat = data['geo']['location']['lat']
            lng = data['geo']['location']['lng']
            conf += f" -coord {lat},{lng}"

        if data['geo']['date']:
            date = datetime.utcfromtimestamp(
                int(data['geo']['date'])).strftime('%d.%m.%Y')
            conf += f" -date {date}"

        if data['geo']['time']:
            conf += f" -time {data['geo']['time']}"

    # Customize Options
    if data['customize']:
        if data['customize']['frame']:
            # Hex to RGB colors
            frameColor = ImageColor.getrgb(data['customize']['frame'])
            frameColor = frameColor.strip().replace(
                "(", "").replace(")", "").replace(" ", "")
        if data['customize']['background']:
            # Hex to RGB colors
            backgroundColor = ImageColor.getrgb(
                data['customize']['background'])
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
    if data['filename']:
        conf += f" -o images/{ data['filename'] }"

    return conf


@app.route("/starmap", methods=['POST'])
def starmap():
    content = request.json

    if content["paint"]:
        try:
            os.system(config_creator(content))
            return jsonify(result=True, message="file created!", path=f"http://localhost:5000/download/{content['filename']}")
        except:
            return jsonify(result=False, message="something wrong happend here...")
    else:
        return jsonify(result=True, message="i did not paint anything")


@app.route('/download/<path>')
def downloadFile(path):
    if os.path.exists("images/"+path):
        return send_file("images/" + path, as_attachment=True)
    else:
        return jsonify(result=False, message="file not found")


@app.route("/")
def index():
    return "Index"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
