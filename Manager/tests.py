from django.test import TestCase
from django.core.management import call_command
from django.utils.six import StringIO
# Create your tests here.

class DatabaseInputTest(TestCase):
    """docstring for NewMasterTest."""
    def test_command_output(self):
        out = StringIO()
        call_command('InputDataInDataBase', stdout = out)
        # self.assertIn('Expected output', out.getvalue())
