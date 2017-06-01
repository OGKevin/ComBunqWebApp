from django.shortcuts import render
from BunqAPI.forms import GenerateKeyForm, MyBunqForm
from BunqAPI.installation import installation
from BunqAPI.callbacks import callback
from django.utils.decorators import method_decorator
from django.utils.encoding import smart_str
from django.http import HttpResponse
# from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django_otp.decorators import otp_required
from django.contrib.sessions.models import Session
from django.views import View
from django.views.generic.base import RedirectView
import json
import os
from pprint import pprint

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


@method_decorator(otp_required, name='dispatch')
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
            form_data = form.cleaned_data

            generate_data = installation(
                user,
                form_data['encryption_password'],
                form_data['API']
            ).encrypt()

            registration = callback(
                json.loads(generate_data),
                user,
                form_data['encryption_password'],
            ).register()

            if registration.status_code is 200:
                response = HttpResponse(
                    generate_data, content_type='application/force-download')
                response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('BunqWebApp.json')  # noqa

                user.save()
            else:
                error = {
                    "Error": [{
                        "error_description_translated": 'something whent wrong while registering your API key wiht the bunq servers'  # noqa
                    }]
                }
                response = HttpResponse(json.dumps(error))
            return response

        else:
            return render(request, self.template, {'form': form})


@method_decorator(otp_required, name='dispatch')
class MyBunqView(View):
    """docstring for MyBunqView.
        Shows the template on the my_bunq page.
    """
    form = MyBunqForm
    template = 'BunqAPI/my_bunq.html'

    def get(self, request):
        form = self.form()
        return render(request, self.template, {'form': form})


@method_decorator(otp_required, name='dispatch')
class APIView(View):
    """docstring for APIView.
    API that handles post requests to make calls to the bunq api.
    """

    __variables = ['user_id', 'account_id', 'payment_id',
                   'date_start', 'date_end', 'statement_format',
                   'regional_format', 'selector'
                   ]

    def post(self, request, **kwargs):
        file_contents = json.loads(request.POST['json'])
        encryption_password = request.POST['pass']
        user = User.objects.get(username=request.user)

        # self._kwargs_setter(kwargs)

        if file_contents['userID'] in user.profile.GUID:
            try:
                API = callback(
                    file_contents,
                    user,
                    encryption_password,
                    **kwargs
                    # self.user_id,
                    # self.account_id,
                    # self.payment_id,
                    # self.date_start,
                    # self.date_end,
                    # self.statement_format,
                    # self.regional_format
                )
            except UnicodeDecodeError:
                error = {
                    "Error": [
                        {"error_description_translated": "During decpyting something whent wrong, maybe you entreded a wrong password?"}  # noqa
                        ]

                     }
                return HttpResponse(json.dumps(error))
            else:
                response = getattr(API, kwargs.get('selector').strip('/'))()
                return HttpResponse(json.dumps(response))
        else:  # pragma: no cover
            error = {
                'Error': [{'error_description_translated': 'This file is not yours to use.'}]  # noqa
                }
            return HttpResponse(json.dumps(error))

    def _kwargs_setter(self, kwargs):
        for k in self.__variables:
            if kwargs.get(k) is not None:
                setattr(self, k, kwargs.get(k))
            else:
                setattr(self, k, None)


@method_decorator(otp_required, name='dispatch')
class FileDownloader(View):
    """docstring for FileDownloader.
    Handles downloading files via GET.
    """

    def get(self, request, action):
        user = User.objects.get(username=request.user)
        return getattr(self, action.strip('/'))(user)

    def invoice(self, user):
        file_path = Session.objects.get(
            session_key=user.profile.invoice_token
        ).get_decoded()['invoice_pdf']

        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/force-download")  # noqa
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('BunqWebApp_invoice.pdf')  # noqa
            try:
                return response
            # except Exception as e:
            #     raise
            finally:
                os.remove(file_path)
