from django.test import TestCase, Client
from django.contrib.auth.models import User
from BunqWebApp import validator
from django.core.exceptions import ValidationError
from BunqWebApp import forms
from faker import Faker


class Validation(TestCase):
    """docstring for Validation.
    Tests the registration validator
    """
    def setUp(self):
        user = User.objects.create_user('more life', 'no email', 'life more')  # noqa
        self.username = user.username

    def test_check_username(self):
        self.assertRaises(
            ValidationError,
            validator.checkUsername,
            self.username
        )


class Views(TestCase):
    """docstring for Views.
    This test will test the views.
    """

    def test_home(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        response = self.client.get('/account/register', follow=True)
        self.assertEqual(response.status_code, 200)

        c = Client()
        form = {
                'username': 'Get Down.',
                'password': 'testtesttesttest',
                'confirm_password': 'testtesttesttest'
        }

        response2 = c.post(
            '/account/register/', form, follow=True)
        self.assertEqual(response2.status_code, 200)


class Forms(TestCase):
    """docstring for Froms.
    This will test the forms
    """

    fake = Faker()

    def test_registration(self):
        password = self.fake.password()

        form_data = {
            'username': self.fake.name(),
            'password': password,
            'confirm_password': password,
            'api_key': self.fake.sha1()
        }
        form_data2 = {
            'username': self.fake.name(),
            'password': self.fake.password(),
            'confirm_password': self.fake.password(),
            'api_key': self.fake.sha1()
        }
        form = forms.registration(data=form_data)
        form2 = forms.registration(data=form_data2)
        self.assertTrue(form.is_valid())
        self.assertFalse(form2.is_valid())
