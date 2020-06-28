import json

from flask import Flask, jsonify, request
from flask_cors import cross_origin

from project.resource.payload.container_resource_payload import ContainerPayload
from project.service.container_service import Check
from project.service.containers_service import ContainerService
from project.service.dockerfile_service import DockerfileService

app = Flask(__name__)


@app.route("/sds/health")
@cross_origin()
def get_healthcheck():
    return jsonify({"message": "Running..."}), 200


@app.route('/sds/containers')
@cross_origin()
def get_containers():
    containers_payload = [ContainerPayload(v) for v in ContainerService().get_containers()]
    json_containers = [o.json() for o in containers_payload]
    return jsonify(json_containers), 200


@app.route('/sds/containers/<container_id>/check')
@cross_origin()
def get_check_container(container_id):
    check = Check()
    return jsonify({"result": check.check_and_fix(container_id)}), 200


@app.route('/sds/containers/<container_id>/fix')
@cross_origin()
def get_check_and_fix_container(container_id):
    check = Check()
    return jsonify({"result": check.check_and_fix(container_id)}), 200


@app.route('/sds/containers/<container_id>/fix')
@cross_origin()
def check_and_fix_container(container_id):
    check = Check()
    return jsonify({"result": check.check_and_fix(container_id)}), 200


@app.route('/sds/images/analyse-dockerfile', methods=['POST'])
@cross_origin()
def post_analyse_dockerfile():
    dockerfile_path = request.get_json().get('dockerFile')
    dockerfile_service = DockerfileService()
    dockerfile_service.check_dockerfile(dockerfile_path)
    return jsonify({"dockerFile": dockerfile_path})


if __name__ == '__main__':
    app.debug = True
    app.run()
