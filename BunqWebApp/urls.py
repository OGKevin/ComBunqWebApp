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
from BunqAPI.views import GenerateView, MyBunqView, APIView, RedirectView
from BunqWebApp import views
from filecreator.views import APIView as filecreator
from filecreator.views import FileDownloaderView as file_downlaoder
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
    url(r'^accounts/profile/$', RedirectView.as_view(), name='my_bunq'),
    url(r'^Manager/(?i)$', ManagerView.as_view(), name='Manager'),
    url(r'^Manager/form/(?i)$', ManagerFormView.as_view(), name='managerForm'),
    url(r'^generate/$', GenerateView.as_view(), name='generate'),
    url(r'^my_bunq/$', MyBunqView.as_view(), name='my_bunq'),
    url(r'^API/(?P<selector>[\w-]+)$', APIView.as_view()),  # noqa,
    url(r'^API/(?P<selector>[\w-]+)/(?P<user_id>\d*)$', APIView.as_view()),  # noqa,
    url(r'^API/(?P<selector>[\w-]+)/(?P<user_id>\d*)/(?P<account_id>\d*)$', APIView.as_view()),  # noqa,
    url(r'^API/(?P<selector>[\w-]+)/(?P<user_id>\d*)/(?P<account_id>\d*)/(?P<payment_id>\d*)$', APIView.as_view()),  # noqa,
    url(r'^API/(?P<selector>[\w-]+)/(?P<user_id>\d*)/(?P<account_id>\d*)/(?P<statement_format>[\w-]+)/(?P<date_start>[\w-]+)/(?P<date_end>[\w-]+)/(?P<regional_format>[\w-]+)$', APIView.as_view()),  # noqa,
    url(r'^API/filecreator/(?P<selector>[\w-]+)/(?P<extension>[\w-]+)$', filecreator.as_view(), name='API'),  # noqa
    url(r'^filecreator/download$', file_downlaoder.as_view(), name='API'),  # noqa,
    url(r'^captcha/', include('captcha.urls')),
    url(r'', include('two_factor.urls', 'two_factor')),
    # url(r'^.*$', views.RedirectView.as_view(), name='home'),
    # NOTE: this redirect is not working properly
] + static(settings.STATIC_URL)
