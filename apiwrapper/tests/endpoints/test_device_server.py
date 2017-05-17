import random
import unittest

from faker import Faker

from apiwrapper.endpoints.device_server import DeviceServer
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class DeviceServerTest(EndpointTest, unittest.TestCase):

    def setUp(self):
        super().setUp(DeviceServer)
        self.faker = Faker()

    def test_get_base_endpoint(self):
        endpoint_should_be = "/device-server"
        endpoint_to_check = self.test_class.get_base_endpoint()
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_device_servers(self):
        endpoint_should_be = "/device-server"
        endpoint_to_check = self.test_class.get_all_device_servers()
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_device_server_by_id(self):
        endpoint_should_be = "/device-server/%d" % (
            self.random_id
        )
        endpoint_to_check = self.test_class.get_device_server_by_id(
            self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_create_new_device_server_endpoint(self):
        endpoint_should_be = "/device-server"
        endpoint_to_check, _ = \
            self.test_class.create_new_device_server(
                self.random_uuid)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_create_new_device_server_payload(self):
        description = self.faker.name()
        permitted_ips = []
        for x in range(0, random.randint(1, 10)):
            permitted_ips.append(self.faker.ssn())

        payload_should_be = {
            "description": description,
            "secret": self.api_client.api_key,
            "permitted_ips": permitted_ips
        }

        _, payload_to_check = \
            self.test_class.create_new_device_server(
                description, permitted_ips)

        self.assert_parameters(payload_should_be, payload_to_check)
