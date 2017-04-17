from django.test import TestCase
from django.core.management import call_command
# import json
from .models import catagories
# from .master import sortInfo
# from collections import OrderedDict
# Create your tests here.


class DatabaseInputTest(TestCase):
    """docstring for NewMasterTest."""

    def test_command_output(self):
        call_command('InputDataInDataBase',)


class TestPageAccess(TestCase):
    """docstring for TestPageAccess."""

    def test_HomePage(self):
        response = self.client.get('/')
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
        json = (
            '[{"Datum":"2017-03-31","Bedrag":"-0,01","Rekening":"NL01BUNQ12345'
            '67890","Tegenrekening":"NL48ABNA0502830042","Naam":"test by Ad'
            'yen","Omschrijving":"Payment description"},{"Datum":"2017-03-31"'
            ',"Bedrag":"1,64","Rekening":"NL01BUNQ1234567990","Tegenrekening"'
            ':"NL01BUNQ1234567890","Naam":"bunq","Omschrijving":"Slice heeft'
            ' deze request verstuurd voor de groep Family."}]'
        )
        response2 = self.client.post('/Manager/', {'json': json})
        self.assertEqual(response2.status_code, 200,)

    def test_googleForm(self):
        response = self.client.get('/Manager/googleForm')
        self.assertEqual(response.status_code, 200)


# class testScript(TestCase):
#     def test_Manager(self):
#         trans = [
#             {
#                 "Tegenrekening": "DE60700111100250250061",
#                 "Bedrag": "0,01",
#             }, {
#                 "Tegenrekening": "NL03BUNQ2025449445",
#                 "Bedrag": "24,09",
#             }, {
#                 "Tegenrekening": "NL90INGB0006080785",
#                 "Bedrag": "202,30",
#             }, {
#                 "Tegenrekening": "NL21INGB0674773837",
#                 "Bedrag": "-53,00",
#             }, {
#                 "Tegenrekening": "NL03BUNQ2025449445",
#                 "Bedrag": "50,00"
#             }
#         ]
#         shouldBeReturned = {
#             'catagories': [
#                 ('Gorrila',
#                  202.3),
#                 ('Aliexpres',
#                  0.01),
#                 ('Requests',
#                  74.09),
#                 ('Other',
#                  -53.0),
#             ],
#             'transactions': [
#                 {
#                     'Tegenrekening': 'DE60700111100250250061',
#                     'Bedrag': '0,01',
#                     'Catagory': 'Aliexpres'
#                 },
#                 {
#                     'Tegenrekening': 'NL03BUNQ2025449445',
#                     'Bedrag': '24,09',
#                     'Catagory': 'Requests'
#                 },
#                 {
#                     'Tegenrekening': 'NL90INGB0006080785',
#                     'Bedrag': '202,30',
#                     'Catagory': 'Gorrila'
#                 },
#                 {
#                     'Tegenrekening': 'NL21INGB0674773837',
#                     'Bedrag': '-53,00',
#                     'Catagory': 'Other'
#                 },
#                 {
#                     'Tegenrekening': 'NL03BUNQ2025449445',
#                     'Bedrag': '50,00',
#                     'Catagory': 'Requests'
#                 }
#             ],
#         }
#         # NOTE: NewModel
#         catagories.objects.create(
#             Naam='Aliexpres', Rekening=['DE60700111100250250061'])
#         catagories.objects.create(
#             Naam='Gorrila', Rekening=['NL90INGB0006080785'])
#         catagories.objects.create(
#             Naam='Requests', Rekening=['NL03BUNQ2025449445'])
#         print(sortInfo(json.loads(json.dumps(trans),
#                                   object_pairs_hook=OrderedDict)) == shouldBeReturned)
#         # NOTE: this returns false.... the sorting is messing it up
