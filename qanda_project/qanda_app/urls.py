from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^start/', views.start_questionnaire, name='start'),
    url(r'^action/', views.ActionView.as_view(), name='action'),
    url(r'^best_results/', views.best_results, name='best_results'),
]