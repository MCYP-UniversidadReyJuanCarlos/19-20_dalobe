import docker

from project.check_4 import Check_4_1


class Check:

    def check(self, container):
        client = docker.from_env()
        containers = client.containers.list()
        result = 'KO'
        l = [i for i in containers if container == i.id]
        if l:
            result = Check_4_1.evaluate_container(l[0])
            Check_4_1.fix_container(l[0])

        client.close()
        return result
