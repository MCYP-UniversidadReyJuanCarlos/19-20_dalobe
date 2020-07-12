import unittest
from unittest import mock

from project.service.containers_service import get_running_containers


class Container_Service_Test(unittest.TestCase):
    container_list = [
        {
            "Id": "43dcdb92c72d71fde474bc980755bf5e2ef5edd1b9d9b4347455a97650d1db60",
            "labels": {
                "maintainer": "NGINX Docker Maintainers <docker-maint@nginx.com>"
            },
            "name": "vibrant_keller",
            "ports": {
                "80/tcp": 'null',
                "8080/tcp": [
                    {
                        "HostIp": "0.0.0.0",
                        "HostPort": "80"
                    }
                ]
            },
            "status": "running"
        }
    ]

    @mock.patch("docker.APIClient.containers")
    def test_given_a_container_running_when_call_get_containers_then_one_element_is_returned(self, mock_listdir):
        mock_listdir.return_value = Container_Service_Test.container_list
        containers = get_running_containers()
        self.assertEqual(len(containers), 1)

    @mock.patch("docker.APIClient.containers", return_value=[])
    def test_given_no_container_running_when_call_get_containers_then_no_element_is_returned(self, mockedInspect):
        containers = get_running_containers()
        assert mockedInspect.called
        self.assertEqual(len(containers), 0)


if __name__ == '__main__':
    unittest.main()
