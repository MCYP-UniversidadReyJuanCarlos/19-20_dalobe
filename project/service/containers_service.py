import docker


def get_running_containers():
    client = docker.from_env()
    # List containers. Similar to the ``docker ps`` command.
    containers_list = client.containers.list()
    client.close()
    return containers_list

