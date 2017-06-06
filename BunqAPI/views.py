from django.shortcuts import render
from BunqAPI.forms import GenerateKeyForm, MyBunqForm
from BunqAPI.installation import Installation
from BunqAPI.callbacks import callback
from django.http import HttpResponse, HttpResponseForbidden
# from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic.base import RedirectView
import json
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


# from pprint import pprint

# from django.http.response import FileResponse

# Create your views here.


class RedirectView(RedirectView):
    """docstring for RedirectView.
    Redirects /accounts/porfile to /my_bunq
    """
    permanent = False
    pattern_name = 'my_bunq'

    def get_redirct_url(self):
        return super().get_redirct_url()


@method_decorator(login_required, name='dispatch')
class GenerateView(View):
    """docstring for GenerateView.
    This view handesl generating new JSON file and register the credentials
    with the bunq servers.
    """
    generate_form = GenerateKeyForm
    template = 'BunqAPI/index.html'

    def get(self, request):
        form = self.generate_form()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.generate_form(request.POST)
        user = User.objects.get(username=request.user)

        if form.is_valid():
            self._username = request.user
            self._password = form.cleaned_data['user_password']
            api_key = form.cleaned_data['API']

            if self.authenticate_user():
                user = User.objects.get(username=self._username)
                registration = Installation(user=user, api_key=api_key,
                                            password=self._password,
                                            delete_user=False)

                if registration.status:
                    return render(request, 'registration/complete.html')
                else:
                    messages.error(request, ('something went wrong while '
                                             'registering your API key '
                                             'with the bunq servers'))
                    return render(request, self.template, {'form': form})
            else:
                messages.error(request, ('User authentication failed. '
                                         'This password is not the '
                                         'correct user password.'))
                return render(request, self.template, {'form': form})

        else:
            return render(request, self.template, {'form': form})

    def authenticate_user(self):
        user = authenticate(username=self._username,
                            password=self._password)

        if user is not None:
            return True
        else:
            return False


@method_decorator(login_required, name='dispatch')
class MyBunqView(View):
    """docstring for MyBunqView.
        Shows the template on the my_bunq page.
    """
    form = MyBunqForm
    template = 'BunqAPI/my_bunq.html'

    def get(self, request):
        form = self.form()
        user = User.objects.get(username=request.user)
        try:
            callback(user)
        except ObjectDoesNotExist:
            return HttpResponseForbidden('You are not logged in correctly.')
        return render(request, self.template, {'form': form})


@method_decorator(login_required, name='dispatch')
class APIView(View):
    """docstring for APIView.
    API that handles post requests to make calls to the bunq api.
    """

    def post(self, request, **kwargs):
        # # file_contents = json.loads(request.POST['json'])ß
        # # encryption_password = request.POST['pass']
        user = User.objects.get(username=request.user)
        API = callback(user, **kwargs)
        response = getattr(API, kwargs.get('selector').strip('/'))()
        return HttpResponse(json.dumps(response))
