"""MoneyWebApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from Manager.views import ManagerView, ManagerFormView
from BunqAPI.views import GenerateView, DecryptView, APIView, FileDownloader, RedirectView  # noqa
from BunqWebApp import views
from django.contrib.auth import views as auth_views

'''
Each app needs to get its own URL conf. It works fine this way but its not
ideal.
'''
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^account/register/$', views.RegisterView.as_view(), name='register'),
    url(r'^account/logout/$', auth_views.logout, name='logout'),
    url(r'^accounts/profile/$', RedirectView.as_view(), name='decrypt'),
    url(r'^Manager/(?i)$', ManagerView.as_view(), name='Manager'),
    url(r'^Manager/form/(?i)$', ManagerFormView.as_view(), name='managerForm'),
    url(r'^generate/$', GenerateView.as_view(), name='generate'),
    url(r'^decrypt/$', DecryptView.as_view(), name='decrypt'),
    url(r'^decrypt/download/(?P<action>[\w-]+)$', FileDownloader.as_view(), name='downloader'),  # noqa
    url(r'^API/(?P<selector>[\w-]+)$', APIView.as_view(), name='API'),  # noqa,
    url(r'^API/(?P<selector>[\w-]+)/(?P<userID>\d*)$', APIView.as_view(), name='API'),  # noqa,
    url(r'^API/(?P<selector>[\w-]+)/(?P<userID>\d*)/(?P<accountID>\d*)$', APIView.as_view(), name='API'),  # noqa,
    url(r'^captcha/', include('captcha.urls')),
    url(r'', include('two_factor.urls', 'two_factor')),
    # url(r'^.*$', views.RedirectView.as_view(), name='home'),
    # NOTE: this redirect is not working properly
] + static(settings.STATIC_URL)
