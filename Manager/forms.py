from django import forms
from django.contrib import admin


class GetNewData(forms.Form):
    initialText = (
        '"Datum";"Bedrag";"Rekening";"Tegenrekening";"Naam";'
        '"Omschrijving"\n"2017-03-31";"-0,01";"NL01BUNQ1234567890";"NL48ABNA05'
        '02830042";"Spotify by Adyen";"Payment description"\n"2017-03-31";"1,6'
        '4";"NL01BUNQ1234567890";"NL01BUNQ1234567890";"bunq";"Slice heeft deze'
        ' request verstuurd voor de groep Family."\n\n\n#Only dutch headers su'
        'pported atm\n#Only Bunq CSV supported atm, or place 2 columns with he'
        'aders \'Bedrag\'(ammount) and \'Tegenrekening\'(payee)\n#Press \'via '
        'CSV text\''
        ' to see this example in action\n#Lines that begin with \'#\' wil be '
        'ignored')
    JSONTransactions = forms.CharField(
        initial=initialText,
        widget=forms.Textarea, label=''
        )
    JSONTransactionsFile = forms.FileField(label='')


class catagoriesAdminForm(forms.ModelForm):  # pragma: no cover
    """docstring for catagoriesAdmin."""
    def __init__(self, *args, **kwargs):
        super(catagoriesAdminForm, self).__init__(*args, **kwargs)
        self.fields['Rekening'].widget = admin.widgets.AdminTextareaWidget()
