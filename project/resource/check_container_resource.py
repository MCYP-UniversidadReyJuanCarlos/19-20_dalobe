import os

from flask import Flask, jsonify, request, render_template
from flask_cors import cross_origin, CORS

from project.infrastracture.make_dockerfile import write_dockerfile
from project.resource.invalid_usage import InvalidUsage
from project.resource.payload.container_resource_payload import ContainerPayload
from project.service import dockerfile_service
from project.service.container_service import ContainerService
from project.service.containers_service import get_running_containers
from project.service.dockerfile_service import DockerfileService

DOCKER_FILE = "dockerfile"

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
    dockerfile_service = DockerfileService()
    dockerfile = request.get_json().get(DOCKER_FILE)
    dockerfile_path = write_dockerfile(dockerfile)
    errors = validate_dockerfile(dockerfile_path)
    if errors is not None:
        print(errors)
        raise InvalidUsage(errors)
    evaluation = dockerfile_service.check_dockerfile(dockerfile_path)
    os.remove(dockerfile_path)
    return jsonify(evaluation)


@app.route('/sds/images/dockerfile/fix', methods=['POST'])
@cross_origin()
def post_fix_dockerfile():
    dockerfile_service = DockerfileService()
    dockerfile = request.get_json().get(DOCKER_FILE)
    dockerfile_path = write_dockerfile(dockerfile)
    evaluation = dockerfile_service.check_and_fix_dockerfile(dockerfile_path)
    os.remove(dockerfile_path)
    return jsonify(evaluation)


@app.route("/")
def start():
    return render_template("index.html")

@app.route("/verify_dockerfile", methods = ['POST'])
def verify_dockerfile():
    dockerfile_service = DockerfileService()
    dockerfile = request.form['dockerfile']
    dockerfile_path = write_dockerfile(dockerfile)
    evaluation = dockerfile_service.check_and_fix_dockerfile(dockerfile_path)
    os.remove(dockerfile_path)
    return render_template("index.html", result = evaluation)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def validate_dockerfile(dockerfile_path):
    if os.path.exists(dockerfile_path) and os.path.getsize(dockerfile_path) > 0:
        return None
    return 'File does not exist or is empty'


if __name__ == '__main__':
    app.debug = True
    app.run()
