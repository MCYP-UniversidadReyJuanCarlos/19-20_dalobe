import docker

from project.check_4 import Check_4_1, Check_4_6
from project.infrastracture.make_docker_file import Make_docker_file
from project.service.dockerfile_service import DockerfileService


class ContainerService:

    def check_container(self, container_id):
        container = self.get_container(container_id)
        if not container:
            return 'Error: no container found'
        check_result = self.evaluate_container(container[0])
        return check_result

    def check_and_fix_container(self, container_id):
        container = self.get_container(container_id)
        if not container:
            return 'Error: no container found'
        check_result = self.evaluate_container(container[0])
        fixes = DockerfileService.get_dockerfile_fixes(self, check_result)
        Make_docker_file.write_docker_file_from_dynamic(container[0], fixes)
        return check_result

    def get_container(self, container_id):
        client = docker.from_env()
        containers = client.containers.list()
        container = list(filter(lambda x: x.id == container_id, containers))
        # container = [i for i in containers if container_id == i.id]
        client.close()
        return container

    def evaluate_container(self, container):
        return [{'4_1': Check_4_1.evaluate_container(container),
                '4_6': Check_4_6.evaluate_container(container)}]
