import random
import uuid
from unittest.case import TestCase
from unittest.mock import MagicMock

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from apiwrapper.clients.api_client import ApiClient


class EndpointTest(TestCase):
    @staticmethod
    def create_random_privkey():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

    random_privkey = create_random_privkey.__func__()

    def setUp(self, testing_class):
        self.api_client = ApiClient(self.random_privkey, str(uuid.uuid4()))
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

    def assert_parameters(self, should, was):
        assert (was == should), \
            "Should be: %s but was: %s" % (should, was)

    @property
    def _base_endpoint(self):
        return None
