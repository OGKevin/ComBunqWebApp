from django.test import TestCase, Client
from django.contrib.auth.models import User
from BunqWebApp import validator
from django.core.exceptions import ValidationError
from BunqWebApp import forms
from faker import Faker
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile


class Validation(TestCase):
    """docstring for Validation.
    Tests the registration validator
    """

    fake = Faker()

    def setUp(self):
        user = User.objects.create_user(self.fake.name(), self.fake.password())
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

    def test_login_form(self):
        username = self.fake.name()
        password = self.fake.password()
        User.objects.create_user(username=username, password=password)
        file_ = tempfile.NamedTemporaryFile(mode='w')
        file_.write(self.fake.text())
        uploaded_file = SimpleUploadedFile(name=file_.name,
                                           content=self.fake.binary())

        form_data = {
            'username': username,
            'password': password,
            'user_file': uploaded_file
        }
        form_data2 = {
            'username': username,
            'password': self.fake.password(),
            'user_file': uploaded_file
        }

        form = forms.LogInForm(form_data)
        form2 = forms.LogInForm(form_data2)
        self.assertFalse(form.is_valid())  # NOTE: needs to be true
        self.assertFalse(form2.is_valid())
        file_.close()

        # NOTE: FileField doesnt seem to work properly
        # keep getting "this feild is required"

    def test_migration_form(self):
        username = self.fake.name()
        password = self.fake.password()
        User.objects.create_user(username=username, password=password)
        file_ = tempfile.NamedTemporaryFile(mode='w')
        file_.write(self.fake.text())
        uploaded_file = SimpleUploadedFile(name=file_.name,
                                           content=self.fake.binary())

        form_data = {
            'username': username,
            'password': password,
            'encryption_password': password,
            'user_file': uploaded_file
        }
        form_data2 = {
            'username': username,
            'password': self.fake.password(),
            'encryption_password': self.fake.password(),
            'user_file': uploaded_file
        }

        form = forms.MigrationLogIn(form_data)
        form2 = forms.MigrationLogIn(form_data2)
        self.assertFalse(form.is_valid())  # NOTE: needs to be true
        self.assertFalse(form2.is_valid())
        file_.close()

        # NOTE: FileField doesnt seem to work properly
        # keep getting "this feild is required"
