from docker import APIClient


class Check_4_1:

    def evaluate_container(container):
        inspection = APIClient().inspect_container(container.name)
        user = (inspection.get("Config").get("User"))
        if user == 'root':
            return {'evaluation': 'KO',
                    'code': 'CONTAINER_RUNNING_AS_ROOT',
                    'description': 'It is a good practice to run the container as a non-root user, if possible.'}
        elif user is None or user == '':
            return {'evaluation': 'KO',
                    'code': 'NO_USER_FOUND_RUNNING_CONTAINER',
                    'description': 'It is a good practice to run the container as a non-root user, if possible.'}
        else:
            return {'evaluation': 'OK'}


class Check_4_6:

    def evaluate_container(container):
        inspection = APIClient().inspect_container(container.name)
        healthcheck = (inspection.get("Config").get("Healthcheck"))
        if healthcheck is None or healthcheck == '':
            return {'evaluation': 'KO',
                    'code': 'NO_HEALTHCHECK_CONFIGURED',
                    'description': 'You should add the HEALTHCHECK instruction to your Docker container images in '
                                   'order to ensure that health checks are executed against running containers.'}
        else:
            return {'evaluation': 'OK'}
