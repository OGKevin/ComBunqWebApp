from apiwrapper.endpoints.installation import Installation
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class InstallationTest(EndpointTest):
    __base_endpoint_url = "/installation"

    @property
    def _base_endpoint(self):
        return self.__base_endpoint_url

    def setUp(self):
        super().setUp(Installation)

    def test_get_base_endpoint(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class._get_base_endpoint()

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_id_for_installation(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class.get_id_for_installation()

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_check_installation_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%d" % self.random_id

        endpoint_to_check = self.test_class.check_installation_id(self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_create_installation_endpoint(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check, _ = self.test_class.create_installation()

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_create_installation_payload(self):
        payload_should_be = {
            "client_public_key": self.api_client.pubkey
        }

        _, payload_to_check = self.test_class.create_installation()

        self.assert_parameters(payload_should_be, payload_to_check )
