from django.test import TestCase
from .installation import installation
from django.contrib.auth.models import User
from .encryption import AESCipher
from pprint import pprint
import json


# Create your tests here.

class testScript(TestCase):
    """docstring for testScript.
    This test is supposed to test the scipts."""
    def setUp(self):
        user = User.objects.create_user('test', '', 'password')
        user.save()

    def test_installation(self):
        decryt = AESCipher('password')
        encryt = json.loads(installation(
            'test', 'password', 'API_KEY').encrypt())
        d = AESCipher.decrypt(decryt, encryt['secret'])
        pprint(d)

    def test_installation_error1(self):
        decryt = AESCipher('wrong password')
        encryt = json.loads(installation(
            'test', 'password', 'API_KEY').encrypt())
        d = AESCipher.decrypt(decryt, encryt['secret'])
        pprint(d)

    def test_installation_error2(self):
        decryt = AESCipher('password')
        encryt = json.loads(installation(
            'test', 'password', 'API_KEY').encrypt())
        secret = encryt['secret'] = 'destroyed'
        d = AESCipher.decrypt(decryt, secret)
        pprint(d)


class testView(TestCase):
    """docstring for testView.
    This test is supposed to test the views."""
    def test_generate(self):
        response = self.client.get('/generate', follow=True)
        self.assertEqual(response.status_code, 200)

        response2 = self.client.post('/generate', follow=True)
        self.assertEqual(response2.status_code, 200)
