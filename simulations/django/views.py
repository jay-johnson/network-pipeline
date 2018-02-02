import logging
from django.http import Http404
from django.shortcuts import render


log = logging.getLogger("django")


def home(request):
    log.info(("home - req={}")
             .format(request))
    return render(request, 'home.html', {})


def index(request):
    log.info(("index - req={}")
             .format(request))
    return render(request, 'base.html', {})


def profile(request):
    log.info(("profile - req={}")
             .format(request))
    return render(request, 'profile.html', {})
