from docker import APIClient


class Check_4_1:

    def evaluate_container(container):
        inspection = APIClient().inspect_container(container.name)
        user = (inspection.get("Config").get("User"))
        if user == 'root':
            return {'evaluation': 'KO',
                    'code': 'DOCKERFILE_RUNNING_USER',
                    'description': 'Container running as root. It is a good practice to run the container as a non-root user, if possible.'}
        elif user is None or user == '':
            return {'evaluation': 'KO',
                    'code': 'DOCKERFILE_RUNNING_USER',
                    'description': 'No user found running container. It is a good practice to run the container as a non-root user, if possible.'}
        else:
            return {'evaluation': 'OK',
                    'code': 'DOCKERFILE_RUNNING_USER'}

    def evaluate_dockerfile(instructions):
        user_instruction = list(filter(lambda x: x['instruction'] == 'USER', instructions))
        if not user_instruction:
            return {'evaluation': 'KO',
                    'code': 'DOCKERFILE_RUNNING_USER',
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
                    'code': 'HEALTHCHECK_CONFIGURED',
                    'description': 'You should add the HEALTHCHECK instruction to your Docker container images in '
                                   'order to ensure that health checks are executed against running containers.'}
        else:
            return {'evaluation': 'OK',
                    'code': 'HEALTHCHECK_CONFIGURED'}

    def evaluate_dockerfile(instructions):
        user_instruction = list(filter(lambda x: x['instruction'] == 'HEALTHCHECK', instructions))
        if not user_instruction:
            return {'evaluation': 'KO',
                    'code': 'HEALTHCHECK_CONFIGURED',
                    'description': 'Dockerfile without healthcheck. It is a good practice to create a healthcheck in the Dockerfile.'}
        return {'evaluation': 'OK',
                'code': 'HEALTHCHECK_CONFIGURED'}

class Check_4_7:

    def evaluate_dockerfile(instructions):
        run_apt_get_instructions = list(filter(lambda x: x['instruction'] == 'RUN' and x['value'].startswith('apt-get'), instructions))
        if len(run_apt_get_instructions)>1:
            return {'evaluation': 'KO',
                    'code': 'APT-GET_INSTRUCTION_USAGE',
                    'description': 'Use only one apt-get instruction. Always combine RUN apt-get update with apt-get install in the same RUN statement.',
                    'line':  [o['startline'] for o in run_apt_get_instructions]}
        return {'evaluation': 'OK',
                'code': 'APT-GET_INSTRUCTION_USAGE'}


class Check_4_9:

    def evaluate_dockerfile(instructions):
        add_instructions = list(filter(lambda x: x['instruction'] == 'ADD', instructions))
        evaluation = list(filter(lambda x: not Check_4_9.is_add_proper_used(x), add_instructions))
        if evaluation:
            return {'evaluation': 'KO',
                    'code': 'ADD_INSTRUCTION_USAGE',
                    'description': 'Dockerfile with add instruction not properly used. You should use COPY rather than ADD instructions in Dockerfiles.',
                    'line':  [o['startline'] for o in evaluation]}
        return {'evaluation': 'OK',
                'code': 'ADD_INSTRUCTION_USAGE'}

    def is_add_proper_used(x):
        return x['value'].startswith('http') or '.tar' in x['value']
