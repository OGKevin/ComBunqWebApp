import unittest

from apiwrapper.endpoints.share_invite_bank_inquiry import \
    ShareInviteBankInquiry
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class ShareInviteBankInquiryTest(EndpointTest, unittest.TestCase):
    def setUp(self):
        super().setUp(ShareInviteBankInquiry)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/user/%d/monetary-account/%d/share-invite-bank" \
                             "-inquiry" % (
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_base_endpoint(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_all_share_invite_bank_inquiries(self):
        endpoint_should_be = "/user/%d/monetary-account/%d/share-invite-bank" \
                             "-inquiry" % (
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_all_share_invite_bank_inquiries(
            self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_share_invite_bank_inquiry_by_id(self):
        endpoint_should_be = "/user/%d/monetary-account/%d/share-invite-bank" \
                             "-inquiry/%d" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_share_invite_bank_inquiry_by_id(
            self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)
