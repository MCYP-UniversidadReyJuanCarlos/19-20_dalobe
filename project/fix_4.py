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

class Fix_4_7:

    def fix_dockerfile(self, check_result, instructions):
        lines_with_apt_get_usage = []
        lines = check_result['line']
        for line in lines:
            line_with_apt_get_usage = next(filter(lambda x: x['startline'] == line, instructions))
            lines_with_apt_get_usage.append(line_with_apt_get_usage)
        fixed_lines = []
        values = list(map(lambda x:x['value'], lines_with_apt_get_usage))
        apt_get_one_line = ' && '.join(values)
        instruction = {
            'instruction': 'RUN',
            'startline': lines_with_apt_get_usage[0]['startline'],
            'endline': lines_with_apt_get_usage[0]['startline'],
            'content': 'RUN ' + apt_get_one_line,
            'value': apt_get_one_line
        }
        lines_to_remove = (lines[1:len(lines)]);
        fixed_lines.append(instruction)
        for i in lines_to_remove:
            instruction_to_remove = {
                'instruction': '',
                'startline': i,
                'endline': i,
                'content': '',
                'value': ''
            }
            fixed_lines.append(instruction_to_remove)
        return fixed_lines

class Fix_4_9:

    def fix_dockerfile(self, check_result, instructions):
        lines_with_add_wrong_usage = []
        lines = check_result['line']
        for line in lines:
            lines_with_add_wrong_usage.append(next(filter(lambda x: x['startline'] == line, instructions)))
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
