from django.shortcuts import render
from BunqAPI.forms import GenerateKeyForm, MyBunqForm
from BunqAPI.installation import Installation
from BunqAPI.callbacks import callback
from django.http import HttpResponse
# from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic.base import RedirectView
import json
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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
                                            password=self._password)

                if registration.status:
                    response = render(request, 'registration/complete.html')
                else:
                    response = json.dumps({
                        "Error": [{
                            "error_description_translated": 'something whent wrong while registering your API key wiht the bunq servers'  # noqa
                        }]
                    })
                return response

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
        callback(user)
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

        #
        # if file_contents['userID'] in user.profile.GUID:
        #     try:
        #         API = callback(
        #             user,
        #             **kwargs
        #         )
        #     except UnicodeDecodeError:
        #         error = {
        #             "Error": [
        #                 {"error_description_translated": "During decpyting something whent wrong, maybe you entreded a wrong password?"}  # noqa
        #                 ]
        #
        #              }
        #         return HttpResponse(json.dumps(error))
        #     else:
        #         response = getattr(API, kwargs.get('selector').strip('/'))()
        #         return HttpResponse(json.dumps(response))
        # else:  # pragma: no cover
        #     error = {
        #         'Error': [{'error_description_translated': 'This file is not yours to use.'}]  # noqa
        #         }
        #     return HttpResponse(json.dumps(error))
