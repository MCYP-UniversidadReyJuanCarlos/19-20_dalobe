import unittest
from unittest import mock

from docker.models.containers import Container

from project.check_4 import Check_4_1


class MyTestCase(unittest.TestCase):
    inspect_container_not_root_user_item = {'Config': {
        'User': 'sonarqube'}}

    inspect_container_root_user_item = {'Config': {
        'User': 'root'}}

    inspect_container_empty_user_item = {'Config': {
        'User': ''}}

    @mock.patch("docker.APIClient.inspect_container", return_value=inspect_container_not_root_user_item)
    def test_given_container_when_config_user_is_not_root(self, mockedInspect):
        container = Container()
        ret = Check_4_1.evaluate_container(container)
        assert mockedInspect.called
        self.assertEqual(ret, 'OK')

    @mock.patch("docker.APIClient.inspect_container", return_value=inspect_container_root_user_item)
    def test_given_container_when_config_user_is_root(self, mockedInspect):
        container = Container()
        ret = Check_4_1.evaluate_container(container)
        assert mockedInspect.called
        self.assertEqual(ret, 'KO')

    @mock.patch("docker.APIClient.inspect_container", return_value=inspect_container_empty_user_item)
    def test_given_container_when_config_user_is_empty(self, mockedInspect):
        container = Container()
        ret = Check_4_1.evaluate_container(container)
        assert mockedInspect.called
        self.assertEqual(ret, 'KO')


if __name__ == '__main__':
    unittest.main()
