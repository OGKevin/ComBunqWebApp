from django.shortcuts import render
from django.http import HttpResponse
# from django.template import loader
# from . import master
from .automaticDbInput import addTegenrekening
import json
from .forms import GetNewData
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
