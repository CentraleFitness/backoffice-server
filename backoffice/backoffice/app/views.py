"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
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

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    logger.debug('contact')
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Page de contact.',
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
            'message':'Description de l\'application.',
            'year':datetime.now().year,
        }
    )
