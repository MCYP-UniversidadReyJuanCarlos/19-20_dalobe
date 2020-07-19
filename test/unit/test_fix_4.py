import unittest


from project.fix_4 import Fix_4_9


class Check_4_9_Test(unittest.TestCase):

    def test_given_result_with_wrong_add_usage_when_fix_then_copy_instruction_returned(self):
        check_result = {'evaluation': 'KO',
                        'code': 'DOCKERFILE_WITH_ADD_INSTRUCTION_NOT_PROPER_USED',
                        'description': 'You should use COPY rather than ADD instructions in Dockerfiles.',
                        'line': [6]}
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
        result = Fix_4_9.fix_dockerfile(self,check_result,instructions)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['instruction'],'COPY')

    def test_given_result_with_two_wrong_add_usage_when_fix_then_copy_instruction_returned(self):
        check_result = {'evaluation': 'KO',
                        'code': 'DOCKERFILE_WITH_ADD_INSTRUCTION_NOT_PROPER_USED',
                        'description': 'You should use COPY rather than ADD instructions in Dockerfiles.',
                        'line': [4,6]}
        instructions = [{'instruction': 'FROM', 'startline': 0, 'endline': 0, 'content': 'FROM alpine\n', 'value': 'alpine'},
                        {'instruction': 'ENV', 'startline': 1, 'endline': 1, 'content': 'ENV ADMIN_USER="mark"\n', 'value': 'ADMIN_USER="mark"'},
                        {'instruction': 'RUN', 'startline': 2, 'endline': 2, 'content': 'RUN echo $ADMIN_USER > '
                                                                                        './mark\n', 'value': 'echo '
                                                                                                             '$ADMIN_USER > ./mark'},
                        {'instruction': 'RUN', 'startline': 3, 'endline': 3, 'content': 'RUN unset ADMIN_USER\n', 'value': 'unset ADMIN_USER'},
                        {'instruction': 'ADD', 'startline': 4, 'endline': 6, 'content': 'ADD . /tmp/', 'value': '. '
                                                                                                                '/tmp/'},
                        {'instruction': 'RUN', 'startline': 5, 'endline': 5, 'content': 'RUN pip install '
                                                                                        '--requirement '
                                                                                        '/tmp/requirements.txt\n',
                         'value': 'pip install --requirement /tmp/requirements.txt'},
                        {'instruction': 'ADD', 'startline': 6, 'endline': 6, 'content': 'ADD . /tmp/', 'value': '. '
                                                                                                                '/tmp/'}]
        result = Fix_4_9.fix_dockerfile(self,check_result,instructions)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['instruction'],'COPY')
        self.assertEqual(result[1]['instruction'], 'COPY')


if __name__ == '__main__':
    unittest.main()
