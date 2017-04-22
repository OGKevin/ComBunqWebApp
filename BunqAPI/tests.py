from django.test import TestCase
from .installation import createKey

# Create your tests here.


class testScript(TestCase):
    def test_installation(self):
        createKey()
