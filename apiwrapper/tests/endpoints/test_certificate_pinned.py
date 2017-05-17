import unittest

from apiwrapper.endpoints.certificate_pinned import CertificatePinned
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class MonetaryAccountTest(EndpointTest, unittest.TestCase):

    def setUp(self):
        super().setUp(CertificatePinned)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/user/%d/certificate-pinned" % (
            self.random_id
        )
        endpoint_to_check = self.test_class.get_base_endpoint(
            self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_pinned_certificates_for_user(self):
        endpoint_should_be = "/user/%d/certificate-pinned" % (
            self.random_id
        )
        endpoint_to_check = self.test_class.get_all_pinned_certificates_for_user(
            self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_pinned_certificate_by_id(self):
        endpoint_should_be = "/user/%d/certificate-pinned/%d" % (
            self.random_id,
            self.random_id
        )
        endpoint_to_check = self.test_class.get_pinned_certificate_by_id(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)
