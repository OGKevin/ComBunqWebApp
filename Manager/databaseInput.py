from .models import catagories
# import json
import re
from .master import sortInfo
from itertools import chain


def addTegenrekening(transactions):
    cat = catagories.objects
    regex = cat.values_list('regex')
    regex1 = list(chain.from_iterable(chain.from_iterable(regex)))
    # print (list(regex1), 'list')
    for x in transactions:
        # print (json.dumps(x, indent=4))
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
                    # print(editCat)
                    x['Tegenrekening'] = str(editCat)
    # # for k in cat.values():
    # #     print (json.dumps(k, indent=4))
    for ibanList in cat.values_list('Rekening', flat=True):
        p = cat.get(Rekening=ibanList)
        # print (set(ibanList))
        p.Rekening = list(set(ibanList))
        p.save()
    # # print (json.dumps(transactions, indent=4))
    return sortInfo(transactions)
    # # for l in cat.values():
    # #     print (json.dumps(l, indent=4))


def store(data):
    # NOTE: cant test this via post due to captcha
    print (data)
    keyWord = data['keyWord']
    iban = data['iban']
    p = catagories.objects.get(Naam=data['catagory'])
    keyWordList = p.regex
    ibanList = p.Rekening
    # print(p)
    if keyWord is not '':
        # print (keyWord)
        keyWordList.append(keyWord)
        # print (keyWordList)
        # print (set(keyWordList))
        p.regex = list(set(keyWordList))
        p.save()
    if iban is not '':
        # print (iban)
        ibanList.append(iban)
        # print (ibanList)
        # print (set(ibanList))
        p.Rekening = list(set(ibanList))
        p.save()
