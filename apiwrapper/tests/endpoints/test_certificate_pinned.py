from apiwrapper.endpoints.certificate_pinned import CertificatePinned
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class CertificatePinnedTest(EndpointTest):
    __base_endpoint_url = "/user/%d/certificate-pinned"

    @property
    def _base_endpoint(self):
        return self.__base_endpoint_url % self.random_id

    def setUp(self):
        super().setUp(CertificatePinned)

    def test_get_base_endpoint(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class._get_base_endpoint(
            self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_pinned_certificates_for_user(self):
        endpoint_should_be = self._base_endpoint

        endpoint_to_check = self.test_class.get_all_pinned_certificates_for_user(
            self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_pinned_certificate_by_id(self):
        endpoint_should_be = self._base_endpoint
        endpoint_should_be += "/%d" % self.random_id

        endpoint_to_check = self.test_class.get_pinned_certificate_by_id(
            self.random_id, self.random_id)

        self.assert_parameters(endpoint_should_be, endpoint_to_check)
