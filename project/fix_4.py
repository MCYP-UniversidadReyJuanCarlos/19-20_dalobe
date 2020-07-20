import shutil


class Fix_4_1:

    def fix_dockerfile(self):
        # 'RUN useradd -d /home/username -m -s /bin/bash username \nUSER username \n\n'
        return [{
            'instruction': 'RUN',
            'content': '\nRUN useradd -d /home/username -m -s /bin/bash username \n',
            'value': 'useradd -d /home/username -m -s /bin/bash username \n'
        }, {
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


class Fix_4_9:

    def fix_dockerfile(self, check_result, instructions):
        lines_with_add_wrong_usage = []
        lines = check_result['line']
        for line in lines:
            line_with_add_wrong_usage = next(filter(lambda x: x['startline'] == line, instructions))
            lines_with_add_wrong_usage.append(line_with_add_wrong_usage)

        fixed_lines = []
        [fixed_lines.append(Fix_4_9.fix_line(o)) for o in lines_with_add_wrong_usage]
        return fixed_lines

    def fix_line(o):
        return {
            'instruction': 'COPY',
            'startline': o['startline'],
            'endline': o['endline'],
            'content': 'COPY ' + o['value'],
            'value': o['value']
        }
