from django.test import TestCase
from BunqAPI.installation import Installation
from BunqAPI.callbacks import callback
from faker import Faker
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
import requests_mock
from BunqWebApp.views import LogInView
# from unittest.mock import patch
import json


@requests_mock.Mocker(real_http=True)
class TestCode(TestCase):

    fake = Faker()

    @requests_mock.Mocker(real_http=True)
    def setUp(self, mock):
        mock.register_uri(requests_mock.ANY, '/v1/device-server')

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
        LogInView().store_in_session(username=username, password=self.password,
                         data=file_contents)

    def test_installation(self, mock):
        mock.register_uri(requests_mock.ANY, '/v1/device-server')
        i = Installation(user=self.user, api_key=self.fake.sha1(),
                         password=self.password)

        self.assertTrue(i.status)

    def test_load_file(self, mock):
        mock.register_uri(requests_mock.ANY, '/v1/session-server',
                          json=self.get_start_session)
        mock.register_uri(requests_mock.ANY, '/monetary-account',
                          json=self.get_accounts)
        mock.register_uri(requests_mock.ANY, '/payment',
                          json=self.get_payments)

        c = callback(user=self.user)
        print(c.load_file())

    @staticmethod
    def get_start_session():
        with open('BunqAPI/test_files/start_session.json', 'r') as f:
            return json.loads(f.read())

    @staticmethod
    def get_accounts():
        with open('BunqAPI/test_files/accounts.json', 'r') as f:
            return json.loads(f.read())

    @staticmethod
    def get_payments():
        with open('BunqAPI/test_files/payments.json') as f:
            return json.loads(f.read())
