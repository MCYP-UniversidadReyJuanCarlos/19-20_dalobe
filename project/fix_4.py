class Fix_4_1:

    def fix_container(container):
        return 'RUN useradd -d /home/username -m -s /bin/bash username \n USER username \n'


class Fix_4_6:

    def fix_container(container):
        return 'COPY docker-healthcheck /usr/local/bin/ \n HEALTHCHECK CMD ["docker-healthcheck"]'
