from .models import catagories
import re
from .master import sortInfo
from itertools import chain


def addTegenrekening(transactions):
    '''
    Automaticlly adds Ibans to the database based on keywords stored in the
    database.
    '''
    cat = catagories.objects
    regex = cat.values_list('regex')
    regex1 = list(chain.from_iterable(chain.from_iterable(regex)))
    for x in transactions:
        for y in regex1:
            editCat = cat.get(regex__contains=[y])
            ibanList = editCat.Rekening
            pattern = re.compile(y)
            if pattern.search(x['Naam']):
                print ('match found -->', editCat)
                if x['Tegenrekening'] is not "":
                    ibanList.append(x['Tegenrekening'])
                    editCat.save()
                else:
                    ibanList.append(editCat)
                    editCat.save()
                    x['Tegenrekening'] = str(editCat)
    for ibanList in cat.values_list('Rekening', flat=True):
        p = cat.get(Rekening=ibanList)
        p.Rekening = list(set(ibanList))
        p.save()
    return sortInfo(transactions)


def store(data):
    '''
    Stores infomration in the database that is provided via the form on
    /manager/form page.
    '''
    # NOTE: cant test this via post due to captcha
    # print (data)
    keyWord = data['keyWord']
    iban = data['iban']
    p = catagories.objects.get(Naam=data['catagory'])
    keyWordList = p.regex
    ibanList = p.Rekening
    if keyWord is not '':
        keyWordList.append(keyWord)
        p.regex = list(set(keyWordList))
        p.save()
    if iban is not '':
        ibanList.append(iban)
        p.Rekening = list(set(ibanList))
        p.save()
