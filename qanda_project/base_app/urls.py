from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='base'),
    url(r'^redirect_to/$', views.RedirectModelView.as_view(), name='redirect_to'),
]
