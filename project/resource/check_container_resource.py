import json

from flask import Flask, jsonify

from project.resource.payload.container_resource_payload import ContainerPayload
from project.service.check_container_service import Check
from project.service.containers_service import ContainerService

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200


@app.route('/containers')
def get_containers():
    containers_payload = [ContainerPayload(v) for v in ContainerService().get_containers()]
    json_containers = [o.json() for o in containers_payload]
    return jsonify({"result": json_containers}), 200


@app.route('/containers/<id>/check')
def check_container(container_id):
    check = Check()
    return jsonify({"result": check.check_and_fix(container_id)}), 200


if __name__ == '__main__':
    app.debug = True
    app.run()
