from django.test import TestCase, RequestFactory
from BunqAPI.installation import installation
from django.contrib.auth.models import User
from BunqAPI.encryption import AESCipher
import json
import base64
from BunqAPI import views
from django.contrib.auth import authenticate
from faker import Faker
# from pprint import pprint
from unittest.mock import patch
from BunqAPI.models import Proxy
# Create your tests here.


class testScript(TestCase):
    """docstring for testScript.
    This test is supposed to test the scipts."""

    def setUp(self):
        fake = Faker()
        Proxy.objects.create(proxy_uri='')
        self.username = fake.name()
        self.password = fake.password(
            length=10,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True)
        user = User.objects.create_user(self.username, '', self.password)
        user.save()

    def installation(self):
        decryt = AESCipher(self.password)
        encryt = json.loads(installation(
            self.username, self.password, 'API_KEY').encrypt())
        d = AESCipher.decrypt(decryt, encryt['secret'])
        self.assertIs(len(d), 4)
        self.assertTrue(isinstance(d, dict))

    def installation_error1(self):
        decryt = AESCipher('wrong password')
        encryt = json.loads(installation(
            self.username, self.password, 'API_KEY').encrypt())
        self.assertRaises(
            UnicodeDecodeError,
            AESCipher.decrypt,
            decryt, encryt['secret']
        )

    def installation_error2(self):
        decryt = AESCipher(self.password)
        encryt = json.loads(installation(
            self.username, self.password, 'API_KEY').encrypt())
        secret = encryt['secret'] = 'destroyed'
        self.assertRaises(
            base64.binascii.Error,
            AESCipher.decrypt,
            decryt, secret
        )

    def GUIDs(self):
        guid = User.objects.get(username=self.username).profile.GUID
        self.assertTrue(isinstance(guid, list))

    def test_run(self):
        self.installation()
        self.installation_error1()
        self.installation_error2()
        self.GUIDs()


