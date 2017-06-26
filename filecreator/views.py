# from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from filecreator.creator import Creator
import json
from django.contrib.sessions.models import Session
import os
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.


class APIView(View):
    """docstring for APIView."""

    def post(self, request, selector, extension):
        data = json.loads(request.POST['json'])
        user = User.objects.get(username=request.user)
        crt = Creator(user, extension)
        return HttpResponse(json.dumps(getattr(crt, selector.strip('/'))(data)))  # noqa


@method_decorator(login_required, name='dispatch')
class FileDownloaderView(View):
    """docstring for FileDownloaderView."""
    # @login_required(login_url='/accounts/login/')
    def get(self, request):
        user = User.objects.get(username=request.user)
        file_path = Session.objects.get(
            session_key=user.tokens.file_token
        ).get_decoded()["file_path"]

        file_name = os.path.basename(file_path).split('-pr-')
        print(file_name)
        if len(file_name) >= 3:
            transaction_id = "_%s" % file_name[1]
        else:
            transaction_id = None

        file_extension = os.path.splitext(file_path)[1]

        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(),
                                    content_type="application/force-download")
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(  # noqa
                                'ComBunqWebApp_%s%s%s' % (user, transaction_id,
                                                          file_extension))
            try:
                return response
            # except Exception as e:
            #     raise
            finally:
                os.remove(file_path)
