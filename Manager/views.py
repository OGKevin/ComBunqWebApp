from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from . import master
import json
from .forms import GetNewData
# Create your views here.


def Manager(request):
    # data = master.getDate("", "",'database')
    # simpleData = json.dumps(data, sort_keys=True)
    # # NOTE: Colecting user input to match againts catagory in db
    if request.method == 'POST':
        print 'post'
        form = GetNewData(request.POST)
        # print form
        inputData = json.loads(request.POST['json'])
        # print inputData
        print type(inputData)
        # print master.sortInfo(inputData)
        return HttpResponse(json.dumps(master.sortInfo(inputData)))
        # print 'This should be the unser input',dict(inputData.lists())
        if form.is_valid():
            print "valed form"
    else:
        form = GetNewData()
        # print form
        print 'get'
    # # NOTE: endNote
    return render(request,'Manager/index.html',{ 'from': form  })
