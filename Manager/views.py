from django.shortcuts import render
from django.http import HttpResponse
# from django.template import loader
# from . import master
from .databaseInput import addTegenrekening, store
import json
from .forms import GetNewData, inputDatabase
from collections import OrderedDict

# Create your views here.


def Manager(request):
    # # NOTE: Colecting user input to match againts catagory in db
    if request.method == 'POST':
        form = GetNewData(request.POST)
        inputData = json.loads(
            request.POST['json'], object_pairs_hook=OrderedDict)
        return HttpResponse(json.dumps(addTegenrekening(inputData)))
    else:
        form = GetNewData()
    # # NOTE: endNote
    return render(request, 'Manager/index.html', {'from': form})


def googleFrom(request):
    return render(request, 'Manager/googleFrom.html')


def managerForm(request):
    if request.method == 'POST':
        form = inputDatabase(request.POST)
        print ('post')
        if form.is_valid():
            data = form.cleaned_data
            store(data)
            return render(request, 'Manager/thanks.html', {'data': data})
    else:
        form = inputDatabase()
    return render(request, 'Manager/form.html', {'form': form})
