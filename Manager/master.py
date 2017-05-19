from .models import catagories


def sortInfo(transactions):
    '''
     Does the category soorting of the transactions.
    '''
    catOBJ = {'Other': 0}
    cat = catagories.objects
    for x in transactions:
        filt = cat.filter(Rekening__contains=[x['Tegenrekening']])
        ammount = float(x['Bedrag'].replace(",", "."))
        try:
            catName = str(filt[0])
        except IndexError:
            catOBJ['Other'] += ammount
            x['Category'] = 'Other'

        else:
            if x['Tegenrekening'] is not "":
                if catName in catOBJ:
                    catOBJ[catName] += ammount
                    x['Category'] = catName
                else:
                    catOBJ[catName] = ammount
                    x['Category'] = catName
            else:
                catOBJ['Other'] += ammount
                x['Category'] = 'Other'
    returnInfo = {
        'catagories': list(catOBJ.items()), 'transactions': transactions}
    return returnInfo
