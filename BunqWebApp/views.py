from django.shortcuts import render, redirect
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
        # setattr(self, '__request', request)
        # self._request = request

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            api_key = form.cleaned_data['api_key']
            self.create_and_login(username=username, password=password,
                                  request=request)
            registration = self.register_api_key(api_key, self._user, password)

            if registration:
                print('no returning None')
                return render(request,
                              template_name='registration/complete.html')
            else:
                print('heeeeyy ERRRROR')
                pass

        else:
            return render(request, 'registration/register.html',
                          {'form': form})

    def create_and_login(self, username, password, request):
        self._user = User.objects.create_user(username=username,
                                              password=password)
        authentication = authenticate(username=username, password=password)
        if authentication is not None:
            login(request, self._user)

    def register_api_key(self, api_key, user, password):
        c = callback(api_key=api_key, user=self._user)
        installation = c.installation()

        if installation['status']:
            enc_string = signing.dumps(obj=installation['data'], key=password)
            now = datetime.datetime.now()
            json = {
                'secret': enc_string,
                'username': self._user.username,
                'created': arrow.get(now).format(fmt='DD-MM-YYYY HH:mm:ss')
            }
            Creator(user=self._user).user_json(data=json)
            return True
        else:
            print('user should be deleted.\n%s' % self._user)
            self._user.delete()
            return False
