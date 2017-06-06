from django.shortcuts import render, redirect
from BunqWebApp import forms, decrypt
from BunqAPI.forms import GenerateKeyForm
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import authenticate, login
from django.views.generic.base import RedirectView
from django.views import View
from django.core import signing
import requests
import arrow
import markdown2
from django.http import HttpResponse
from BunqAPI.installation import Installation
import json
# from pprint import pprint
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
    form = forms.registration

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
    form = forms.LogInForm

    def get(self, request):
        form = self.form()
        return render(request, 'registration/log_in.html', {'form': form})

    def post(self, request):
        form = self.form(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            file_contents = request.FILES['user_file']

            if self.authenticate_user(username, password, request):
                self.store_in_session(file_contents, password, username)
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
    def authenticate_user(username, password, request):
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return True
        else:
            return False

    @staticmethod
    def store_in_session(data, password, username):
        user = User.objects.get(username=username)
        data = json.loads(data.read().decode())
        dec_data = signing.loads(data['secret'], key=password)

        enc_data = signing.dumps(dec_data)

        s = SessionStore()
        s['api_data'] = enc_data
        s.create()
        user.session.session_token = s.session_key
        user.save()


class MigrationService(View):
    form = forms.MigrationLogIn
    generate_form = GenerateKeyForm

    def get(self, request):
        form = self.form()
        return render(request, 'registration/old_log_in.html', {
                                                            'form': form})

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            encryption_password = form.cleaned_data['encryption_password']
            user_file = request.FILES['user_file']
            if self.authenticate_user(username=username, password=password,
                                      request=request):
                api_key = self.decrypt_file(user_file=user_file,
                                            encryption_password=encryption_password)  # noqa
                if api_key is not False:
                    print(api_key)
                    form = self.generate_form(initial={'API': api_key})
                    return render(request, 'BunqAPI/index.html',
                                  {'form': form})
                else:
                    print('decrypt_file no')
            else:
                print('autentication no')
        else:
            print('invalid form')
            return render(request, 'registration/old_log_in.html', {
                                                                'form': form})

    @staticmethod
    def authenticate_user(username, password, request):
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return True
        else:
            return False

    @staticmethod
    def decrypt_file(user_file, encryption_password):
        aes = decrypt.AESCipher(key=encryption_password)
        try:
            dec = aes.decrypt(enc=json.loads(user_file.read().decode())[
                                                                    'secret'])
        except UnicodeDecodeError:
            return False
        else:
            return dec['API']
