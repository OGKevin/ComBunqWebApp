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
from Manager.views import Manager, managerForm
from BunqAPI.views import generate, decrypt, error
from . import views
from django.contrib.auth import views as auth_views

'''
Each app needs to get its own URL conf. It works fine this way but its not
ideal.
'''
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^account/register/$', views.register, name='register'),
    url(r'^account/logout/$', auth_views.logout, name='logout'),
    url(r'^Manager/(?i)$', Manager, name='Manager'),
    url(r'^Manager/form/(?i)$', managerForm, name='managerForm'),
    url(r'^generate/$', generate, name='generate'),
    url(r'^decrypt/$', decrypt, name='decrypt'),
    url(r'^decrypt/error/$', error, name='error'),
    url(r'^decrypt/error/(?P<error>.*)/$', error, name='error'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'', include('two_factor.urls', 'two_factor')),
] + static(settings.STATIC_URL)
