from django.test import TestCase, RequestFactory
from BunqAPI.installation import installation
from django.contrib.auth.models import User
from BunqAPI.encryption import AESCipher
import json
import base64
from BunqAPI import views
from django.contrib.auth import authenticate
from faker import Faker
from unittest.mock import patch
import requests
import requests_mock
# Create your tests here.


class testScript(TestCase):
    """docstring for testScript.
    This test is supposed to test the scipts."""

    def setUp(self):
        fake = Faker()
        username = fake.name()
        self.password = fake.password(
            length=10,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True)
        self.user = User.objects.create_user(username, '', self.password)
        self.user.save()

    def installation(self):
        decryt = AESCipher(self.password)
        encryt = json.loads(installation(
            self.user, self.password, 'API_KEY').encrypt())
        d = AESCipher.decrypt(decryt, encryt['secret'])
        self.assertIs(len(d), 4)
        self.assertTrue(isinstance(d, dict))

    def installation_error1(self):
        decryt = AESCipher('wrong password')
        encryt = json.loads(installation(
            self.user, self.password, 'API_KEY').encrypt())
        self.assertRaises(
            UnicodeDecodeError,
            AESCipher.decrypt,
            decryt, encryt['secret']
        )

    def installation_error2(self):
        decryt = AESCipher(self.password)
        encryt = json.loads(installation(
            self.user, self.password, 'API_KEY').encrypt())
        secret = encryt['secret'] = 'destroyed'
        self.assertRaises(
            base64.binascii.Error,
            AESCipher.decrypt,
            decryt, secret
        )

    def GUIDs(self):
        guid = self.user.profile.GUID
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

    def test_generate(self):
        response = self.client.get('/generate', follow=True)
        self.assertEqual(response.status_code, 200)

        response2 = self.client.post('/generate', follow=True)
        self.assertEqual(response2.status_code, 200)

    def test_my_bunq(self):
        response = self.client.get('/my_bunq', follow=True)
        self.assertEqual(response.status_code, 200)

        response2 = self.client.post('/my_bunq', follow=True)
        self.assertEqual(response2.status_code, 200)

    def test_api(self):
        response = self.client.post('/API/register', follow=True)
        self.assertEqual(response.status_code, 200)


class TestViewCode(TestCase):
    """docstring for TestViewCode."""

    def setUp(self):
        fake = Faker()
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
            views.GenerateView().get(request).status_code,
            200
        )

    def test_my_bunq_get(self):
        request = self.factory.get('/my_bunq')
        request.user = self.user
        self.assertEqual(
            views.MyBunqView().get(request).status_code,
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
            views.GenerateView().post(request).status_code,
            200
        )


