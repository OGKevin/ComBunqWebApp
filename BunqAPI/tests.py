from django.test import TestCase
from .installation import createKey

# Create your tests here.


class testScript(TestCase):
    def test_installation(self):
        createKey()


class testView(TestCase):
    """docstring for testView."""
    def test_generate(self):
        response = self.client.get('/generate')
        self.assertEqual(response.status_code, 200)

        response2 = self.client.post('/generate')
        self.assertEqual(response2.status_code, 200)
