from django.shortcuts import render
# from .form import login_form
# from django.http import HttpResponse
# from django.contrib.auth import authenticate, login
# from django.http import HttpResponse
# from django.template import loader

# Create your views here.


def home(request):
    return render(request, 'Home/index.html')
