from .models import catagories
# import json

# NOTE: starting from the beginning with new databse models


def sortInfo(transactions):
    catOBJ = {'Other': 0}
    cat = catagories.objects
    for x in transactions:
        filt = cat.filter(Rekening__contains=[x['Tegenrekening']])
        ammount = float(x['Bedrag'].replace(",", "."))
        try:
            catName = str(filt[0])
        except IndexError:
            print ('catagory not found in database\nAdding it to "Other"')
            catOBJ['Other'] += ammount
            x['Catagory'] = 'Other'

        else:
            print (catName, 'found')
            if catName in catOBJ:
                catOBJ[catName] += ammount
                x['Catagory'] = catName
            else:
                catOBJ[catName] = ammount
                x['Catagory'] = catName
    returnInfo = {
        'catagories': list(catOBJ.items()), 'transactions': transactions}
    return returnInfo
