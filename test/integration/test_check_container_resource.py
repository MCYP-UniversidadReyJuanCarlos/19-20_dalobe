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
        file = open('test/resources/Dockerfile_with_user', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': file.read()})
        data = json.loads(result.data)
        user_check_result = list(filter(lambda x: x['4_1']['evaluation'] == 'OK', data["dockerFile"]))
        self.assertEqual(len(user_check_result), 1)

    def test_post_given_dockerfile_without_user_when_check_then_KO(self):
        file = open('test/resources/Dockerfile_basic', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': file.read()})
        data = json.loads(result.data)
        user_check_result = list(filter(lambda x: x['4_1']['evaluation'] == 'KO', data["dockerFile"]))
        self.assertEqual(len(user_check_result), 1)

    def test_post_given_dockerfile_with_healthcheck_when_check_then_OK(self):
        file = open('test/resources/Dockerfile_with_user', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': file.read()})
        data = json.loads(result.data)
        user_check_result = list(filter(lambda x: x['4_1']['evaluation'] == 'OK', data["dockerFile"]))
        self.assertEqual(len(user_check_result), 1)

    def test_post_given_dockerfile_without_healthcheck_when_check_then_KO(self):
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': 'test/resources/Dockerfile_basic'})
        data = json.loads(result.data)
        user_check_result = list(filter(lambda x: x['4_6']['evaluation'] == 'KO', data["dockerFile"]))
        self.assertEqual(len(user_check_result), 1)

    def test_post_given_dockerfile_with_ADD_when_check_then_KO(self):
        file = open('test/resources/Dockerfile_wrong_ADD_usage', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': file.read()})
        data = json.loads(result.data)
        user_check_result = list(filter(lambda x: x['4_9']['evaluation'] == 'KO', data["dockerFile"]))
        self.assertEqual(len(user_check_result), 1)

    def test_post_given_dockerfile_with_COPY_when_check_then_OK(self):
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': 'test/resources/Dockerfile_proper_COPY_usage'})
        data = json.loads(result.data)
        user_check_result2 = list(filter(lambda x: x['4_9']['evaluation'] == 'OK', data["dockerFile"]))
        self.assertEqual(len(user_check_result2), 1)

    def test_post_given_dockerfile_with_ADD_tar_when_check_then_OK(self):
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': 'test/resources/Dockerfile_proper_ADD_tar_usage'})
        data = json.loads(result.data)
        user_check_result2 = list(filter(lambda x: x['4_9']['evaluation'] == 'OK', data["dockerFile"]))
        self.assertEqual(len(user_check_result2), 1)

    def test_post_given_dockerfile_with_ADD_https_when_check_then_OK(self):
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': 'test/resources/Dockerfile_proper_ADD_https_usage'})
        data = json.loads(result.data)
        add_check_result = list(filter(lambda x: x['4_9']['evaluation'] == 'OK', data["dockerFile"]))
        self.assertEqual(len(add_check_result), 1)

    def test_post_given_dockerfile_with_two_ADD_when_check_then_KO(self):
        file = open('test/resources/Dockerfile_proper_two_ADD_instructions', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': file.read()})
        data = json.loads(result.data)
        add_check_result = list(filter(lambda x: x['4_9']['evaluation'] == 'KO', data["dockerFile"]))
        self.assertEqual(len(add_check_result), 1)

    def test_post_given_dockerfile_with_wrong_ADD_when_check_then_line_is_returned(self):
        file = open('test/resources/Dockerfile_proper_two_ADD_instructions', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': file.read()})
        data = json.loads(result.data)
        add_check_result = list(filter(lambda x: x['4_9']['evaluation'] == 'KO', data["dockerFile"]))
        self.assertEqual(add_check_result[0]['4_9']['line'], [5, 6])

    def test_post_given_dockerfile_with_ADD_when_check_and_fix_then_KO_and_fix(self):
        file = open('test/resources/Dockerfile_wrong_ADD_usage', 'r')
        result = self.app.post('/sds/images/dockerfile/fix', json={
            'dockerFile': file.read()})
        data = json.loads(result.data)
        user_check_result = list(filter(lambda x: x['4_9']['evaluation'] == 'KO', data["dockerFile"]))
        self.assertEqual(len(user_check_result), 1)

    def test_post_given_dockerfile_with_two_apt_get_when_check_then_KO(self):
        file = open('test/resources/Dockerfile_with_two_apt-get', 'r')
        result = self.app.post('/sds/images/dockerfile/fix', json={
            'dockerFile': file.read()})
        data = json.loads(result.data)
        apt_get_check_result = list(filter(lambda x: x['4_7']['evaluation'] == 'KO', data["dockerFile"]))
        self.assertEqual(len(apt_get_check_result), 1)

    def test_post_given_dockerfile_with_no_apt_get_when_check_then_OK(self):
        file = open('test/resources/Dockerfile_basic', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': file.read()})
        data = json.loads(result.data)
        apt_get_check_result = list(filter(lambda x: x['4_7']['evaluation'] == 'OK', data["dockerFile"]))
        self.assertEqual(len(apt_get_check_result), 1)

    def test_post_given_dockerfile_with_proper_apt_get_when_check_then_OK(self):
        file = open('test/resources/Dockerfile_with_proper_apt-get_usage', 'r')
        result = self.app.post('/sds/images/dockerfile/check', json={
            'dockerFile': file.read()})
        data = json.loads(result.data)
        apt_get_check_result = list(filter(lambda x: x['4_7']['evaluation'] == 'OK', data["dockerFile"]))
        self.assertEqual(len(apt_get_check_result), 1)

    def test_post_given_dockerfile_with_wrong_aptget_usage_when_fix_and_check_then_KO_and_fix(self):
        file = open('test/resources/Dockerfile_with_two_apt-get', 'r')
        result = self.app.post('/sds/images/dockerfile/fix', json={
            'dockerFile': file.read()})
        data = json.loads(result.data)
        user_check_result = list(filter(lambda x: x['4_7']['evaluation'] == 'KO', data["dockerFile"]))
        self.assertEqual(len(user_check_result), 1)