import unittest

from apiwrapper.endpoints.share_invite_bank_response import \
    ShareInviteBankResponse
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class ShareInviteBankResponseTest(EndpointTest, unittest.TestCase):

    def setUp(self):
        super().setUp(ShareInviteBankResponse)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/user/%d/share-invite-bank-response" % (
            self.random_id
        )
        endpoint_to_check = self.test_class.get_base_endpoint(
            self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_invite_responses(self):
        endpoint_should_be = "/user/%d/share-invite-bank-response" % (
            self.random_id
        )
        endpoint_to_check = self.test_class.get_all_invite_responses(
            self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_invite_response_by_id(self):
        endpoint_should_be = "/user/%d/share-invite-bank-response/%d" % (
            self.random_id,
            self.random_id
        )
        endpoint_to_check = self.test_class.get_invite_response_by_id(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)
