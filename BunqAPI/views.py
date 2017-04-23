from django.shortcuts import render
from .forms import GenerateKeyForm
from .installation import createKey
# from django.http import HttpResponse
# from django.http.response import FileResponse

# Create your views here.


def generate(request):
    if request.method == 'POST':
        formKey = GenerateKeyForm(request.POST)
        if formKey.is_valid():
            print ('\n\nGenerating...\n\n')
            return createKey()

    else:
        formKey = GenerateKeyForm()
    return render(request, 'BunqAPI/index.html', {'form': formKey})
