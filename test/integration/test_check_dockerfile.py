import json
from unittest import TestCase

from project.resource import check_container_resource

DOCKER_FILE = 'dockerfile'
PROPOSED_DOCKER_FILE = 'proposed_dockerfile'

class Test(TestCase):
    def setUp(self):
        check_container_resource.app.testing = True
        self.app = check_container_resource.app.test_client()

    def test_get_healthcheck(self):
        result = self.app.get('/sds/health')
        print(result)

    def test_post_given_dockerfile_with_two_apt_get_when_check_then_KO(self):
        file = open('test/resources/Dockerfile_with_two_apt-get', 'r')
        result = self.app.post('/sds/images/dockerfile/fix', json={
            DOCKER_FILE: file.read()})
        data = json.loads(result.data)
        self.assertEqual(data[0]['dockerfile_evaluation']['4_7']['evaluation'], 'KO')

    def test_post_given_dockerfile_with_no_apt_get_when_check_then_OK(self):
        file = open('test/resources/Dockerfile_basic', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            DOCKER_FILE: file.read()})
        data = json.loads(result.data)
        self.assertEqual(data['dockerfile_evaluation']['4_7']['evaluation'], 'OK')

    def test_post_given_dockerfile_with_proper_apt_get_when_check_then_OK(self):
        file = open('test/resources/Dockerfile_with_proper_apt-get_usage', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            DOCKER_FILE: file.read()})
        data = json.loads(result.data)
        self.assertEqual(data['dockerfile_evaluation']['4_7']['evaluation'], 'OK')

    def test_post_given_dockerfile_with_wrong_aptget_usage_when_fix_and_check_then_KO_and_fix(self):
        file = open('test/resources/Dockerfile_with_two_apt-get', 'r')
        result = self.app.post('/sds/images/dockerfile/fix', json={
            DOCKER_FILE: file.read()})
        data = json.loads(result.data)
        self.assertEqual(data[0]['dockerfile_evaluation']['4_7']['evaluation'], 'KO')

    def test_post_given_dockerfile_with_from_instrucion_when_check_then_OK(self):
        file = open('test/resources/Dockerfile_basic_with_comments', 'r')
        result = self.app.post('/sds/images/dockerfile/fix', json={
            DOCKER_FILE: file.read()})
        data = json.loads(result.data)
        self.assertEqual(data[0]['dockerfile_evaluation']['4_7']['evaluation'], 'OK')
