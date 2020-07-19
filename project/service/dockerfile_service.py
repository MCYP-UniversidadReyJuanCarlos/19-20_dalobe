import re

from project.check_4 import Check_4_1, Check_4_6, Check_4_9
from project.fix_4 import Fix_4_1, Fix_4_6, Fix_4_9
from project.infrastracture.make_docker_file import Make_docker_file


class DockerfileService:

    def check_dockerfile(self, dockerfile_path):
        instructions = DockerfileService.parse_dockerfile(self, dockerfile_path)
        return DockerfileService.evaluate_dockerfile(self, instructions)

    def check_and_fix_dockerfile(self, dockerfile_path):
        instructions = DockerfileService.parse_dockerfile(self, dockerfile_path)
        check_result = DockerfileService.evaluate_dockerfile(self, instructions)
        dockerfile_fixes = DockerfileService.get_dockerfile_fixes(self, check_result, instructions)
        Make_docker_file.write_docker_file_from_static(instructions, dockerfile_fixes)
        return check_result

    def parse_dockerfile(self, dockerfile_path):
        parser = DockerfileParser(dockerfile_path)
        instructions = parser.structure()
        return instructions

    def evaluate_dockerfile(self, instructions):
        return [{'4_1': Check_4_1.evaluate_dockerfile(instructions),
                 '4_6': Check_4_6.evaluate_dockerfile(instructions),
                 '4_9': Check_4_9.evaluate_dockerfile(instructions),
                 }]

    def get_dockerfile_fixes(self, check_result, instructions=None):
        fix_dockerfile = []
        user_check_result = check_result[0]['4_1']
        if user_check_result['evaluation'] == 'KO':
            [fix_dockerfile.append(o) for o in Fix_4_1.fix_dockerfile(self)]

        healthcheck_check_result = check_result[0]['4_6']
        if healthcheck_check_result['evaluation'] == 'KO':
            [fix_dockerfile.append(o) for o in Fix_4_6.fix_dockerfile(self)]

        add_check_result = check_result[0]['4_9']
        if add_check_result['evaluation'] == 'KO':
            [fix_dockerfile.append(o) for o in Fix_4_9.fix_dockerfile(self, add_check_result, instructions)]

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
        insnre = re.compile(r'^\s*(\S+)\s+(.*)$')  # matched group is insn
        contre = re.compile(r'^.*\\\s*$')          # line continues?
        commentre = re.compile(r'^\s*#')           # line is a comment?

        in_continuation = False
        current_instruction = None

        for line in lines:
            lineno += 1

            # It is necessary to keep instructions and comment parsing separate,
            # as a multi-line instruction can be interjected with comments.
            if commentre.match(line):
                comment = create_instruction_dict(
                    instruction='COMMENT_INSTRUCTION',
                    value=clean_comment_line(line)
                )
                instructions.append(comment)

            else:
                if not in_continuation:
                    m = insnre.match(line)
                    if not m:
                        continue
                    current_instruction = create_instruction_dict(
                        instruction=m.groups()[0].upper(),
                        value=rstrip_backslash(m.groups()[1])
                    )
                else:
                    current_instruction['content'] += line
                    current_instruction['endline'] = lineno

                    # pylint: disable=unsupported-assignment-operation
                    if current_instruction['value']:
                        current_instruction['value'] += rstrip_backslash(line)
                    else:
                        current_instruction['value'] = rstrip_backslash(line.lstrip())
                    # pylint: enable=unsupported-assignment-operation

                in_continuation = contre.match(line)
                if not in_continuation and current_instruction is not None:
                    instructions.append(current_instruction)
        dockerfile.close()
        return instructions
