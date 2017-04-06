from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from . import master
import json
from models import transactions
# from .forms import GetNewData
# Create your views here.


def Manager(request):
    data = master.getDate("", "")
    simpleData = json.dumps(data, sort_keys=True)
    # # NOTE: for when using login and db
    # if request.method == 'POST':
    #     form = GetNewData(request.POST)
    #     if form.is_valid():
    #         data = master.getDate("20170330", "20170331")
    #         simpleData = json.dumps(data, sort_keys=True)
    #         return render(request, 'Manager/index.html',{'data': data, 'simpleData': simpleData, } )
    #         print "valed form"
    # else:
    #     form = GetNewData()
    # # NOTE: endNote
    return render(request,'Manager/index.html',{'data': data, 'simpleData': simpleData,  })


# def getData(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = GetNewData(request.POST)
#         print 'post'
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             data = master.getDate("20170330", "20170331")
#             simpleData = json.dumps(data, sort_keys=True)
#             return render(request, 'Manager/index.html',{'data': data, 'simpleData': simpleData, 'from' : form} )
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = GetNewData()
#
#     return render(request, 'Manager/form.html', {'form': form})
