import docker

import re


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
