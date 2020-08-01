import json
from unittest import TestCase

from project.resource import check_container_resource

DOCKER_FILE = 'dockerfile'


class Test(TestCase):
    def setUp(self):
        check_container_resource.app.testing = True
        self.app = check_container_resource.app.test_client()

    def test_post_given_dockerfile_with_healthcheck_when_check_then_OK(self):
        file = open('test/resources/Dockerfile_with_healthcheck', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            DOCKER_FILE: file.read()})
        data = json.loads(result.data)
        self.assertEqual(data['dockerfile_evaluation']['4_6']['evaluation'], 'OK')

    def test_post_given_dockerfile_without_healthcheck_when_check_then_KO(self):
        result = self.app.post('/sds/images/dockerfile/check', json={
            DOCKER_FILE: 'test/resources/Dockerfile_basic'})
        data = json.loads(result.data)
        self.assertEqual(data['dockerfile_evaluation']['4_6']['evaluation'], 'KO')

    def test_post_given_dockerfile_without_healthcheck_when_check_and_fix_then_KO_and_fix(self):
        file = open('test/resources/Dockerfile_basic', 'r')
        result = self.app.post('/sds/images/dockerfile/fix', json={
            DOCKER_FILE: file.read()})
        data = json.loads(result.data)
        self.assertEqual(data[0]['dockerfile_evaluation']['4_6']['evaluation'], 'KO')
        self.assertIn('HEALTHCHECK',data[1]['proposed_dockerfile'])
        self.assertEqual(data[1]['proposed_dockerfile'].count('HEALTHCHECK'),1)

    def test_post_given_dockerfile_with_healthcheck_when_check_and_fix_then_OK_and_no_fix(self):
        file = open('test/resources/Dockerfile_with_healthcheck', 'r')
        result = self.app.post('/sds/images/dockerfile/fix', json={
            DOCKER_FILE: file.read()})
        data = json.loads(result.data)
        self.assertEqual(data[0]['dockerfile_evaluation']['4_6']['evaluation'], 'OK')
        self.assertIn('HEALTHCHECK',data[1]['proposed_dockerfile'])
        self.assertEqual(data[1]['proposed_dockerfile'].count('HEALTHCHECK'),1)

