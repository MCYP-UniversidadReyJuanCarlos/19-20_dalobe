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

    def evaluate_dockerfile(instructions):
        user_instruction = list(filter(lambda x: x['instruction'] == 'USER', instructions))
        if not user_instruction:
            return {'evaluation': 'KO',
                    'code': 'DOCKERFILE_WITHOUT_USER',
                    'description': 'It is a good practice to create a user for each container image different from '
                                   'default (root).'
                    }
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

    def evaluate_dockerfile(instructions):
        user_instruction = list(filter(lambda x: x['instruction'] == 'HEALTHCHECK', instructions))
        if not user_instruction:
            return {'evaluation': 'KO',
                    'code': 'DOCKERFILE_WITHOUT_HEALTHCHECK',
                    'description': 'It is a good practice to create a healthcheck in the Dockerfile.'}
        return {'evaluation': 'OK'}


class Check_4_9:

    def evaluate_dockerfile(instructions):
        add_instructions = list(filter(lambda x: x['instruction'] == 'ADD', instructions))
        evaluation = list(filter(lambda x: not Check_4_9.is_add_proper_used(x), add_instructions))
        if evaluation:
            return {'evaluation': 'KO',
                    'code': 'DOCKERFILE_WITH_ADD_INSTRUCTION_NOT_PROPER_USED',
                    'description': 'You should use COPY rather than ADD instructions in Dockerfiles.',
                    'line':  [o['startline'] for o in evaluation]}
        return {'evaluation': 'OK'}

    def is_add_proper_used(x):
        return x['value'].startswith('http') or '.tar' in x['value']
