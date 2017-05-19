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

# Create your tests here.


class testScript(TestCase):
    """docstring for testScript.
    This test is supposed to test the scipts."""

    def setUp(self):
        fake = Faker()
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
