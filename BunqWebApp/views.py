from django.shortcuts import render, redirect
from BunqWebApp.forms import registration
from django.contrib.auth.models import User
# from django.http import HttpResponse
from django.contrib.auth import authenticate, login
# from django.http import HttpResponse
# from django.template import loader

# Create your views here.


def home(request):
    '''
    The dummy home page.
    '''
    return render(request, 'Home/index.html')


def register(request):
    '''
    View that handles the registration page.
    '''
    if request.method == 'POST':
        form = registration(request.POST)
        if form.is_valid():
            print('valid form')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, '', password)
            user.save()
            auth = authenticate(username=username, password=password)
            if auth is not None:
                login(request, auth)

                return redirect('../two_factor/setup')
    else:
        form = registration()
    return render(request, 'registration/register.html', {'form': form})
