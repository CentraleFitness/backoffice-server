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
    keys = apiKey.objects.all()
    return render(
        request,
        'app/manage_key.html',
        {
            'keys': keys,
            'form': form,
            'year':datetime.now().year,
        }
    )

def delete_key(request):
    if request.method == "POST":
        key_value = request.POST.get('api_key')
        nb_del, _ = apiKey.objects.get(api_key=key_value).delete()
    return redirect('manage_key')

@login_required
def support(request):
    """Render the Support page."""
    assert isinstance(request, HttpRequest)
    logger.debug('support')
    return render(
        request,
        'app/support.html',
        {
            'title': 'Support',
            'message': '',
        }
    )
