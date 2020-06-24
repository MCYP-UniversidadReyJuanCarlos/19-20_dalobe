import json

from flask import Flask, jsonify
from flask_cors import cross_origin

from project.resource.payload.container_resource_payload import ContainerPayload
from project.service.check_container_service import Check
from project.service.containers_service import ContainerService

app = Flask(__name__)


@app.route("/sds/health")
@cross_origin()
def health():
    return jsonify({"status": "UP"}), 200


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


if __name__ == '__main__':
    app.debug = True
    app.run()
