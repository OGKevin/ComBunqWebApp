from django.shortcuts import render
from django.http import HttpResponse
from Manager.databaseInput import addTegenrekening, store
import json
from Manager.forms import GetNewData, inputDatabase
from collections import OrderedDict
from django.views import View


# Create your views here.

class ManagerView(View):
    """docstring for ManagerView."""
    form = GetNewData

    def get(self, request):
        form = self.form()
        return render(request, 'Manager/index.html', {'form': form})

    def post(self, request):
        # form = self.form(request.POST)  # NOTE: whats this, never used !!??
        inputData = json.loads(
            request.POST['json'], object_pairs_hook=OrderedDict)
        return HttpResponse(json.dumps(addTegenrekening(inputData)))


class ManagerFormView(View):
    """docstring for ManagerFormView."""
    form = inputDatabase

    def get(self, request):
        form = self.form()
        return render(request, 'Manager/form.html', {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid:
            data = form.cleaned_data
            store(data)
            return render(request, 'Manager/thanks.html', {'data': data})