class TestCallback(TestCase):
    """docstring for TestCallback."""
    c = 'apiwrapper.endpoints.'

    def setUp(self):
        fake = Faker()
        username = fake.name()
        password = fake.password()
        user = User.objects.create_user(username, '', password)
        encryption_password = fake.password()
        data = installation(
            user,
            encryption_password,
            fake.sha1()
        ).encrypt()
        user.save()
        self.id = fake.random_number()
        self.factory = RequestFactory()
        self.user = authenticate(username=username, password=password)
        self.user.is_verified = lambda: True

        self.post_data = {
            'json': data,
            'pass': encryption_password,
        }

    @requests_mock.Mocker()
    def get_inoice(a, m):
        f = open('BunqAPI/test_files/invoice.json', 'r')
        m.get('http://fake_url', json=json.loads(f.read()))
        r = requests.get('http://fake_url')
        return r

    @requests_mock.Mocker()
    def get_start_session(m):
        f = open('BunqAPI/test_files/start_session.json', 'r')
        m.get('http://fake_url', json=json.loads(f.read()))
        r = requests.get('http://fake_url')
        return r

    @requests_mock.Mocker()
    def get_user(m):
        f = open('BunqAPI/test_files/users.json', 'r')
        m.get('http://fake_url', json=json.loads(f.read()))
        r = requests.get('http://fake_url')
        return r

    @requests_mock.Mocker()
    def get_accounts(a, m):
        f = open('BunqAPI/test_files/accounts.json', 'r')
        m.get('http://fake_url', json=json.loads(f.read()))
        r = requests.get('http://fake_url')
        return r

    @requests_mock.Mocker()
    def get_payment(a, b, m):
        f = open('BunqAPI/test_files/payments.json')
        m.get('http://fake_url', json=json.loads(f.read()))
        r = requests.get('http://fake_url')
        return r

    @requests_mock.Mocker()
    def get_card(a, m):
        f = open('BunqAPI/test_files/card.json')
        m.get('http://fake_url', json=json.loads(f.read()))
        r = requests.get('http://fake_url')
        return r

    @requests_mock.Mocker()
    def get_avatar(a, m):
        f = open('BunqAPI/test_files/avatar.txt')
        m.get('http://fake_url', json=f.read())
        r = requests.get('http://fake_url')
        return r

    @patch('%ssession_server.SessionServer.create_new_session_server' % c, side_effect=get_start_session)  # noqa
    @patch('%sattachment_public.AttachmentPublic.get_content_of_public_attachment' % c, side_effect=get_avatar)  # noqa
    def test_start_session(self, mock, mock3):
        request = self.factory.post('/API/start_session', data=self.post_data)
        request.user = self.user
        r = views.APIView().post(request, selector='start_session')
        self.assertEqual(r.status_code, 200)

    @patch('%sattachment_public.AttachmentPublic.get_content_of_public_attachment' % c, side_effect=get_avatar)  # noqa
    @patch('%ssession_server.SessionServer.create_new_session_server' % c, side_effect=get_start_session)  # noqa
    @patch('%suser.User.get_logged_in_user' % c, side_effect=get_user)
    def test_users(self, mock, mock2, mock3):
        user = self.user
        data = self.post_data

        request1 = self.factory.post('/API/start_session', data=data)
        request1.user = user
        views.APIView().post(request1, selector='start_session')

        request2 = self.factory.post('/API/users', data=data)
        request2.user = user
        r2 = views.APIView().post(request2, selector='users')

        self.assertEqual(r2.status_code, 200)

    @patch('%ssession_server.SessionServer.create_new_session_server' % c, side_effect=get_start_session)  # noqa
    @patch('%sattachment_public.AttachmentPublic.get_content_of_public_attachment' % c, side_effect=get_avatar)  # noqa
    @patch('%smonetary_account.MonetaryAccount.get_all_accounts_for_user' % c, side_effect=get_accounts)  # noqa
    def test_accounts(self, mock, mock2, mock3):
        user = self.user
        data = self.post_data

        request1 = self.factory.post('/API/start_session', data=data)
        request1.user = user
        views.APIView().post(request1, selector='start_session')

        request2 = self.factory.post('/API/accounts', data=data)
        request2.user = user
        r2 = views.APIView().post(request2, selector='accounts',
                                  user_id=self.id)

        self.assertEqual(r2.status_code, 200)

    @patch('%ssession_server.SessionServer.create_new_session_server' % c, side_effect=get_start_session)  # noqa
    @patch('%spayment.Payment.get_all_payments_for_account' % c, side_effect=get_payment)  # noqa
    @patch('%sattachment_public.AttachmentPublic.get_content_of_public_attachment' % c, side_effect=get_avatar)  # noqa
    def test_payment(self, mock, mock2, mock3):
        user = self.user
        data = self.post_data

        request1 = self.factory.post('/API/start_session', data=data)
        request1.user = user
        views.APIView().post(request1, selector='start_session')

        request2 = self.factory.post('/API/payment', data=data)
        request2.user = user
        r2 = views.APIView().post(request2, selector='payment',
                                  user_id=self.id,
                                  account_id=self.id)

        self.assertEqual(r2.status_code, 200)

    @patch('%ssession_server.SessionServer.create_new_session_server' % c, side_effect=get_start_session)  # noqa
    @patch('%sinvoice.Invoice.get_all_invoices_for_user' % c, side_effect=get_inoice)  # noqa
    @patch('%sattachment_public.AttachmentPublic.get_content_of_public_attachment' % c, side_effect=get_avatar)  # noqa
    def test_invoice(self, mock, mock2, mock3):
        user = self.user
        data = self.post_data
        userID = self.id

        request1 = self.factory.post('/API/start_session', data=data)
        request1.user = user
        views.APIView().post(request1, selector='start_session')

        request2 = self.factory.post('/API/invoice', data=data)
        request2.user = user
        r2 = views.APIView().post(request2, selector='invoice', user_id=userID)

        self.assertEqual(r2.status_code, 200)

    @patch('%ssession_server.SessionServer.create_new_session_server' % c, side_effect=get_start_session)  # noqa
    @patch('%sattachment_public.AttachmentPublic.get_content_of_public_attachment' % c, side_effect=get_avatar)  # noqa
    @patch('%scard.Card.get_all_cards_for_user' % c, side_effect=get_card)  # noqa
    def test_card(self, mock, mock2, mock3):
        user = self.user
        data = self.post_data

        request1 = self.factory.post('/API/start_session', data=data)
        request1.user = user
        views.APIView().post(request1, selector='start_session')

        request2 = self.factory.post('/API/card', data=data)
        request2.user = user
        r2 = views.APIView().post(request2, selector='card',
                                  account_id=self.id)

        self.assertEqual(r2.status_code, 200)
