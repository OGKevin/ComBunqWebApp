from django.test import TestCase, Client
from django.core.management import call_command
from .models import catagories
from .databaseInput import store, addTegenrekening
from .validator import ibanValidator
from django.core.exceptions import ValidationError
from . import master
import json
# Create your tests here.


class DatabaseInputTest(TestCase):
    """docstring for NewMasterTest."""

    def test_command_output(self):
        call_command('InputDataInDataBase',)


class TestPageAccess(TestCase):
    """docstring for TestPageAccess."""

    def test_HomePage(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_ManagerPage(self):
        response = self.client.get('/Manager', follow=True)
        self.assertEqual(response.status_code, 200,)
        catagories.objects.create(
            Naam='Bunq Requests', Rekening=[], regex=['bunq']
        )
        catagories.objects.create(
            Naam='Bunq test', Rekening=['NL48ABNA0502830042'], regex=['test']
        )
        data = (
            '[{"Datum":"2017-03-31","Bedrag":"-0,01","Rekening":"NL01BUNQ12345'
            '67890","Tegenrekening":"NL48ABNA0502830042","Naam":"test by Ad'
            'yen","Omschrijving":"Payment description"},{"Datum":"2017-03-31"'
            ',"Bedrag":"1,64","Rekening":"NL01BUNQ1234567990","Tegenrekening"'
            ':"NL01BUNQ1234567890","Naam":"bunq","Omschrijving":"Slice heeft'
            ' deze request verstuurd voor de groep Family."}]'
        )
        c = Client()
        response2 = c.post('/Manager', {'json': data}, follow=True)
        self.assertEqual(response2.status_code, 200,)

    def test_form(self):
        response = self.client.get('/Manager/form', follow=True)
        self.assertEqual(response.status_code, 200)


class testScript(TestCase):
    def setUp(self):
        catagories.objects.create(
            Naam='Bunq Requests', Rekening=[], regex=[]
        )

    def test_store(self):
        data = {
            'iban': 'GB82WEST12345698765432',
            'category': 'Bunq Requests',
            'keyWord': 'test',
            'captcha': ['9e64410d52317ffc9744b11ef878386a4121c1d6', '']}
        store(data)

    def test_ibanValidator(self):
        ibanValidator('GB82WEST12345698765432')
        self.assertRaises(
            ValidationError,
            ibanValidator,
            'unvalid iban',
        )

    def test_master(self):
        transactions = json.loads('[{"Datum":"2017-03-31","Bedrag":"-0,01","Rekening":"NL01BUNQ1234567890","Tegenrekening":"NL48ABNA0502830042","Naam":"Spotify by Adyen","Omschrijving":"Payment description"},{"Datum":"2017-03-31","Bedrag":"1,64","Rekening":"NL01BUNQ1234567890","Tegenrekening":"NL01BUNQ1234567890","Naam":"bunq","Omschrijving":"Slice heeft deze request verstuurd voor de groep Family."}]') # noqa
        # NOTE: need to add catagories that stored in db
        d = master.sortInfo(transactions)
        self.assertTrue(isinstance(d, dict))
        self.assertIs(len(d), 2)

    def test_addTegenrekening(self):
        data = (
            '[{"Datum":"2017-03-31","Bedrag":"-0,01","Rekening":"NL01BUNQ12345'
            '67890","Tegenrekening":"NL48ABNA0502830042","Naam":"test by Ad'
            'yen","Omschrijving":"Payment description"},{"Datum":"2017-03-31"'
            ',"Bedrag":"1,64","Rekening":"NL01BUNQ1234567990","Tegenrekening"'
            ':"NL01BUNQ1234567890","Naam":"bunq","Omschrijving":"Slice heeft'
            ' deze request verstuurd voor de groep Family."}]'
        )

        d = addTegenrekening(json.loads(data))
        self.assertTrue(isinstance(d, dict))
        self.assertIs(len(d), 2)
