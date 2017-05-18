from apiwrapper.endpoints.credential_password_ip import CredentialPasswordIp
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class CredentialPasswordIpTest(EndpointTest):
    __base_endpoint_url = "/user/%d/credential-password-ip"

    @property
    def _base_endpoint(self):
        return self.__base_endpoint_url % self.random_id

    def setUp(self):
        super().setUp(CredentialPasswordIp)

    def test_get_base_endpoint(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class._get_base_endpoint(
            self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_credentials_for_user(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class.get_all_credentials_for_user(
            self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_credential_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%d" % self.random_id

        endpoint_to_check = self.test_class.get_credential_by_id(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)
