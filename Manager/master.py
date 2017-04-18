from .models import catagories


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
            if x['Tegenrekening'] is not "":
                if catName in catOBJ:
                    catOBJ[catName] += ammount
                    x['Catagory'] = catName
                else:
                    catOBJ[catName] = ammount
                    x['Catagory'] = catName
            else:
                print ("empty Tegenrekening")
                catOBJ['Other'] += ammount
                x['Catagory'] = 'Other'
    returnInfo = {
        'catagories': list(catOBJ.items()), 'transactions': transactions}
    return returnInfo
