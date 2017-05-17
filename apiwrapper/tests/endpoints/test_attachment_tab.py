import unittest

from apiwrapper.endpoints.attachment_tab import AttachmentTab
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class AttachmentTabTest(EndpointTest, unittest.TestCase):
    def setUp(self):
        super().setUp(AttachmentTab)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/attachment-tab/%d" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_base_endpoint(
            self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_attachment_tab_by_id(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/attachment-tab/%d" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_attachment_tab_by_id(
            self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_attachment_content(self):
        endpoint_should_be = "/user/%d/monetary-account/%d" \
                             "/attachment-tab/%d/content" % (
                                 self.random_id,
                                 self.random_id,
                                 self.random_id
                             )
        endpoint_to_check = self.test_class.get_attachment_content(
            self.random_id, self.random_id, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)
