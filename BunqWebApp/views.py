from django.shortcuts import render, redirect
from BunqWebApp.forms import registration
from django.contrib.auth.models import User
# from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views.generic.base import RedirectView
from django.views import View
import requests
# from pprint import pprint
import arrow
import markdown2
# from django.http import HttpResponse
# from django.template import loader

# Create your views here.


class RedirectView(RedirectView):
    """docstring for RedirectView.
    Redirects ecerything else to home page
    """
    permanent = False
    pattern_name = 'home'

    def get_redirct_url(self):
        return super().get_redirct_url()


class HomeView(View):
    """docstring for HomeView."""

    def get(self, request):
        data = self.get_releases()
        return render(request, 'Home/index.html', {'data': data})

    def get_releases(self):
        res = requests.get(
            'https://api.github.com/repos/OGKevin/combunqwebapp/releases').json()  # noqa

        data = res[:7]
        for x in data:
            x['created_at'] = arrow.get(x['created_at']).format('Do MMM')
            x['body'] = markdown2.markdown(x['body'])

        return data


class RegisterView(View):
    """docstring for RegisterView."""
    form = registration

    def get(self, request):
        form = self.form()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = self.form(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, '', password)
            user.save()
            auth = authenticate(username=username, password=password)
            if auth is not None:
                login(request, auth)

                return redirect('../two_factor/setup')
        else:
            return render(request, 'registration/register.html', {'form': form})  # noqa


def register(request):
    '''
    View that handles the registration page.
    '''
    if request.method == 'POST':
        form = registration(request.POST)
        if form.is_valid():
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
