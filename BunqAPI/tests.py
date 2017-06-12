from django.test import TestCase, RequestFactory
from BunqAPI.installation import Installation
from BunqAPI.callbacks import callback
from BunqAPI import views
from faker import Faker
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.core import signing
import requests_mock
import requests
# from pprint import pprint
# from apiwrapper.clients.api_client
from unittest.mock import patch
import json
import re
import os


def make_get_request(endpoint, verify=False):
    url = 'https://sandbox.public.api.bunq.com/v1'
    return requests.get(url=url + endpoint)


@requests_mock.Mocker(real_http=False)
@patch('apiwrapper.endpoints.endpoint.Endpoint._make_get_request',
       side_effect=make_get_request)
class TestCode(TestCase):

    fake = Faker()
    installation = re.compile('/v1/installation')
    device_server = re.compile('/v1/device-server')
    attachemt_pubilc = re.compile('/v1/attachment-public/')
    session_server = re.compile('/v1/session-server')
    session = re.compile('/session/')
    accounts = re.compile('/monetary-account')
    payment = re.compile('/payments')
    users = re.compile('/user')
    card = re.compile('/card')
    invoice = re.compile('/invoice')
    invoice_api = re.compile('https://api.sycade.com/btp-int/Invoice/Generate')
    customer_statement = re.compile('/customer-statement')

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

        self.c = callback(self.user)

        os.remove(file_path)

    def test_installation(self, mock, _):
        mock.register_uri(requests_mock.ANY, self.installation,
                          json=self.get_installation)
        mock.register_uri(requests_mock.ANY, self.device_server)
        i = Installation(user=self.user, api_key=self.fake.sha1(),
                         password=self.password)

        self.assertTrue(i.status)

    def test_load_file(self, mock, _):
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

        # c = callback(user=self.user)
        self.c.load_file()
        self.c.account_id = self.fake.random_number()
        self.c.payment_id = self.fake.random_number()
        self.c.load_file()  # NOTE: need to find an assertion for this.
        # assertEqual doesnt do the job due to the order
        # of the JSON's

    def test_delete_session(self, mock, _):
        mock.register_uri(requests_mock.ANY, self.attachemt_pubilc,
                          content=self.get_avatar)
        mock.register_uri(requests_mock.ANY, self.session_server,
                          json=self.get_start_session)
        mock.register_uri(requests_mock.ANY, self.session)

        self.c.start_session()
        self.assertTrue(self.c.delete_session())

    def test_users(self, mock, _):
        mock.register_uri(requests_mock.ANY, self.users,
                          json=self.get_users)
        mock.register_uri(requests_mock.ANY, self.attachemt_pubilc,
                          content=self.get_avatar)
        # c = callback(user=self.user)
        self.c.users()
        self.c.user_id = self.fake.random_number()
        self.c.users()

    def test_card(self, mock, _):
        mock.register_uri(requests_mock.ANY, self.card,
                          json=self.get_card)

        # c = callback(user=self.user)
        self.c.user_id = self.fake.random_number()
        self.c.card()
        self.c.account_id = self.fake.random_number()
        self.c.card()

    def test_invoice(self, mock, _):
        mock.register_uri(requests_mock.ANY, self.invoice,
                          json=self.get_invoice_data)
        mock.register_uri(requests_mock.ANY, self.invoice_api,
                          text=self.get_invoice_pdf)

        self.c.user_id = self.fake.random_number()
        self.c.invoice()

    def test_payment_pdf(self, mock, _):
        mock.register_uri(requests_mock.ANY, self.payment,
                          json=self.get_payments)

        self.c.payment_id = self.fake.random_number()
        self.c.get_payment_pdf()

    def test_cusomer_statement_pdf(self, mock, _):
        mock.register_uri(requests_mock.ANY, self.customer_statement,
                          json=self.get_customer_statment)

        self.c.user_id = self.fake.random_number()
        self.c.account_id = self.fake.random_number()
        self.c.date_start = self.fake.date()
        self.c.date_end = self.fake.date()
        self.c.statement_format = 'PDF'

        self.c.customer_statement()

    def test_cusomer_statement_csv(self, mock, _):
        mock.register_uri(requests_mock.ANY, self.customer_statement,
                          json=self.get_customer_statment)

        self.c.user_id = self.fake.random_number()
        self.c.account_id = self.fake.random_number()
        self.c.date_start = self.fake.date()
        self.c.date_end = self.fake.date()
        self.c.statement_format = 'CSV'

        self.c.customer_statement()

    def test_cusomer_statement_mt940(self, mock, _):
        mock.register_uri(requests_mock.ANY, self.customer_statement,
                          json=self.get_customer_statment)

        self.c.user_id = self.fake.random_number()
        self.c.account_id = self.fake.random_number()
        self.c.date_start = self.fake.date()
        self.c.date_end = self.fake.date()
        self.c.statement_format = 'MT940'

        self.c.customer_statement()

    def store_in_session(self, data):
        data = json.loads(data)

        dec_data = signing.loads(data['secret'], key=self.password)

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
    def get_users(self):
        with open('BunqAPI/test_files/users.json', 'r') as f:
            return json.loads(f.read())

    @property
    def get_card(self):
        with open('BunqAPI/test_files/card.json', 'r') as f:
            return json.loads(f.read())

    @property
    def get_invoice_data(self):
        with open('BunqAPI/test_files/invoice.json', 'r') as f:
            return json.loads(f.read())

    @property
    def get_invoice_pdf(self):
        with open('BunqAPI/test_files/invoice.txt', 'r') as f:
            return f.read()

    @property
    def get_customer_statment(self):
        with open('BunqAPI/test_files/customer_statement.json', 'r') as f:
            return json.loads(f.read())


