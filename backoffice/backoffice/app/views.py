"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.utils import timezone
from datetime import timedelta, date
from django.shortcuts import redirect
from datetime import datetime
from .models import apiKey
from .forms import apiKeyForm
from django.contrib.auth.decorators import login_required

import logging

logger = logging.getLogger(__name__)

@login_required
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    logger.debug('home')
    return render(
        request,
        'app/index.html',
        {
            'title':'Accueil',
            'year':datetime.now().year,
        }
    )

@login_required
def manage_key(request):
    number_row = apiKey.objects.count()
    keys = apiKey.objects.all()
    return render(
        request,
        'app/manage_key.html',
        {
            'keys' : keys,
            'year':datetime.now().year,
        }
    )

@login_required
def new_key(request):
    if request.method == "POST":
        form = apiKeyForm(request.POST)
        if form.is_valid():
            apiKey.objects.all().delete()
            key = form.save(commit=False)
            key.date_creation = datetime.now()
            current_year = datetime.now().year
            now = datetime.now()
            key.date_expiration = datetime(current_year + 1, now.month, now.day, now.hour, now.minute, now.second)
            key.save()
            return redirect('manage_key')
    else:
        form = apiKeyForm()
    return render (
        request,
        'app/new_key.html',
        {
            'form' : form,
            'year' : datetime.now().year,
         }
    )

def support(request):
    """Renders the support page."""
    assert isinstance(request, HttpRequest)
    logger.debug('support')
    return render(
        request,
        'app/support.html',
        {
            'title':'support',
            'message':'',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    logger.debug('about')
    return render(
        request,
        'app/about.html',
        {
            'title':'A Propos',
            'message':' ',
            'year':datetime.now().year,
        }
    )
