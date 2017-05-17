import unittest

from apiwrapper.endpoints.session_server import SessionServer
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class SessionServerTest(EndpointTest, unittest.TestCase):

    def setUp(self):
        super().setUp(SessionServer)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/session-server"
        endpoint_to_check = self.test_class.get_base_endpoint()
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_create_new_session_server_endpoint(self):
        endpoint_should_be = "/session-server"
        endpoint_to_check, _ = self.test_class.create_new_session_server()
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_create_new_session_server_payload(self):
        payload_should_be = {
            "secret": self.api_client.api_key
        }
        _, payload_to_check = self.test_class.create_new_session_server()
        self.assert_parameters(payload_should_be, payload_to_check)
