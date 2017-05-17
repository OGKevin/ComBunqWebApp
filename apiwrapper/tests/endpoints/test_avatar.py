import unittest

from apiwrapper.endpoints.avatar import Avatar
from apiwrapper.tests.endpoints.test_endpoint import EndpointTest


class AvatarTest(EndpointTest, unittest.TestCase):

    def setUp(self):
        super().setUp(Avatar)

    def test_get_base_endpoint(self):
        endpoint_should_be = "/avatar/%s" % (
            self.random_uuid
        )
        endpoint_to_check = self.test_class.get_base_endpoint(
            self.random_uuid)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)

    def test_get_avatar_by_id(self):
        endpoint_should_be = "/avatar/%s" % (
            self.random_uuid
        )
        endpoint_to_check = self.test_class.get_avatar_by_id(
            self.random_uuid)
        self.assert_parameters(endpoint_should_be, endpoint_to_check)
