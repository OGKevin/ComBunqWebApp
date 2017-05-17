import random
import uuid
from unittest.case import TestCase
from unittest.mock import MagicMock

from apiwrapper.clients.api_client import ApiClient


class EndpointTest(TestCase):

    def setUp(self, testing_class):
        self.api_client = ApiClient(str(uuid.uuid4()))
        self.test_class = testing_class(self.api_client)
        self.test_class._make_get_request = MagicMock(
            side_effect=self.side_effect_get)
        self.test_class._make_post_request = MagicMock(
            side_effect=self.side_effect_post)
        self.random_id = random.randint(1, 10000)
        self.random_uuid = uuid.uuid4()

    def side_effect_get(self, endpoint):
        return endpoint

    def side_effect_post(self, endpoint, payload):
        return endpoint, payload

    def assert_parameters(self, should, check):
        assert (check == should), \
            self.print_assertion_error(should, check)

    def print_assertion_error(self, should, was):
        return "Should be: %s but was: %s" % (should, was)
