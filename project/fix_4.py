import shutil


class Fix_4_1:

    def fix_container(container):
        return 'RUN useradd -d /home/username -m -s /bin/bash username \nUSER username \n\n'

    def fix_dockerfile(self):
        # 'RUN useradd -d /home/username -m -s /bin/bash username \nUSER username \n\n'
        return [{
            'instruction': 'RUN',
            'content': 'RUN useradd -d /home/username -m -s /bin/bash username \n',
            'value': 'useradd -d /home/username -m -s /bin/bash username \n'
        },
            {
                'instruction': 'RUN',
                'content': 'RUN useradd -d /home/username -m -s /bin/bash username \n',
                'value': 'useradd -d /home/username -m -s /bin/bash username \n'
            }]


class Fix_4_6:

    def fix_container(container):
        shutil.copyfile('../../templates/docker-healthcheck', '../../output/docker-healthcheck')
        return 'COPY docker-healthcheck /usr/local/bin/ \nHEALTHCHECK CMD ["docker-healthcheck"]\n'

    def fix_dockerfile(self):
        return [{
            'instruction': 'COPY',
            'content': 'COPY docker-healthcheck /usr/local/bin/ \n',
            'value': 'docker-healthcheck /usr/local/bin/ \n'
        },
        {
            'instruction': 'HEALTHCHECK',
            'content': 'HEALTHCHECK CMD ["docker-healthcheck"]\n',
            'value': 'CMD ["docker-healthcheck"]\n'
        }]
