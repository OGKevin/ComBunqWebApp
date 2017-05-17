from django.test import TestCase
from BunqAPI.installation import installation
from django.contrib.auth.models import User
from BunqAPI.encryption import AESCipher
# from .callbacks import callback
from pprint import pprint
import json
import base64
# from django_otp import decorators

# from .pythonBunq.bunq import API


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
        pprint(d)

    def installation_error1(self):
        decryt = AESCipher('wrong password')
        encryt = json.loads(installation(
            'test', 'password', 'API_KEY').encrypt())
        try:
            AESCipher.decrypt(decryt, encryt['secret'])
        except UnicodeDecodeError:
            print('wrong password')

    def installation_error2(self):
        decryt = AESCipher('password')
        encryt = json.loads(installation(
            'test', 'password', 'API_KEY').encrypt())
        secret = encryt['secret'] = 'destroyed'
        try:
            AESCipher.decrypt(decryt, secret)
        except base64.binascii.Error:
            print('secret might be corrupt')

    def GUIDs(self):
        guid = User.objects.get(username='test').profile.GUID
        print('this should be guid\n\n', guid)
        print(type(guid))

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
