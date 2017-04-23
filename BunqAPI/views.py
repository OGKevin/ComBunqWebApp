from django.shortcuts import render
from .forms import GenerateKeyForm
from .installation import createKey, delTemp
from django.http import HttpResponse
# from django.http.response import FileResponse

# Create your views here.


def generate(request):
    if request.method == 'POST':
        formKey = GenerateKeyForm(request.POST)
        if formKey.is_valid():
            print ('\n\nGenerating...\n\n')
            # print (createKey()['privateKey'])
            keyFilePath = createKey()
            print (keyFilePath)
            keyFile = HttpResponse(
                open(keyFilePath, 'r'),
                content_type='application/force-download')
            keyFile['Content-Disposition'] = 'attachment;filename="privateKey.json"'
            try:
                return keyFile  # NOTE: somehting is not right here
            finally:
                delTemp()

    else:
        formKey = GenerateKeyForm()
    return render(request, 'BunqAPI/index.html', {'form': formKey})
