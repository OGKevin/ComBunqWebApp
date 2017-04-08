# from Manager.models import catagories
import csv
import json
import os
import sys
curdir = os.path.abspath(os.curdir)
print curdir
sys.path.insert(0, curdir)
from Manager.models import catagories


f = open('DatabseInput/ComBunqWeb-category-filter.csv')
reader = csv.reader(f, delimiter=',', quotechar='"')
keys = next(reader) #skip the headers
out = [{key: val for key, val in zip(keys, prop)} for prop in reader]
print json.dumps(out, sort_keys = True,indent=2)
