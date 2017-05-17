import unittest

from apiwrapper.endpoints.draft_payment import DraftPayment
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class DraftPaymentTest(EndpointTest, unittest.TestCase):
    def setUp(self):
        super().setUp(DraftPayment)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/draft-payment" % (
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_base_endpoint(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_draft_payments_for_account(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/draft-payment" % (
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_all_draft_payments_for_account(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_draft_payment_by_id(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/draft-payment/%d" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_draft_payment_by_id(
            self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)
