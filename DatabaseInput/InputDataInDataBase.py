# from Manager.models import catagories
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
    
    catFiltersCSV = open('DatabseInput/ComBunqWeb-category-filter.csv')
    reader = csv.reader(catFiltersCSV, delimiter=',', quotechar='"')
    keys = next(reader)
    catFiltersJSON = [{key:val for key,val in zip(keys,prop)} for prop in reader]
    # print json.dumps(catFiltersJSON,sort_keys=True,indent=2)
    # getHeaders()
    return catFiltersJSON
    

def getHeaders():
    catFiltersCSV = open('DatabseInput/ComBunqWeb-category-filter.csv')
    reader = csv.reader(catFiltersCSV, delimiter=',', quotechar='"')
    keys = reader.next()
    # print keys
    return keys

# getJSON()

def validator():
    obj = getJSON()
    url = 'https://openiban.com/validate/'
    
    print json.dumps(obj,sort_keys=True,indent = 2 )
    for x in range(len(getJSON())):
        print x
        for y in getHeaders():
            try:
                obj[x][y]
                # print y,':',obj[x][y]
                check = json.loads(requests.get("".join([url,obj[x][y]])).content)
                print check['valid']
                # print type(list(valid))
            except KeyError:
                continue
            
        

validator()
