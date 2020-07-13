import json
from unittest import TestCase

from project.resource import check_container_resource


class Test(TestCase):
    def setUp(self):
        check_container_resource.app.testing = True
        self.app = check_container_resource.app.test_client()

    def test_get_healthcheck(self):
        result = self.app.get('/sds/health')
        print(result)

    def test_post_given_dockerfile_with_user_when_check_then_OK(self):
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': 'test/resources/Dockerfile_with_user'})
        data = json.loads(result.data)
        user_check_result = list(filter(lambda x: x['4_1']['evaluation'] == 'OK', data["dockerFile"]))
        self.assertEqual(len(user_check_result),1)

    def test_post_given_dockerfile_without_user_when_check_then_KO(self):
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': 'test/resources/Dockerfile_test1'})
        data = json.loads(result.data)
        user_check_result = list(filter(lambda x: x['4_1']['evaluation'] == 'KO', data["dockerFile"]))
        self.assertEqual(len(user_check_result),1)

    def test_post_given_dockerfile_with_healthcheck_when_check_then_OK(self):
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': 'test/resources/Dockerfile_with_user'})
        data = json.loads(result.data)
        user_check_result = list(filter(lambda x: x['4_1']['evaluation'] == 'OK', data["dockerFile"]))
        self.assertEqual(len(user_check_result),1)

    def test_post_given_dockerfile_without_healthcheck_when_check_then_KO(self):
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': 'test/resources/Dockerfile_test1'})
        data = json.loads(result.data)
        user_check_result = list(filter(lambda x: x['4_6']['evaluation'] == 'KO', data["dockerFile"]))
        self.assertEqual(len(user_check_result),1)
