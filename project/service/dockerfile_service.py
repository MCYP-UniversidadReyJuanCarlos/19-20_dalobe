import re

from project.check_4 import Check_4_1, Check_4_6
from project.fix_4 import Fix_4_1, Fix_4_6
from project.infrastracture.make_docker_file import Make_docker_file


class DockerfileService:

    def check_dockerfile(self, dockerfile_path):
        instructions = DockerfileService.parse_dockerfile(self, dockerfile_path)
        return DockerfileService.evaluate_dockerfile(self, instructions)

    def check_and_fix_dockerfile(self, dockerfile_path):
        instructions = DockerfileService.parse_dockerfile(self, dockerfile_path)
        check_result = DockerfileService.evaluate_dockerfile(self, instructions)
        dockerfile_fixes = DockerfileService.get_dockerfile_fixes(self, check_result)
        Make_docker_file.write_docker_file_from_static(instructions, dockerfile_fixes)
        return check_result

    def parse_dockerfile(self, dockerfile_path):
        parser = DockerfileParser(dockerfile_path)
        instructions = parser.structure()
        return instructions

    def evaluate_dockerfile(self, instructions):
        return [{'4_1': Check_4_1.evaluate_dockerfile(instructions),
                 '4_6': Check_4_6.evaluate_dockerfile(instructions)}]

    def get_dockerfile_fixes(self, check_result):
        fix_dockerfile = []
        user_check_result_failed = list(filter(lambda x: x['4_1']['evaluation'] == 'KO', check_result))
        if user_check_result_failed:
            [fix_dockerfile.append(o) for o in Fix_4_1.fix_dockerfile(self)]
        healthcheck_check_result_failed = list(filter(lambda x: x['4_6']['evaluation'] == 'KO', check_result))
        if healthcheck_check_result_failed:
            [fix_dockerfile.append(o) for o in Fix_4_6.fix_dockerfile(self)]
        return fix_dockerfile


class DockerfileParser:
    def __init__(self, fileobj):
        self.fileobj = fileobj

    def structure(self):
        dockerfile = open(self.fileobj, mode='r', encoding='utf-8')
        lines = [l for l in dockerfile.readlines()]
        lineno = -1
        instructions = []

        def create_instruction_dict(instruction=None, value=None):
            return {
                'instruction': instruction,
                'startline': lineno,
                'endline': lineno,
                'content': line,
                'value': value
            }

        def rstrip_backslash(l):
            l = l.rstrip()
            if l.endswith('\\'):
                return l[:-1]
            return l

        def clean_comment_line(l):
            l = re.sub(r'^\s*#\s*', '', l)
            l = re.sub(r'\n', '', l)
            return l

        lineno = -1
        insnre = re.compile(r'^\s*(\S+)\s+(.*)$')  # instruction
        commentre = re.compile(r'^\s*#')  # comment
        for line in lines:
            lineno += 1
            m = insnre.match(line)
            if not m:
                continue
            if commentre.match(line):
                comment = create_instruction_dict(
                    instruction='COMMENT_INSTRUCTION',
                    value=clean_comment_line(line)
                )
                instructions.append(comment)
            else:
                current_instruction = create_instruction_dict(
                    instruction=m.groups()[0].upper(),
                    value=rstrip_backslash(m.groups()[1])
                )
                current_instruction['endline'] = lineno
                instructions.append(current_instruction)
        dockerfile.close()
        return instructions
