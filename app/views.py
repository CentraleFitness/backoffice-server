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
from .forms import apiKeyForm, GymForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


from app.models import MongoHandler

import bson
import random
import string
import logging
import requests

logger = logging.getLogger(__name__)

ACK = {
    'ADD_GENERIC_KO': 0,
    'ADD_OK': 1,
    'ADD_FAIL': 2,
    'UPDATE_GENERIC_KO': 10,
    'UPDATE_OK': 11,
    'UPDATE_FAIL': 12,
    # 20, 21, 22
    'DELETE_GENERIC_KO': 30,
    'DELETE_OK': 31,
    'DELETE_FAIL': 32,
    'SEND_GENERIC_KO': 40,
    'SEND_OK': 41,
    'SEND_FAIL': 42
}

@login_required
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Accueil',
            'year':datetime.now().year
        })

@login_required
@require_POST
def send_api_email(request):
    ack = 40
    ret = requests.post('http://127.0.0.1:4456/send_email', data={
        'cf': 42,
        'id': request.POST['id']
        })
    print(ret)
    return redirect('manage_gym', ack)

@login_required
@require_POST
def send_newsletter_email(request):
    ack = 50
    ret = requests.post('http://127.0.0.1:4456/send_notification', data={
        'cf': 43,
        'id': request.POST['id']
        })
    print(ret)
    return redirect('manage_gym', ack)

@login_required
@require_POST
def delete_gym(request):
    db = MongoCollection('fitness_centers', 'centralefitness', 'localhost', 27017)
    ack = 30
    ret = db.collection.delete_one({'_id': bson.ObjectId(request.POST['id'])})
    ack = 31 if ret.deleted_count > 0 else 32
    return redirect('manage_gym', ack)

@login_required
@require_POST
def add_gym(request):
    db = MongoCollection('fitness_centers', 'centralefitness', 'localhost', 27017)
    form = GymForm(request.POST)
    ack = 0
    if form.is_valid():
        ret = db.collection.insert_one({
            'apiKey': ''.join(random.choice('abcdef' + string.digits) for _ in range(24)),
            'name': form.cleaned_data['name'],
            'description': form.cleaned_data['desc'],
            'address': form.cleaned_data['address'],
            'address_second': form.cleaned_data['alt_address'],
            'zip_code': form.cleaned_data['zip'],
            'city': form.cleaned_data['city'],
            'phone_number': form.cleaned_data['phone'],
            'email': form.cleaned_data['email']
            })
        ack = 1 if ret.acknowledged else 2
    return redirect('manage_gym', ack)


@login_required
@require_POST
def update_field(request):
    db = MongoCollection('fitness_centers', 'centralefitness', 'localhost', 27017)
    ack = 10
    ret = db.collection.update_one(
        {
            "_id": bson.ObjectId(request.POST['id'])
        },
        {
            "$set": {
                request.POST['field']: request.POST['new_value']
            }
        })
    ack = 11 if ret.modified_count > 0 else 12
    return redirect('manage_gym', ack)

@login_required
@require_POST
def edit_field(request):
    object_id = request.POST['id']
    field_name = request.POST['field']
    value = request.POST['value']
    return render(
        request,
        'app/edit_field.html',
        {
            'title': 'Edition',
            'id': object_id,
            'field': field_name,
            'value': value
        })

def connect_error(request):
    return render(request, 'app/connect_error.html')

@login_required
def manage_gym(request, ack: int=-1):
    db = MongoHandler(
        'localhost',
        27017,
        collection='fitness_centers',
        db='centralefitness')
    if not db.ping():
        return redirect('connect_error')
    items = db.collection.find()
    gyms = list()
    for gym in items:
        gym['id'] = gym.pop('_id')
        gyms.append(gym)
    gym_form = GymForm()
    return render(
        request,
        'app/manage_gym.html',
        {
            'title': 'Gestion',
            'gyms': gyms,
            'year': datetime.now().year,
            'form': gym_form,
            'ack': ack
        })
