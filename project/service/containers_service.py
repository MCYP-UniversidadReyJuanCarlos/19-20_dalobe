import docker


class ContainerService:

    def get_containers(self):
        client = docker.from_env()
        # List containers. Similar to the ``docker ps`` command.
        containers_list = client.containers.list()
        client.close()
        return containers_list
