# from django.shortcuts import render
from django.views import View
# from pprint import pprint
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import json
from box import Box
from bunq_bot.main import MessagesHandler


# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class WebHook(View):

    def post(self, request):
        data = Box(json.loads(request.body.decode('utf-8')))
        # pprint(data)
        MessagesHandler(data).reply()
        return HttpResponse('ok')

    @staticmethod
    def handle_msg():
        pass
