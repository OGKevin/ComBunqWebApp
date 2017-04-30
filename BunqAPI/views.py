from django.shortcuts import render
from .forms import GenerateKeyForm
from .installation import createJSON
from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.contrib.auth import authenticate
# from django.http.response import FileResponse

# Create your views here.


def generate(request):
    if request.method == 'POST':
        formKey = GenerateKeyForm(request.POST)
        if formKey.is_valid():
            print ('\n\nGenerating...\n\n')
            password = formKey.cleaned_data['password']
            username = formKey.cleaned_data['username']
            API = formKey.cleaned_data['API']
            encryption_password = formKey.cleaned_data['encryption_password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # login(request, user)
                encryptedData = createJSON(username, encryption_password, API)
                response = HttpResponse(
                    encryptedData, content_type='application/force-download')
                response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('BunqWebApp.json')  # noqa
                return response
            else:
                return HttpResponse('invalid user')

    else:
        formKey = GenerateKeyForm()
    return render(request, 'BunqAPI/index.html', {'form': formKey})
