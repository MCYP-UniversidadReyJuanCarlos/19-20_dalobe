import shutil


class Fix_4_1:

    def fix_container(container):
        return 'RUN useradd -d /home/username -m -s /bin/bash username \nUSER username \n\n'


class Fix_4_6:

    def fix_container(container):
        shutil.copyfile('../../templates/docker-healthcheck', '../../output/docker-healthcheck')
        return 'COPY docker-healthcheck /usr/local/bin/ \nHEALTHCHECK CMD ["docker-healthcheck"]\n'
