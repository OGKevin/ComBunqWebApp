from django.test import TestCase
from BunqAPI.installation import installation
from django.contrib.auth.models import User
from BunqAPI.encryption import AESCipher
import json
import base64
from BunqAPI import views
from django.http import HttpRequest
from django.contrib.auth import authenticate

# Create your tests here.


class testScript(TestCase):
    """docstring for testScript.
    This test is supposed to test the scipts."""
    def setUp(self):
        user = User.objects.create_user('test', '', 'password')
        user.save()

    def installation(self):
        decryt = AESCipher('password')
        encryt = json.loads(installation(
            'test', 'password', 'API_KEY').encrypt())
        d = AESCipher.decrypt(decryt, encryt['secret'])
        self.assertIs(len(d), 4)
        self.assertTrue(isinstance(d, dict))

    def installation_error1(self):
        decryt = AESCipher('wrong password')
        encryt = json.loads(installation(
            'test', 'password', 'API_KEY').encrypt())
        self.assertRaises(
            UnicodeDecodeError,
            AESCipher.decrypt,
            decryt, encryt['secret']
            )

    def installation_error2(self):
        decryt = AESCipher('password')
        encryt = json.loads(installation(
            'test', 'password', 'API_KEY').encrypt())
        secret = encryt['secret'] = 'destroyed'
        self.assertRaises(
            base64.binascii.Error,
            AESCipher.decrypt,
            decryt, secret
        )

    def GUIDs(self):
        guid = User.objects.get(username='test').profile.GUID
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


class TestViewCode(TestCase):
    """docstring for TestViewCode."""

    def setUp(self):
        User.objects.create_user('test', '', 'password')
        self.user = authenticate(username='test', password='password')
        self.user.is_verified = lambda: True
        self.request = HttpRequest
        self.request.META = {}
        self.request.user = self.user

    def test_generate_get(self):
        self.request.method = 'GET'
        self.assertEqual(
            views.generate(self.request).status_code,
            200
        )

    def test_decrypt_get(self):
        self.request.method = 'GET'
        self.assertEqual(
            views.decrypt(self.request).status_code,
            200
        )
