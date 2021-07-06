import os
from datetime import datetime
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

PATH = os.getcwd()


@app.route("/starmap", methods=['POST'])
def starmap():
    content = request.json

    # Format Coord
    coord = content["coord"]
    # Format Time
    time = content["time"]
    time = time.split(":")
    if len(time) == 2:
        time.append("00")
    time = ".".join(time)
    # Format Date
    date = content["date"]
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    date = date_obj.strftime("%d.%m.%Y")
    # Format City
    city = content["city"]
    # Format Filename
    filename = content["name"] + ".svg"
    # Format Info
    info = content["info"]

    os.system(
        f"python starmap.py -coord {coord} -time {time} -date {date} -utc +3 -constellation True -o {'images/'+ filename} -info {city}")

    response = jsonify(result=True, message="Starmap created successfully",
                       path=f"http://{request.host}/download/{filename}")
    return response


@app.route('/download/<path>')
def downloadFile(path):
    return send_file("images/" + path, as_attachment=True)


@app.route("/")
def index():
    return "Index"


if __name__ == '__main__':
    app.run(debug=True)
