from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from filecreator.creator import Creator
from faker import Faker
import json
import os

# Create your tests here.


class TestCode(TestCase):

    fake = Faker()

    def setUp(self):
        self.user = User.objects.create_user(username=self.fake.name(),
                                             password=self.fake.password())

    def delete_file(self):
        key = self.user.tokens.file_token
        file_path = SessionStore(session_key=key)['file_path']

        os.remove(file_path)

    def test_payment(self):
        c = Creator(user=self.user, extension='pdf')
        data = self.get_payment['Response'][0]
        c.payment(data=data)

        self.delete_file()

    def test_transactions(self):
        c = Creator(user=self.user, extension='csv')
        data = self.get_transactions
        c.transactions(data=data)

        self.delete_file()

    def test_avatar(self):
        c = Creator(user=self.user)
        data = self.get_avatar
        c.avatar(data=data)

        self.delete_file()

    @property
    def get_payment(self):
        with open('BunqAPI/test_files/payments.json', 'r') as f:
            return json.loads(f.read())

    @property
    def get_transactions(self):
        with open('filecreator/test_files/transactions_csv.json', 'r') as f:
            return json.loads(f.read())

    @property
    def get_avatar(self):
        with open('BunqAPI/test_files/avatar.txt', 'rb') as f:
            return f.read()
