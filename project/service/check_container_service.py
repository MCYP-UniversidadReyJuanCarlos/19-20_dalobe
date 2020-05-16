import docker

from project.check_4 import Check_4_1
from project.fix_4 import Fix_4_1


class Check:

    def check_and_fix(self, container_id):
        client = docker.from_env()
        containers = client.containers.list()
        container = [i for i in containers if container_id == i.id]
        if not container:
            return 'Error: no container found'
        result = {'4_1': Check_4_1.evaluate_container(container[0])}
        Fix_4_1.fix_container(container[0], result)
        client.close()
        return result
