from django.shortcuts import render
from .forms import GenerateKeyForm
from .installation import createKey
from django.http import HttpResponse
# from django.http.response import FileResponse

# Create your views here.


def generate(request):
    if request.method == 'POST':
        form = GenerateKeyForm(request.POST)
        if form.is_valid():
            print ('\n\nGenerating...\n\n')
            # print (createKey()['privateKey'])
            response = HttpResponse(
                createKey()['privateKey'],
                content_type='application/force-download')
            response['Content-Disposition'] = 'attachment;filename="privateKey.pem"'
            return response  # NOTE: somehting is not right here

    else:
        form = GenerateKeyForm()
    return render(request, 'BunqAPI/index.html', {'form': form})
