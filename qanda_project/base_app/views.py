from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


@login_required
def index(request, *args, **kwargs):
    return render(request, 'base_app/home.html', {})


class RedirectModelView(View):
    def post(self, request, *args, **kwargs):
        if "home" in request.POST:
            return HttpResponseRedirect(reverse('base_app:base'))
        elif "qanda" in request.POST:
            return HttpResponseRedirect(reverse('qanda_app:start'))
        elif "best_results" in request.POST:
            return HttpResponseRedirect(reverse('qanda_app:best_results'))

        return HttpResponse("Page not found")
