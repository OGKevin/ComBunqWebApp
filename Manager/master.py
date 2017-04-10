import json
import os
import sys
from models import catagories

# NOTE: startinh from the beginning with new databse models

catOBJ = {}
        
def sortInfo(transactions):
    cat = catagories.objects
    for x in transactions:
        print x
        filt = cat.filter(Rekening__contains = [x['Tegenrekening']])
        try:
            catName = str(filt[0])
            print catName
        except IndexError:
            print 'cat not found in database'
        else:
            ammount = float(x['Bedrag'].replace(",","."))
            print 'cat found '
            if catName in catOBJ:
                catOBJ[catName] += ammount
            else:
                catOBJ[catName] = ammount
    print 'catOBJ', catOBJ.items()
    return catOBJ.items()
