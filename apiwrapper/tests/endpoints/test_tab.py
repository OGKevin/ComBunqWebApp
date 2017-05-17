import unittest

from apiwrapper.endpoints.tab import Tab
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class TabTest(EndpointTest, unittest.TestCase):

    def setUp(self):
        super().setUp(Tab)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/tab/%s/attachment/%d" % (
            self.random_uuid,
            self.random_id
        )
        endpoint_to_check = self.test_class.get_base_endpoint(
            self.random_uuid, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_tab_attachment_by_id(self):
        endpoint_should_be = "/tab/%s/attachment/%d" % (
            self.random_uuid,
            self.random_id
        )
        endpoint_to_check = self.test_class.get_tab_attachment_by_id(
            self.random_uuid, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_content_of_tab_attachment(self):
        endpoint_should_be = "/tab/%s/attachment/%d/content" % (
            self.random_uuid,
            self.random_id
        )
        endpoint_to_check = self.test_class.get_content_of_tab_attachment(
            self.random_uuid, self.random_id)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)
