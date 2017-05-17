import unittest

from apiwrapper.endpoints.monetary_account import MonetaryAccount
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class MonetaryAccountTest(EndpointTest, unittest.TestCase):

    def setUp(self):
        super().setUp(MonetaryAccount)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/user/%d/monetary-account" % (
            self.random_id
        )
        endpoint_to_check = self.test_class.get_base_endpoint(
            self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_accounts_for_user(self):
        endpoint_should_be = "/user/%d/monetary-account" % (
            self.random_id
        )
        endpoint_to_check = self.test_class.get_all_accounts_for_user(
            self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_account_by_id(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" % (
            self.random_id,
            self.random_id
        )
        endpoint_to_check = self.test_class.get_account_by_id(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)
