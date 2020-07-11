import shutil


class Fix_4_1:

    def fix_dockerfile(self):
        # 'RUN useradd -d /home/username -m -s /bin/bash username \nUSER username \n\n'
        return [{
            'instruction': 'RUN',
            'content': '\nRUN useradd -d /home/username -m -s /bin/bash username \n',
            'value': 'useradd -d /home/username -m -s /bin/bash username \n'
        },{
            'instruction': 'USER',
            'content': 'RUN username \n',
            'value': 'username \n'
        }]


class Fix_4_6:

    def fix_dockerfile(self):
        shutil.copyfile('templates/docker-healthcheck', 'output/docker-healthcheck')
        return [{
            'instruction': 'COPY',
            'content': '\nCOPY docker-healthcheck /usr/local/bin/ \n',
            'value': 'docker-healthcheck /usr/local/bin/ \n'
        },
        {
            'instruction': 'HEALTHCHECK',
            'content': 'HEALTHCHECK CMD ["docker-healthcheck"]\n',
            'value': 'CMD ["docker-healthcheck"]\n'
        }]
