import unittest

from apiwrapper.endpoints.attachment_public import AttachmentPublic
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class AttachmentPublicTest(EndpointTest, unittest.TestCase):

    def setUp(self):
        super().setUp(AttachmentPublic)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/attachment-public/%s" % self.random_uuid
        endpoint_to_check = self.test_class.get_base_endpoint(self.random_uuid)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_public_attachment_by_id(self):
        endpoint_should_be = "/attachment-public/%s" % self.random_uuid
        endpoint_to_check = self.test_class.get_public_attachment_by_id(
            self.random_uuid)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_content_of_public_attachment(self):
        endpoint_should_be = "/attachment-public/%s/content" % self.random_uuid
        endpoint_to_check = self.test_class.get_content_of_public_attachment(
            self.random_uuid)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)
