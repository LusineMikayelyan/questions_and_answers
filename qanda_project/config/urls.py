"""Task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.views.generic.base import RedirectView
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import path


admin.site.site_header = _('Questions and Answers')
admin.site.site_title = _('Questions and Answers')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='/home', permanent=True)),
    url(r'^home/?', include(('base_app.urls', 'base_app'))),
    url(r'^questions_and_answers/?', include(('qanda_app.urls', 'qanda_app'))),
    url('^signup/', CreateView.as_view(
            template_name='registration/signup.html',
            form_class=UserCreationForm,
            success_url='/home'
    )),
    path('accounts/', include('django.contrib.auth.urls')),
]
