import csv
import json
import os
import sys
import requests
curdir = os.path.abspath(os.curdir)
print curdir
sys.path.insert(0, curdir)
from Manager.models import catagories


def getJSON():
    
    catFiltersCSV = open('DatabaseInput/ComBunqWeb-category-filter.csv')
    reader = csv.reader(catFiltersCSV, delimiter=',', quotechar='"')
    keys = next(reader)
    catFiltersJSON = [{key:val for key,val in zip(keys,prop)} for prop in reader]
    return catFiltersJSON
    

def getHeaders():
    catFiltersCSV = open('DatabaseInput/ComBunqWeb-category-filter.csv')
    reader = csv.reader(catFiltersCSV, delimiter=',', quotechar='"')
    keys = reader.next()
    return keys


def validator():
    obj = getJSON()
    url = 'https://openiban.com/validate/'
    
    print json.dumps(obj,sort_keys=True,indent = 2 )
    for x in range(len(getJSON())):
        print x
        for y in getHeaders():
            try:
                obj[x][y]
                check = json.loads(requests.get("".join([url,obj[x][y]])).content)
                if check['valid']:
                    print 'valid IBAN'
                    print y, ' ', obj[x][y]
                    obj[x][y] = newCatInfo(y,obj[x][y])
                    isInDatabase(obj[x][y])
                    
                else:
                    print 'unvalid IBAN'
            except KeyError:
                continue


class newCatInfo(object):
    """docstring for newCatInfo."""
    def __init__(self, catName,Iban):
        super(newCatInfo, self).__init__()
        self.catName = catName
        self.Iban = Iban
    
    def getIban(self):
        print self.Iban
    
    def __str__(self):
        return self.catName


def isInDatabase(catInfo):
    test = 'Aliexpres'
    cat = catagories.objects
    # print catInfo.getIban()
    catName = str(catInfo)
    ibanList = cat.get(Naam = catName)
    print type(catName)
    print cat.filter(Naam = catName)[0] # NOTE: query set from DB the [0] is so that we get the catagory name if its in the db
    if str(cat.filter(Naam = catName)[0]) == catName:
        print catName,"is in database", ibanList.Rekening #catagory is already in database
    else:
        print catName, 'is not in database' # not in data base so need to create it
    

validator()
