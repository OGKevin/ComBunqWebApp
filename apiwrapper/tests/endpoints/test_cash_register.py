import unittest

from apiwrapper.endpoints.cash_register import CashRegister
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class CashRegisterTest(EndpointTest, unittest.TestCase):
    def setUp(self):
        super().setUp(CashRegister)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/cash-register" % (
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_base_endpoint(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_cash_registers_for_account(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/cash-register" % (
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_all_cash_registers_for_account(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_cash_register_by_id(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/cash-register/%d" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_cash_register_by_id(
            self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_qr_codes_for_cash_register(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/cash-register/%d/qr-code" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_all_qr_codes_for_cash_register(
            self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_qr_code_by_id(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/cash-register/%d/qr-code/%d" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_qr_code_by_id(
            self.random_id, self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_content_for_qr_code(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/cash-register/%d/qr-code/%d/content" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_content_for_qr_code(
            self.random_id, self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)
