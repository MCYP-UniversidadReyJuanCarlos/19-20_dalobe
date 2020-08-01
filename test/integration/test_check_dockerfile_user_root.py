import json
from unittest import TestCase

from project.resource import check_container_resource

DOCKER_FILE = 'dockerfile'


class Test(TestCase):
    def setUp(self):
        check_container_resource.app.testing = True
        self.app = check_container_resource.app.test_client()

    def test_post_given_dockerfile_with_user_when_check_then_OK(self):
        file = open('test/resources/Dockerfile_with_user', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            DOCKER_FILE: file.read()})
        data = json.loads(result.data)
        self.assertEqual(data['dockerfile_evaluation']['4_1']['evaluation'], 'OK')

    def test_post_given_dockerfile_without_user_when_check_then_KO(self):
        file = open('test/resources/Dockerfile_basic', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            DOCKER_FILE: file.read()})
        data = json.loads(result.data)
        self.assertEqual(data['dockerfile_evaluation']['4_1']['evaluation'], 'KO')

