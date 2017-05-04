from django.test import TestCase
from .installation import installation
from django.contrib.auth.models import User
from .encryption import AESCipher
from .callbacks import callback
from pprint import pprint
import json
import jsonpickle
# from .pythonBunq.bunq import API


# Create your tests here.

class callbacks(TestCase):
    """docstring for callbaks.
    This is to test the jsonpickle/jsonpickle/#171.

    Via previous test i could conclude that the API class is the source of the
    issue, therefore I've changed this test to specificly encode the API class.
    This will return in a import error as shown on the issue.
    """
    def setUp(self):
        self.password = '12345'
        self.user = User.objects.create_user('test', '', self.password)
        self.user.save()
        self.f = {'secret': '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'}

    def test_callback(self):
        p = callback(self.f, self.user, self.password)
        print('\n\n', p.bunq_api)
        l = jsonpickle.encode(p.bunq_api)
        print('\n\n', l)
        # NOTE: this raises the error
        k = jsonpickle.decode(l)
        print('\n\n', k)


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
