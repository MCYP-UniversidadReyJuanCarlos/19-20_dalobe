from flask import Flask, jsonify

from project.check_container import Check

app = Flask(__name__)


@app.route('/')
def hello_world():
    return send_response()


@app.route('/check')
def check():
    check = Check()
    return jsonify({"result": check.check()}), 200


@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200


def send_response():
    return jsonify({"message": "Hello World"}), 200


if __name__ == '__main__':
    app.debug = True
    app.run()
