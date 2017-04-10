from django.test import TestCase, Client
from django.core.management import call_command
from django.utils.six import StringIO
from models import  catagories
from master import sortInfo
# Create your tests here.

class DatabaseInputTest(TestCase):
    """docstring for NewMasterTest."""
    def test_command_output(self):
        call_command('InputDataInDataBase',)

class TestPageAccess(TestCase):
    """docstring for TestPageAccess."""
    # def setUp(self):



    def test_HomePage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_ManagerPage(self):
        response = self.client.get('/Manager',follow=True)
        self.assertEqual(response.status_code, 200,)
        
    def test_Manager(self):
        trans = [
   {
      "Tegenrekening":"DE60700111100250250061",
      "Naam":"Kevin",
      "Bedrag":"0,01",
   },
   {
      "Tegenrekening":"NL03BUNQ2025449445",
      "Naam":"bunq",
      "Bedrag":"24,09",
   },
   {
      "Tegenrekening":"NL90INGB0006080785",
      "Bedrag":"202,30",
   },
   {
      "Tegenrekening":"NL21INGB0674773837",
      "Bedrag":"-53,00",
   },
   {
   'Tegenrekening':'NL03BUNQ2025449445',
   'Bedrag': '50,00'
   }
]
        # NOTE: NewModel
        catagories.objects.create(Naam = 'Aliexpres', Rekening = ['DE60700111100250250061'])
        catagories.objects.create(Naam = 'Gorrila', Rekening = ['NL90INGB0006080785'])
        catagories.objects.create(Naam = 'Requests', Rekening = ['NL03BUNQ2025449445'])
        self.assertEqual(sortInfo(trans), [('Aliexpres', 0.01), ('Gorrila', 202.30), ('Requests', 74.09),('Other', -53.00)])
