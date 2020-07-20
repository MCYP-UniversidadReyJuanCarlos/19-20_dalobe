from unittest import TestCase

from project.infrastracture.make_dockerfile import Make_docker_file


class Test_make_dockerfile(TestCase):
    def test_given_fixes_with_copy_when_write_then_copy_overwrittes_add(self):
        instructions = [{'instruction': 'FROM', 'startline': 0, 'endline': 0, 'content': 'FROM alpine\n', 'value': 'alpine'},
                        {'instruction': 'ENV', 'startline': 1, 'endline': 1, 'content': 'ENV ADMIN_USER="mark"\n', 'value': 'ADMIN_USER="mark"'},
                        {'instruction': 'RUN', 'startline': 2, 'endline': 2, 'content': 'RUN echo $ADMIN_USER > '
                                                                                        './mark\n', 'value': 'echo '
                                                                                                             '$ADMIN_USER > ./mark'},
                        {'instruction': 'RUN', 'startline': 3, 'endline': 3, 'content': 'RUN unset ADMIN_USER\n', 'value': 'unset ADMIN_USER'},
                        {'instruction': 'COPY', 'startline': 4, 'endline': 4, 'content': 'COPY requirements.txt /tmp/\n', 'value': 'requirements.txt /tmp/'},
                        {'instruction': 'RUN', 'startline': 5, 'endline': 5, 'content': 'RUN pip install '
                                                                                        '--requirement '
                                                                                        '/tmp/requirements.txt\n',
                         'value': 'pip install --requirement /tmp/requirements.txt'},
                        {'instruction': 'ADD', 'startline': 6, 'endline': 6, 'content': 'ADD . /tmp/', 'value': '. '
                                                                                                                '/tmp/'}]
        dockerfile_fixes = [
                        {'instruction': 'COPY', 'startline': 6, 'endline': 6, 'content': 'COPY . /tmp/', 'value': '. '
                                                                                                                '/tmp/'}]

        proposed_dockerfile = Make_docker_file.generate_proposed_dockerfile(instructions, dockerfile_fixes)
        self.assertEqual(len(proposed_dockerfile), 7)
        self.assertEqual(proposed_dockerfile[6]['instruction'],'COPY')

