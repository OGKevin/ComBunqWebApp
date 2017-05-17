import unittest

from apiwrapper.endpoints.invoice import Invoice
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class InvoiceTest(EndpointTest, unittest.TestCase):
    def setUp(self):
        super().setUp(Invoice)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/invoice" % (
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_base_endpoint(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_invoices_for_account(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/invoice" % (
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_all_invoices_for_account(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_invoice_by_id(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/invoice/%d" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_invoice_by_id(
            self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

