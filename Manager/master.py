import json
import os
import sys
from models import catagories

# NOTE: startinh from the beginning with new databse models

catOBJ = {'Other': 0 }
        
def sortInfo(transactions):
    cat = catagories.objects
    for x in transactions:
        filt = cat.filter(Rekening__contains = [x['Tegenrekening']])
        ammount = float(x['Bedrag'].replace(",","."))
        try:
            catName = str(filt[0])
        except IndexError:
            print 'catagory not found in database\nAdding it to "Other"'
            catOBJ['Other'] += ammount
            
        else:
            print catName,'found '
            if catName in catOBJ:
                catOBJ[catName] += ammount
            else:
                catOBJ[catName] = ammount
    print 'catOBJ', catOBJ.items()
    return catOBJ.items()
