from django.test import TestCase, Client
from django.core.management import call_command
from django.utils.six import StringIO
from models import transactions, catagories
from master import getDate
# Create your tests here.

class DatabaseInputTest(TestCase):
    """docstring for NewMasterTest."""
    def test_command_output(self):
        call_command('InputDataInDataBase',)

class TestPageAccess(TestCase):
    """docstring for TestPageAccess."""
    def setUp(self):
        trans = [
   {
      "Tegenrekening":"NL08SNSB0862762731",
      "Naam":"K. Hellemun",
      "Bedrag":"0,01",
   },
   {
      "Tegenrekening":"NL03BUNQ2025449445",
      "Naam":"bunq",
      "Bedrag":"24,09",
   },
   {
      "Tegenrekening":"NL08SNSB0862762731",
      "Bedrag":"202,30",
   },
   {
      "Tegenrekening":"NL90INGB0006080785",
      "Bedrag":"-94,75",
   }
]
        cat = [
   {
      "Naam":"Aliexpres",
      "Rekening":"DE60700111100250250061"
   },
   {
      "Naam":"Gorilla",
      "Rekening":"NL90INGB0006080785"
   },{
      "Naam":"Other",
      "Rekening":"Geen rekening"
   }
]
        # NOTE: oldModel
        transactions.objects.create(attrs = trans, catagory = cat)
        # NOTE: NewModel
        catagories.objects.create(Naam = 'Aliexpres', Rekening = ['DE60700111100250250061'])
        catagories.objects.create(Naam = 'Gorrila', Rekening = ['NL90INGB0006080785'])
        catagories.objects.create(Naam = 'Requests', Rekening = ['NL03BUNQ2025449445'])


    def test_HomePage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_Manager(self):
        getDate("","",'database')
        
