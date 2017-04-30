from django.shortcuts import render
from .forms import GenerateKeyForm, decrypt_form
from .installation import createJSON
from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import json
from .encryption import AESCipher
from pprint import pprint

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


def decrypt(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        userGUID = user.profile.GUID
        print(user)
        print(userGUID)
        form = decrypt_form(request.POST)
        inputData = json.loads(
            request.POST['json'])
        password = request.POST['pass']
        print(password)
        pprint(inputData)
        print(type(inputData))
        if inputData['userID'] == userGUID:
            p = AESCipher(password)
            data = json.loads(AESCipher.decrypt(p, inputData['secret']))
            pprint(data)
            print(type(data))
            return HttpResponse(json.dumps(data, indent=4))
        else:
            return HttpResponse('this file is not yours')

    else:
        form = decrypt_form()
    return render(request, 'BunqAPI/decrypt.html', {'form': form})
