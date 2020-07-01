from flask import Flask, jsonify, request
from flask_cors import cross_origin

from project.resource.payload.container_resource_payload import ContainerPayload
from project.service.container_service import ContainerService
from project.service.containers_service import get_running_containers
from project.service.dockerfile_service import DockerfileService

app = Flask(__name__)


@app.route("/sds/health")
@cross_origin()
def get_healthcheck():
    return jsonify({"message": "Running..."}), 200


@app.route('/sds/containers')
@cross_origin()
def get_containers():
    containers_payload = [ContainerPayload(v) for v in get_running_containers()]
    json_containers = [o.json() for o in containers_payload]
    return jsonify(json_containers), 200


@app.route('/sds/containers/<container_id>/check')
@cross_origin()
def get_check_container(container_id):
    container_service = ContainerService()
    return jsonify({"result": container_service.check_container(container_id)}), 200


@app.route('/sds/containers/<container_id>/fix')
@cross_origin()
def get_check_and_fix_container(container_id):
    container_service = ContainerService()
    return jsonify({"result": container_service.check_and_fix_container(container_id)}), 200


@app.route('/sds/images/dockerfile/check', methods=['POST'])
@cross_origin()
def post_check_dockerfile():
    dockerfile_path = request.get_json().get('dockerFile')
    dockerfile_service = DockerfileService()
    return jsonify({"dockerFile": dockerfile_service.check_dockerfile(dockerfile_path)})


@app.route('/sds/images/dockerfile/fix', methods=['POST'])
@cross_origin()
def post_fix_dockerfile():
    dockerfile_path = request.get_json().get('dockerFile')
    dockerfile_service = DockerfileService()
    return jsonify({"dockerFile": dockerfile_service.check_and_fix_dockerfile(dockerfile_path)})


if __name__ == '__main__':
    app.debug = True
    app.run()
