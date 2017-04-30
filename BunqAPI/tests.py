from django.test import TestCase
from .installation import createJSON

# Create your tests here.


class testScript(TestCase):
    def test_installation(self):
        createJSON(None)  # NOTE: need to change this


class testView(TestCase):
    """docstring for testView."""
    def test_generate(self):
        response = self.client.get('/generate')
        self.assertEqual(response.status_code, 200)

        response2 = self.client.post('/generate')
        self.assertEqual(response2.status_code, 200)