class TestViews(TestCase):

    def test_my_bunq_view(self):
        r = self.client.get('/my_bunq')
        self.assertEqual(r.status_code, 301)

    def test_generate_view(self):
        r = self.client.get('/generate')
        self.assertEqual(r.status_code, 301)


# @requests_mock.Mocker(real_http=False)
# @patch('apiwrapper.endpoints.endpoint.Endpoint._make_get_request',
#        side_effect=make_get_request)
class TestViewCode(TestCase):

    fake = Faker()
    installation = re.compile('/v1/installation')
    device_server = re.compile('/v1/device-server')
    attachemt_pubilc = re.compile('/v1/attachment-public/')
    session_server = re.compile('/v1/session-server')
    session = re.compile('/session/')
    accounts = re.compile('/monetary-account')
    payment = re.compile('/payments')
    users = re.compile('/user')
    card = re.compile('/card')
    invoice = re.compile('/invoice')
    invoice_api = re.compile('https://api.sycade.com/btp-int/Invoice/Generate')
    customer_statement = re.compile('/customer-statement')

    # @requests_mock.Mocker(real_http=False)
    def setUp(self):
        # mock.register_uri(requests_mock.ANY, self.installation,
        #                   json=self.get_installation)
        # mock.register_uri(requests_mock.ANY, self.device_server)
        self.request = RequestFactory()
        self.password = self.fake.password()
        self.user = User.objects.create_user(username=self.fake.name(),
                                             password=self.password)

    #     i = Installation(user=self.user, api_key=self.fake.sha1(),
    #                      password=self.password)
    #     i.status
    #     key = self.user.tokens.file_token
    #     file_path = SessionStore(session_key=key)['file_path']
    #     with open(file_path, 'r') as f:
    #         file_contents = f.read()
    #     self.store_in_session(data=file_contents)
    #
    #     # self.c = callback(self.user)
    #
    #     os.remove(file_path)
    #
    # def store_in_session(self, data):
    #     data = json.loads(data)
    #
    #     dec_data = signing.loads(data['secret'], key=self.password)
    #
    #     enc_data = signing.dumps(dec_data)
    #
    #     s = SessionStore()
    #     s['api_data'] = enc_data
    #     s.create()
    #     self.user.session.session_token = s.session_key
    #     self.user.save()

    def test_my_bunq_view(self):
        request = self.request.get(path='/my_bunq')
        request.user = self.user
        request.session = {}

        self.client.login(username=self.user.username, password=self.password)

        response = views.MyBunqView.as_view()(request)
        self.assertEqual(response.status_code, 403)
