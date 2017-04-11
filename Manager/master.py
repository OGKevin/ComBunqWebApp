from .models import catagories
import json

# NOTE: starting from the beginning with new databse models

catOBJ = {'Other': 0}


def sortInfo(transactions):
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
    # print ('this should be transactions\n%s' % json.dumps(
        # transactions, indent=4))
    # print ('catOBJ', list(catOBJ.items()))
    returnInfo = {
        'catagories': list(catOBJ.items()), 'transactions': transactions}
    # print (json.dumps(returnInfo, indent=4))
    return returnInfo
