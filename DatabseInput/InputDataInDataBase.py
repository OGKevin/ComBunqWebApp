# from Manager.models import catagories
import csv
import json
import os
import sys
curdir = os.path.abspath(os.curdir)
print curdir
sys.path.insert(0, curdir)
from Manager.models import catagories


def getJSON():
    catFiltersCSV = open('DatabseInput/ComBunqWeb-category-filter.csv')
    reader = csv.reader(catFiltersCSV, delimiter=',', quotechar='"')
    keys = next(reader)
    catFiltersJSON = [{key:val for key,val in zip(keys,prop)} for prop in reader]
    print json.dumps(catFiltersJSON,sort_keys=True,indent=2)
    getHeaders()
    

def getHeaders():
    catFiltersCSV = open('DatabseInput/ComBunqWeb-category-filter.csv')
    reader = csv.reader(catFiltersCSV, delimiter=',', quotechar='"')
    keys = reader.next()
    print keys
    

getJSON()
