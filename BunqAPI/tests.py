from django.test import TestCase
from BunqAPI.installation import Installation
from BunqAPI.callbacks import callback
from faker import Faker
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.core import signing
import requests_mock
from pprint import pprint
from unittest.mock import patch
import json
import re


def make_get_request(endpoint, verify):
    # verify = False
    # res = self._api_client.get(endpoint, verify)
    # if res.status_code is not 200:
    #     logger.error(res.json()['Error'][0]['error_description'])
    return endpoint


@requests_mock.Mocker(real_http=False)
@patch('apiwrapper.endpoints.endpoint.Endpoint._make_get_request',
       side_effect=make_get_request)
class TestCode(TestCase):

    fake = Faker()
    installation = re.compile('/v1/installation')
    device_server = re.compile('/v1/device-server')
    attachemt_pubilc = re.compile('/v1/attachment-public/')
    session_server = re.compile('/v1/session-server')
    accounts = re.compile('/monetary-account')
    payment = re.compile('/payments')

    @requests_mock.Mocker(real_http=False)
    def setUp(self, mock):
        mock.register_uri(requests_mock.ANY, self.installation,
                          json=self.get_installation)
        mock.register_uri(requests_mock.ANY, self.device_server)

        username = self.fake.name()
        self.password = self.fake.password()
        self.user = User.objects.create_user(username=username,
                                             password=self.password,
                                             email=None)
        i = Installation(user=self.user, api_key=self.fake.sha1(),
                         password=self.password)
        i.status
        key = self.user.tokens.file_token
        file_path = SessionStore(session_key=key)['file_path']
        with open(file_path, 'r') as f:
            file_contents = f.read()
        self.store_in_session(data=file_contents)

    def test_installation(self, mock, make_get):
        mock.register_uri(requests_mock.ANY, self.installation,
                          json=self.get_installation)
        mock.register_uri(requests_mock.ANY, self.device_server)
        i = Installation(user=self.user, api_key=self.fake.sha1(),
                         password=self.password)

        self.assertTrue(i.status)

    def test_load_file(self, mock, make_get):
        mock.register_uri(requests_mock.ANY, self.installation,
                          json=self.get_installation)
        mock.register_uri(requests_mock.ANY, self.attachemt_pubilc,
                          content=self.get_avatar)
        mock.register_uri(requests_mock.ANY, self.session_server,
                          json=self.get_start_session)
        mock.register_uri(requests_mock.ANY, self.accounts,
                          json=self.get_accounts)
        mock.register_uri(requests_mock.ANY, self.payment,
                          json=self.get_payments)

        c = callback(user=self.user)
        c.load_file()  # NOTE: need to find an assertion for this.
        # assertEqual doesnt do the job due to the order
        # of the JSON's

    def store_in_session(self, data):
        data = json.loads(data)

        try:
            dec_data = signing.loads(data['secret'], key=self.password)
        except signing.BadSignature:
            return False

        enc_data = signing.dumps(dec_data)

        s = SessionStore()
        s['api_data'] = enc_data
        s.create()
        self.user.session.session_token = s.session_key
        self.user.save()

    @property
    def get_installation(self):
        with open('BunqAPI/test_files/installation.json', 'r') as f:
            return json.loads(f.read())

    @property
    def get_start_session(self):
        with open('BunqAPI/test_files/start_session.json', 'r') as f:
            return json.loads(f.read())

    @property
    def get_accounts(self):
        with open('BunqAPI/test_files/accounts.json', 'r') as f:
            return json.loads(f.read())

    @property
    def get_payments(self):
        with open('BunqAPI/test_files/payments.json') as f:
            return json.loads(f.read())

    @property
    def get_avatar(self):
        with open('BunqAPI/test_files/avatar.txt', 'rb') as f:
            return f.read()

    @property
    def get_laod_file(self):
        with open('BunqAPI/test_files/load_file.json', 'r') as f:
            return json.loads(f.read())
