from .models import catagories
# import json
import re
from .master import sortInfo


def addTegenrekening(transactions):
    cat = catagories.objects
    regex = cat.values_list('regex')
    # print (list(regex))
    for x in transactions:
        # print (json.dumps(x, indent=4))
        for y in regex:
            editCat = cat.get(regex=y[0])
            ibanList = editCat.Rekening
            # print ('y ==', y[0], '\n', editCat)
            pattern = re.compile(y[0])
            if pattern.match(x['Naam']):
                print ('match found -->', editCat)
                if x['Tegenrekening'] is not "":
                    ibanList.append(x['Tegenrekening'])
                    editCat.save()
                else:
                    ibanList.append(editCat)
                    editCat.save()
                    # print(editCat)
                    x['Tegenrekening'] = str(editCat)
    # for k in cat.values():
    #     print (json.dumps(k, indent=4))
    for ibanList in cat.values_list('Rekening', flat=True):
        p = cat.get(Rekening=ibanList)
        # print (set(ibanList))
        p.Rekening = list(set(ibanList))
        p.save()
    # print (json.dumps(transactions, indent=4))
    return sortInfo(transactions)
    # for l in cat.values():
    #     print (json.dumps(l, indent=4))
