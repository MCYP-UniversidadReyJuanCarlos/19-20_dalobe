import unittest
from unittest import mock

from docker.models.containers import Container

from project.check_4 import Check_4_1, Check_4_6


class Check_4_1_Test(unittest.TestCase):
    inspect_container_not_root_user_item = {'Config': {
        'User': 'sonarqube'}}

    inspect_container_root_user_item = {'Config': {
        'User': 'root'}}

    inspect_container_empty_user_item = {'Config': {
        'User': ''}}

    inspect_container_null_user_item = {'Config': {
        'User': None}}

    @mock.patch("docker.APIClient.inspect_container", return_value=inspect_container_not_root_user_item)
    def test_given_container_when_config_user_is_not_root_then_OK(self, mocked_inspect):
        container = Container()
        ret = Check_4_1.evaluate_container(container)
        assert mocked_inspect.called
        self.assertEqual(ret['evaluation'], 'OK')

    @mock.patch("docker.APIClient.inspect_container", return_value=inspect_container_root_user_item)
    def test_given_container_when_config_user_is_root_then_KO(self, mocked_inspect):
        container = Container()
        ret = Check_4_1.evaluate_container(container)
        assert mocked_inspect.called
        self.assertEqual(ret['evaluation'], 'KO')

    @mock.patch("docker.APIClient.inspect_container", return_value=inspect_container_empty_user_item)
    def test_given_container_when_config_user_is_empty_then_KO(self, mocked_inspect):
        container = Container()
        ret = Check_4_1.evaluate_container(container)
        assert mocked_inspect.called
        self.assertEqual(ret['evaluation'], 'KO')

    @mock.patch("docker.APIClient.inspect_container", return_value=inspect_container_null_user_item)
    def test_given_container_when_config_user_is_null_then_KO(self, mocked_inspect):
        container = Container()
        ret = Check_4_1.evaluate_container(container)
        assert mocked_inspect.called
        self.assertEqual(ret['evaluation'], 'KO')


class Check_4_6_Test(unittest.TestCase):
    inspect_container_no_healthcheck_item = {"Config": {
        "Hostname": "4a755ce1ea46",
        "Domainname": "",
        "User": "",
        "AttachStdin": False,
        "AttachStdout": True,
        "AttachStderr": True,
        "Tty": True,
        "OpenStdin": False,
        "StdinOnce": False}}

    @mock.patch("docker.APIClient.inspect_container", return_value=inspect_container_no_healthcheck_item)
    def test_given_container_when_no_healtheck_then_KO(self, mocked_inspect):
        container = Container()
        ret = Check_4_6.evaluate_container(container)
        assert mocked_inspect.called
        self.assertEqual(ret['evaluation'], 'KO')


if __name__ == '__main__':
    unittest.main()
