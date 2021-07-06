import os

from flask import Flask, jsonify, request

app = Flask(__name__)

PATH = os.getcwd()


@app.route("/starmap", methods=['POST'])
def starmap():
    content = request.json

    coord = content["coord"]
    time = content["time"]
    date = content["date"]
    city = content["city"]
    filename = content["name"] + ".svg"

    os.system(
        f"python starmap.py -coord {coord} -time {time} -date {date} -utc +3 -guides False -constellation True -o {'images/'+ filename} -info {city}")
    return jsonify(result=True, message=f"Created")


@app.route("/")
def index():
    return "Index"


if __name__ == '__main__':
    app.run(debug=True)
