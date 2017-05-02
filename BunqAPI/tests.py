from django.test import TestCase
from .installation import createJSON
from django.contrib.auth.models import User
from .encryption import AESCipher
from pprint import pprint
import json


# Create your tests here.


class testScript(TestCase):
    def setUp(self):
        user = User.objects.create_user('test', '', 'password')
        user.save()

    def test_installation(self):
        decryt = AESCipher('password')
        encryt = json.loads(createJSON('test', 'password', 'API_KEY'))
        d = AESCipher.decrypt(decryt, encryt['secret'])
        pprint(d)

    def test_installation_error1(self):
        decryt = AESCipher('wrong password')
        encryt = json.loads(createJSON('test', 'password', 'API_KEY'))
        d = AESCipher.decrypt(decryt, encryt['secret'])
        pprint(d)

    def test_installation_error2(self):
        decryt = AESCipher('password')
        encryt = json.loads(createJSON('test', 'password', 'API_KEY'))
        secret = encryt['secret'] = 'destroyed'
        d = AESCipher.decrypt(decryt, secret)
        pprint(d)


class testView(TestCase):
    """docstring for testView."""
    def test_generate(self):
        response = self.client.get('/generate', follow=True)
        self.assertEqual(response.status_code, 200)

        response2 = self.client.post('/generate', follow=True)
        self.assertEqual(response2.status_code, 200)
