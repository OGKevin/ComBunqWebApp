from django.shortcuts import render, redirect
from BunqWebApp.forms import registration, LogInForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.generic.base import RedirectView
from django.views import View
from django.core import signing
from filecreator.creator import Creator
import requests
from pprint import pprint
import arrow
import markdown2
import datetime
from BunqAPI.callbacks import callback
from django.http import HttpResponse
from BunqAPI.installation import Installation
import json
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


class LogInView(View):
    form = LogInForm

    def get(self, request):
        form = self.form()
        return render(request, 'registration/log_in.html', {'form': form})

    def post(self, request):
        form = self.form(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            file_contents = request.FILES['user_file']

            if self.authenticate_user(username, password):
                self.decrypt_contents(file_contents, password)
                return redirect('my_bunq')
            else:
                error = {
                    'Error': [{
                        'error': 'user autentication failed'
                    }]
                }
                return HttpResponse(json.dumps(error))
        else:
            return render(request, 'registration/log_in.html', {'form': form})

    @staticmethod
    def authenticate_user(username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            return True
        else:
            return False

    @staticmethod
    def decrypt_contents(data, password):
        data = json.loads(data.read().decode())
        dec_data = signing.loads(data['secret'], key=password)
        pprint(dec_data)
