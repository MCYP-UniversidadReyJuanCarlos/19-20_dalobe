import json

from flask import Flask, jsonify
from flask_cors import cross_origin

from project.resource.payload.container_resource_payload import ContainerPayload
from project.service.check_container_service import Check
from project.service.containers_service import ContainerService

app = Flask(__name__)


<<<<<<< HEAD
@app.route("/sds/health")
@cross_origin()
=======
@app.route('/')
def hello_world():
    return send_response()


@app.route('/containers/<id>/check')
def check(id):
    check = Check()
    return jsonify({"evaluation": check.check_and_fix(id)}), 200


@app.route("/health")
>>>>>>> Add healt check evalation rule
def health():
    return jsonify({"message": "Running..."}), 200


<<<<<<< HEAD
@app.route('/sds/containers')
@cross_origin()
def get_containers():
    containers_payload = [ContainerPayload(v) for v in ContainerService().get_containers()]
    json_containers = [o.json() for o in containers_payload]
    return jsonify(json_containers), 200


@app.route('/sds/containers/<id>/check')
@cross_origin()
def check_container(container_id):
    check = Check()
    return jsonify({"result": check.check_and_fix(container_id)}), 200
=======
def send_response():
    return jsonify({"message": "Running..."}), 200
>>>>>>> Add healt check evalation rule


if __name__ == '__main__':
    app.debug = True
    app.run()
