import csv
import json
import requests
from django.core.exceptions import ObjectDoesNotExist
from Manager.models import catagories
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """docstring for Command.

    There is actually no use for this anymore. This was usefull when
    #5 was still in play, now the /manager/form is being used."""
    def handle(self, *args, **options):
        validator()


def getJSON():
    catFiltersCSV = open(
        'Manager/management/DatabaseInput/ComBunqWeb-category-filter.csv')
# NOTE: This can be used later for a from on the App itself

    reader = csv.reader(catFiltersCSV, delimiter=',', quotechar='"')
    keys = next(reader)
    catFiltersJSON = [{
        key: val for key, val in zip(keys, prop)} for prop in reader]
    return catFiltersJSON


def getHeaders():
    catFiltersCSV = open(
        'Manager/management/DatabaseInput/ComBunqWeb-category''-filter.csv')
# NOTE: This can be used later for a from on the App itself
    reader = csv.reader(catFiltersCSV, delimiter=',', quotechar='"')
    keys = next(reader)
    return list(keys)


def validator():
    obj = getJSON()
    url = 'https://openiban.com/validate/'
    for x in range(len(getJSON())):
        for y in getHeaders():
            try:
                obj[x][y]
                # print y,':',obj[x][y]
                check = json.loads(requests.get(
                    "".join([url, obj[x][y]])).content.decode())
                if check['valid']:
                    obj[x][y] = newCatInfo(y, obj[x][y])
                    isInDatabase(obj[x][y])
            except KeyError:
                continue


class newCatInfo(object):
    """docstring for newCatInfo."""
    def __init__(self, catName, Iban):
        super(newCatInfo, self).__init__()
        self.catName = catName
        self.Iban = Iban

    def getIban(self):
        return self.Iban

    def __str__(self):
        return self.catName


def isInDatabase(catInfo):
    cat = catagories.objects
    catName = str(catInfo)
    iban = catInfo.getIban()
    try:
        cat.get(Naam=catName)

    except ObjectDoesNotExist:
        # NOTE: create catagory
        cat.create(Naam=catName, Rekening=[iban], regex=[])
    else:
        editCat = cat.get(Naam=catName)
        ibanList = editCat.Rekening
        if iban not in ibanList:
            ibanList.append(iban)
            editCat.save()
