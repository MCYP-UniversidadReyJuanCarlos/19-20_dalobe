import docker

from project.check_4 import Check_4_1


class Check:
    @staticmethod
    def check():
        client = docker.from_env()

        for container in client.containers.list():
            result = Check_4_1.evaluate_container(container)
            Check_4_1.fix_container(container)


        client.close()
        return result
