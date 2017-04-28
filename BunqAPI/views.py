from django.shortcuts import render
from .forms import GenerateKeyForm
from .installation import createJSON
from django.utils.encoding import smart_str
from django.http import HttpResponse
# from django.http.response import FileResponse

# Create your views here.


def generate(request):
    if request.method == 'POST':
        formKey = GenerateKeyForm(request.POST)
        if formKey.is_valid():
            print ('\n\nGenerating...\n\n')
            # password = formKey.cleaned_data['password']
            # userID = formKey.cleaned_data['userID']
            encryptedData = createJSON()
            response = HttpResponse(
                encryptedData, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('BunqWebApp.json')  # noqa
            # response.write(open(dFile, 'r'))
            # It's usually a good idea to set the 'Content-Length' header too.
            # You can also set any other required headers: Cache-Control, etc.
            return response

    else:
        formKey = GenerateKeyForm()
    return render(request, 'BunqAPI/index.html', {'form': formKey})
