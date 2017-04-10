from django import forms

class GetNewData(forms.Form):
    initialText = '"Datum";"Bedrag";"Rekening";"Tegenrekening";"Naam";"Omschrijving"\n"2017-03-31";"-0,01";"NL01BUNQ1234567890";"NL48ABNA0502830042";"Spotify by Adyen";"Payment description"\n"2017-03-31";"1,64";"NL01BUNQ1234567890";"NL01BUNQ1234567890";"bunq";"Slice heeft deze request verstuurd voor de groep Family."\n\n\n#Only dutch headers supported atm\n#Only Bunq CSV supported atm, or place 2 columns with headers \'Bedrag\'(ammount) and \'Naam\'(name)\n#Press \'via CSV text\' to see this example in action\n#Lines that begin with \'#\' wil be ignored'
    JSONTransactions = forms.CharField(initial = initialText, widget = forms.Textarea, label='')
    # JSONTransactionsFile = forms.FileField(label='')
