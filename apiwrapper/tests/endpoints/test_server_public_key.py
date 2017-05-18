from apiwrapper.endpoints.server_public_key import ServerPublicKey
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class ServerPublicKeyTest(EndpointTest):
    __base_endpoint_url = "/installation/%d/server-public-key"

    @property
    def _base_endpoint(self):
        return self.__base_endpoint_url % self.random_id

    def setUp(self):
        super().setUp(ServerPublicKey)

    def test_get_base_endpoint(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class._get_base_endpoint(
            self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_server_pubkey_for_installation(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class.get_server_pubkey_for_installation(
            self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)
