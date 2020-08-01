import json
from unittest import TestCase

from project.resource import check_container_resource

DOCKER_FILE = 'dockerfile'


class Test(TestCase):
    def setUp(self):
        check_container_resource.app.testing = True
        self.app = check_container_resource.app.test_client()

    def test_get_healthcheck(self):
        result = self.app.get('/sds/health')
        print(result)

    def test_post_given_dockerfile_with_ADD_when_check_then_KO(self):
        file = open('test/resources/Dockerfile_wrong_ADD_usage', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            DOCKER_FILE: file.read()})
        data = json.loads(result.data)
        self.assertEqual(data['dockerfile_evaluation']['4_9']['evaluation'], 'KO')

    def test_post_given_dockerfile_with_COPY_when_check_then_OK(self):
        result = self.app.post('/sds/images/dockerfile/check', json={
            DOCKER_FILE: 'test/resources/Dockerfile_proper_COPY_usage'})
        data = json.loads(result.data)
        self.assertEqual(data['dockerfile_evaluation']['4_9']['evaluation'], 'OK')

    def test_post_given_dockerfile_with_ADD_tar_when_check_then_OK(self):
        result = self.app.post('/sds/images/dockerfile/check', json={
            DOCKER_FILE: 'test/resources/Dockerfile_proper_ADD_tar_usage'})
        data = json.loads(result.data)
        self.assertEqual(data['dockerfile_evaluation']['4_9']['evaluation'], 'OK')

    def test_post_given_dockerfile_with_ADD_https_when_check_then_OK(self):
        result = self.app.post('/sds/images/dockerfile/check', json={
            DOCKER_FILE: 'test/resources/Dockerfile_proper_ADD_https_usage'})
        data = json.loads(result.data)
        self.assertEqual(data['dockerfile_evaluation']['4_9']['evaluation'], 'OK')

    def test_post_given_dockerfile_with_two_ADD_when_check_then_KO(self):
        file = open('test/resources/Dockerfile_proper_two_ADD_instructions', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            DOCKER_FILE: file.read()})
        data = json.loads(result.data)
        self.assertEqual(data['dockerfile_evaluation']['4_9']['evaluation'], 'KO')

    def test_post_given_dockerfile_with_wrong_ADD_when_check_then_line_is_returned(self):
        file = open('test/resources/Dockerfile_proper_two_ADD_instructions', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            DOCKER_FILE: file.read()})
        data = json.loads(result.data)
        self.assertEqual(data['dockerfile_evaluation']['4_9']['evaluation'], 'KO')
        self.assertEqual(data['dockerfile_evaluation']['4_9']['line'], [5, 6])

    def test_post_given_dockerfile_with_ADD_when_check_and_fix_then_KO_and_fix(self):
        file = open('test/resources/Dockerfile_wrong_ADD_usage', 'r')
        result = self.app.post('/sds/images/dockerfile/fix', json={
            DOCKER_FILE: file.read()})
        data = json.loads(result.data)
        self.assertEqual(data[0]['dockerfile_evaluation']['4_9']['evaluation'], 'KO')

