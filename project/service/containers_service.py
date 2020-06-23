import docker


class ContainerService:

    def get_containers(self):
        client = docker.from_env()
        containers_list = client.containers.list()
        client.close()
        return containers_list

