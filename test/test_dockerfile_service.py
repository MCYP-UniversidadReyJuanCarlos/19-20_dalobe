import unittest

from project.service.dockerfile_service import DockerfileParser


class MyTestCase(unittest.TestCase):

    def test_given_a_dockerfile_when_parse_then_instructions_are_parsed(self):
        parser = DockerfileParser('resources/Dockerfile_test1')
        instructions = parser.structure()
        self.assertEqual(len(instructions), 4)
        self.assertEqual(instructions.__getitem__(0).get("instruction"), 'FROM')
        self.assertEqual(instructions.__getitem__(1).get("instruction"), 'RUN')
        self.assertEqual(instructions.__getitem__(0).get("value"), 'alpine:3.4')

    def test_given_an_empty_dockerfile_when_parse_then_instructions_is_empty(self):
        parser = DockerfileParser('resources/Dockerfile_empty')
        instructions = parser.structure()
        self.assertEqual(len(instructions), 0)

    def test_given_a_dockerfile_with_comments_when_parse_then_comments_are_not_parsed(self):
        parser = DockerfileParser('resources/Dockerfile_test2')
        instructions = parser.structure()
        self.assertEqual(len(instructions), 5)
        self.assertEqual(instructions.__getitem__(2).get("instruction"), 'COMMENT_INSTRUCTION')
        self.assertEqual(instructions.__getitem__(0).get("instruction"), 'FROM')
        self.assertEqual(instructions.__getitem__(1).get("instruction"), 'RUN')
        self.assertEqual(instructions.__getitem__(0).get("value"), 'alpine:3.4')


if __name__ == '__main__':
    unittest.main()
