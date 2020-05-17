import docker

from project.check_4 import Check_4_1, Check_4_6
from project.fix_4 import Fix_4_1, Fix_4_6


class Check:

    def check_and_fix(self, container_id):
        container = self.get_container(container_id)
        if not container:
            return 'Error: no container found'
        check_result = self.check_container(container[0])
        fixes = self.fix_container(container[0],check_result)

        return check_result

    def get_container(self, container_id):
        client = docker.from_env()
        containers = client.containers.list()
        container = list(filter(lambda x: x.id == container_id, containers))
        # container = [i for i in containers if container_id == i.id]
        client.close()
        return container

    def check_container(self, container):
        return {'4_1': Check_4_1.evaluate_container(container),
                '4_6': Check_4_6.evaluate_container(container)}

    def fix_container(self, container, check_result):
        check_4_1 = check_result.get('4_1')
        if check_4_1.get('evaluation') == 'KO':
            str = Fix_4_1.fix_container(container)
        check_4_6 = check_result.get('4_6')
        if check_4_6.get('evaluation') == 'KO':
            str = str + Fix_4_6.fix_container(container)
        return str

