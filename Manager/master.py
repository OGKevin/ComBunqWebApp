import json
import os
import sys
from models import transactions, catagories

# NOTE: getting JSON from database
# need to chage this to not use global vars
data = []
catagory =[]
def getInfo(method):
    
    if method == 'database':
        print 'Method: ',method
        data1 = list(transactions.objects.values_list('attrs', flat=True))
        global data
        data = data1[0]
        # print data[0]
        catagory1 = list(transactions.objects.values_list('catagory', flat=True))
        global catagory
        catagory = catagory1[0]
        # print catagory
        
        
        # NOTE: testing databse catagory retrieval
        catName = list(catagories.objects.filter(Rekening__contains = ['DE60700111100250250061']).values_list('Naam'))
        catList = []
        allCatNames = list(catagories.objects.values_list('Naam', flat=True))
        print 'allCatNames = ',allCatNames # NOTE: Whit this in getExpenses catagoryObj can be made. Or wiht something like catName only catagories that has been found should be returned.
        for x in catName:
            # print 'catagoryNmae ',x[0]
            catList.append(x[0])
                    
        print 'catagories found: ',catList
        # NOTE: this should be implemented in getExpenses or a new fucntion createCatagory
        # print type(catName)
        # NOTE: endNote
        
        
        
        
        return {'data':data, 'catagory' : catagory} # NOTE: the idea is that these get returned so that Global vars should be used
    else:
        print 'Method: user input'
        data1 = method
        # print data1
        global data
        data = data1
        # print data
        catagory1 = list(transactions.objects.values_list('catagory', flat=True))
        global catagory
        catagory = catagory1[0]
        # print catagory
        return {'data':data, 'catagory' : catagory} # NOTE: the idea is that these get returned so that Global vars should be used
        

def getTotal():
    getInfo()
    total = 0
    for x in range(len(data)):
        total += float(data[x]["Bedrag"].replace(",", "."))
    return total





def getExpenses(begin, end):
    # getInfo(method)
    catagoryObj = {}
    table = []
    totalExpanses = 0
    totalIncome = 0
    k = 0
    while k < len(catagory):
        catagoryObj[catagory[k]["Naam"]] = 0
        k += 1
    for k in range(begin, end + 1):
        for x in range(len(catagory)):
            if data[k]["Tegenrekening"] == catagory[x]["Rekening"]:
                catagoryObj[catagory[x]["Naam"]
                            ] += round(float(data[k]["Bedrag"].replace(",", ".")), 2)
                break
            elif x == len(catagory) - 1:
                catagoryObj["Other"] += round(float(data[k]
                                                    ["Bedrag"].replace(",", ".")), 2)
                print "not in catagory list"

        if float(data[k]["Bedrag"].replace(",", ".")) < 0:
            totalExpanses += float(data[k]["Bedrag"].replace(",", "."))
        else:
            totalIncome += float(data[k]["Bedrag"].replace(",", "."))
        k += 1
    for x in range(len(catagoryObj)):
        if catagoryObj[catagory[x]["Naam"]] < 0:
            percentage = round(
                abs(catagoryObj[catagory[x]["Naam"]] / totalExpanses * 100), 2)
        else:
            percentage = round(
                abs(catagoryObj[catagory[x]["Naam"]] / totalIncome * 100), 2)
        table.extend(
            [[catagory[x]["Naam"], catagoryObj[catagory[x]["Naam"]], percentage]])
    print table
    return table


def getDate(start, stop, method):
    getInfo(method)
    begin = 0
    end = 0
    if start == "":
        begin = 0
    else:
        for x in range(len(data)):
            if data[x]["Datum"].replace("-", "") == start:
                begin = x
                break
    if stop == "":
        end = len(data) - 1
    else:
        for x in range(len(data)):
            if data[x]["Datum"].replace("-", "") == stop:
                end = x
    
    return getExpenses(begin, end)
        