class testView(TestCase):
    """docstring for testView.
    This test is supposed to test the views.
    Need to find a way to simulate logged in with 2FA

    """

    def setUp(self):
        Proxy.objects.create(proxy_uri='')

    def test_generate(self):
        response = self.client.get('/generate', follow=True)
        self.assertEqual(response.status_code, 200)

        response2 = self.client.post('/generate', follow=True)
        self.assertEqual(response2.status_code, 200)

    def test_decrypt(self):
        response = self.client.get('/decrypt', follow=True)
        self.assertEqual(response.status_code, 200)

        response2 = self.client.post('/decrypt', follow=True)
        self.assertEqual(response2.status_code, 200)

    def test_api(self):
        response = self.client.post('/API/register', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_invoice_downloader(self):
        response = self.client.get('/decrypt/invoice', follow=True)
        self.assertEqual(response.status_code, 200)


class TestViewCode(TestCase):
    """docstring for TestViewCode."""

    def setUp(self):
        fake = Faker()
        Proxy.objects.create(proxy_uri='')
        name = fake.name()
        pas = fake.password(
            length=10,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True
        )
        User.objects.create_user(name, '', pas)
        self.user = authenticate(username=name, password=pas)
        self.user.is_verified = lambda: True
        self.factory = RequestFactory()

    def test_generate_get(self):
        request = self.factory.get('/generate')
        request.user = self.user
        self.assertEqual(
            views.generate(request).status_code,
            200
        )

    def test_decrypt_get(self):
        request = self.factory.get('/decrypt')
        request.user = self.user
        self.assertEqual(
            views.decrypt(request).status_code,
            200
        )

    def test_generate_post(self):
        data = {
            'API': Faker().sha256(raw_output=False),
            'encryption_password': Faker().password(
                length=10,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True
            ),
        }
        request = self.factory.post('/generate', data=data)
        request.user = self.user

        self.assertEqual(
            views.generate(request).status_code,
            200
        )

    def test_decrypt_post(self):
        data = {
            'Nothing': 'Nothing',
        }
        request = self.factory.post('/decrypt', data=data)
        request.user = self.user

        self.assertEqual(
            views.decrypt(request).status_code,
            200
        )


class TestCallback(TestCase):
    """docstring for TestCallback."""
    c = 'apiwrapper.endpoints.'

    def setUp(self):
        fake = Faker()
        Proxy.objects.create(proxy_uri='')
        username = fake.name()
        password = fake.password()
        User.objects.create_user(username, '', password)
        encryption_password = fake.password()
        data = installation(
            username,
            encryption_password,
            fake.sha1()
        ).encrypt()
        self.id = fake.random_number()
        self.factory = RequestFactory()
        self.user = authenticate(username=username, password=password)
        self.user.is_verified = lambda: True

        self.post_data = {
            'json': data,
            'pass': encryption_password,
        }

    def get_inoice(a):
        f = open('BunqAPI/test_files/invoice.json', 'r')
        return json.loads(f.read())

    def get_start_session():
        f = open('BunqAPI/test_files/start_session.json', 'r')
        return json.loads(f.read())

    def get_user():
        f = open('BunqAPI/test_files/users.json', 'r')
        return json.loads(f.read())

    def get_accounts(a):
        f = open('BunqAPI/test_files/accounts.json', 'r')
        return json.loads(f.read())

    def get_payment(a, b):
        f = open('BunqAPI/test_files/payments.json')
        return json.loads(f.read())

    def get_card(a):
        f = open('BunqAPI/test_files/card.json')
        return json.loads(f.read())

    @patch('%ssession_server.SessionServer.create_new_session_server' % c, side_effect=get_start_session)  # noqa
    def test_start_session(self, mock):
        request = self.factory.post('/API/start_session', data=self.post_data)
        request.user = self.user
        r = views.API(request, 'start_session')
        self.assertEqual(r.status_code, 200)

    @patch('%ssession_server.SessionServer.create_new_session_server' % c, side_effect=get_start_session)  # noqa
    @patch('%suser.User.get_logged_in_user' % c, side_effect=get_user)
    def test_users(self, mock, mock2):
        user = self.user
        data = self.post_data

        request1 = self.factory.post('/API/start_session', data=data)
        request1.user = user
        views.API(request1, 'start_session')

        request2 = self.factory.post('/API/users', data=data)
        request2.user = user
        r2 = views.API(request2, 'users')

        self.assertEqual(r2.status_code, 200)

    @patch('%ssession_server.SessionServer.create_new_session_server' % c, side_effect=get_start_session)  # noqa
    @patch('%smonetary_account.MonetaryAccount.get_all_accounts_for_user' % c, side_effect=get_accounts)  # noqa
    def test_accounts(self, mock, mock2):
        user = self.user
        data = self.post_data

        request1 = self.factory.post('/API/start_session', data=data)
        request1.user = user
        views.API(request1, 'start_session')

        request2 = self.factory.post('/API/accounts', data=data)
        request2.user = user
        r2 = views.API(request2, 'accounts', self.id)

        self.assertEqual(r2.status_code, 200)

    @patch('%ssession_server.SessionServer.create_new_session_server' % c, side_effect=get_start_session)  # noqa
    @patch('%spayment.Payment.get_all_payments_for_account' % c, side_effect=get_payment)  # noqa
    def test_payment(self, mock, mock2):
        user = self.user
        data = self.post_data

        request1 = self.factory.post('/API/start_session', data=data)
        request1.user = user
        views.API(request1, 'start_session')

        request2 = self.factory.post('/API/payment', data=data)
        request2.user = user
        r2 = views.API(request2, 'payment', self.id, self.id)

        self.assertEqual(r2.status_code, 200)

    @patch('%ssession_server.SessionServer.create_new_session_server' % c, side_effect=get_start_session)  # noqa
    @patch('%sinvoice.Invoice.get_all_invoices_for_user' % c, side_effect=get_inoice)  # noqa
    def test_invoice(self, mock, mock2):
        user = self.user
        data = self.post_data

        request1 = self.factory.post('/API/start_session', data=data)
        request1.user = user
        views.API(request1, 'start_session')

        request2 = self.factory.post('/API/invoice', data=data)
        request2.user = user
        r2 = views.API(request2, 'invoice', self.id)

        self.assertEqual(r2.status_code, 200)

    @patch('%ssession_server.SessionServer.create_new_session_server' % c, side_effect=get_start_session)  # noqa
    @patch('%scard.Card.get_all_cards_for_user' % c, side_effect=get_card)  # noqa
    def test_card(self, mock, mock2):
        user = self.user
        data = self.post_data

        request1 = self.factory.post('/API/start_session', data=data)
        request1.user = user
        views.API(request1, 'start_session')

        request2 = self.factory.post('/API/card', data=data)
        request2.user = user
        r2 = views.API(request2, 'card', self.id)

        self.assertEqual(r2.status_code, 200)

    @patch('%ssession_server.SessionServer.create_new_session_server' % c, side_effect=get_start_session)  # noqa
    @patch('%sinvoice.Invoice.get_all_invoices_for_user' % c, side_effect=get_inoice)  # noqa  # noqa
    def test_invoice_downloader(self, mock, mock2):
        user = self.user
        data = self.post_data

        request1 = self.factory.post('/API/start_session', data=data)
        request1.user = user
        views.API(request1, 'start_session')

        request2 = self.factory.post('/API/invoice', data=data)
        request2.user = user
        views.API(request2, 'invoice', self.id)

        request3 = self.factory.get('/decryt/invoice')
        request3.user = user

        r = views.invoice_downloader(request3)
        self.assertEqual(r.status_code, 200)
