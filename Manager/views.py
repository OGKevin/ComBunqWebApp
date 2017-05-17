from django.shortcuts import render
from django.http import HttpResponse
from .databaseInput import addTegenrekening, store
import json
from .forms import GetNewData, inputDatabase
from collections import OrderedDict

# Create your views here.


def Manager(request):  # pragma: no cover
    if request.method == 'POST':
        form = GetNewData(request.POST)
        inputData = json.loads(
            request.POST['json'], object_pairs_hook=OrderedDict)
        return HttpResponse(json.dumps(addTegenrekening(inputData)))
    else:
        form = GetNewData()
    return render(request, 'Manager/index.html', {'from': form})


def managerForm(request):  # pragma: no cover
    if request.method == 'POST':  # NOTE: cant test post due to captcha
        form = inputDatabase(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            store(data)
            return render(request, 'Manager/thanks.html', {'data': data})
    else:
        form = inputDatabase()
    return render(request, 'Manager/form.html', {'form': form})
