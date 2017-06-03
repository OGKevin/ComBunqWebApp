from django.shortcuts import render
from BunqWebApp.forms import registration
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.generic.base import RedirectView
from django.views import View
from django.core import signing
from filecreator.creator import Creator
import requests
# from pprint import pprint
import arrow
import markdown2
import datetime
from BunqAPI.callbacks import callback
from BunqAPI.installation import Installation
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
            'https://api.github.com/repos/OGKevin/combunqwebapp/releases') \
                                                                        .json()

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
            api_key = form.cleaned_data['api_key']
            self.create_and_login(username=username, password=password,
                                  request=request)
            registration = Installation(self._user,
                                        api_key, password)

            if registration.status:
                return render(request,
                              'registration/complete.html')
            else:
                return render(request, 'registration/register.html',
                              {'form': form,
                               'Error': 'api registration unsuccessful.',
                               'error': True})

        else:
            return render(request, 'registration/register.html',
                          {'form': form})

    def create_and_login(self, username, password, request):
        self._user = User.objects.create_user(username=username,
                                              password=password)
        authentication = authenticate(username=username, password=password)
        if authentication is not None:
            login(request, self._user)
