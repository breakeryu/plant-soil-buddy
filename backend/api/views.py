from django.views.generic import TemplateView
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.cache import never_cache

from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

import json
import random
import decimal

from .models import *
from django.contrib.auth.models import User

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer



class PostsView(ListAPIView):
    authentication_class = (JSONWebTokenAuthentication,) # Don't forget to add a 'comma' after first element to make it a tuple
    permission_classes = (IsAuthenticated,)

moist = 0
acidity = 7
fertility = 0

#@ensure_csrf_cookie
@csrf_exempt
def home(request):
    return render(request, 'index.html')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            user = None

        if user :
            return HttpResponse('User already Exists')
        else :
            #encrypt_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            
            new_user = User(username=data['username'],password=data['password'])
            new_user.save()

            return HttpResponse('Success')
    else:
        return None

@csrf_exempt
def user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return None
        return HttpResponse(data['username'])
    else:
        return None

def get_current_moist():
    curr_moist = float(decimal.Decimal(random.randrange(4155, 9389))/100)
    global moist
    moist = curr_moist
    return curr_moist

@csrf_exempt
def get_moist_as_value(request):
    return HttpResponse(get_current_moist())

@csrf_exempt
def get_moist_as_stats(request):
    column_1 = 'time'
    column_2 = '%'
    chart_data = {
        'columns': [column_1, column_2],
        'rows': [

                {column_1: '08:00', column_2: 100},
                {column_1: '09:00', column_2: 70},
                {column_1: '10:00', column_2: 80},
                {column_1: '13:00', column_2: 50},
                {column_1: '14:00', column_2: 60},
                {column_1: '15:00', column_2: 40},
                
                
            ]
    }
    return JsonResponse(chart_data)

def get_current_acidity():
    curr_acidity = float(decimal.Decimal(random.randrange(400, 1000))/100)
    global acidity
    acidity = curr_acidity
    return curr_acidity

@csrf_exempt
def get_acidity_as_value(request):
    return HttpResponse(get_current_acidity())

@csrf_exempt
def get_acidity_as_stats(request):
    column_1 = 'time'
    column_2 = 'pH'
    chart_data = {
        'columns': [column_1, column_2],
        'rows': [

                {column_1: '08:00', column_2: 14},
                {column_1: '09:00', column_2: 13},
                {column_1: '10:00', column_2: 11},
                {column_1: '13:00', column_2: 9},
                {column_1: '14:00', column_2: 8},
                {column_1: '15:00', column_2: 7},
                
                
            ]
    }
    return JsonResponse(chart_data)

def get_current_fertility():
    curr_fertility = float(decimal.Decimal(random.randrange(1000, 10000))/100)
    global fertility
    fertility = curr_fertility
    return curr_fertility

@csrf_exempt
def get_fertility_as_value(request):
    return HttpResponse(get_current_fertility())

@csrf_exempt
def get_fertility_as_stats(request):
    column_1 = 'time'
    column_2 = '%'
    chart_data = {
        'columns': [column_1, column_2],
        'rows': [

                {column_1: '08:00', column_2: 100},
                {column_1: '09:00', column_2: 70},
                {column_1: '10:00', column_2: 60},
                {column_1: '13:00', column_2: 50},
                {column_1: '14:00', column_2: 60},
                {column_1: '15:00', column_2: 55},
                
                
            ]
    }
    return JsonResponse(chart_data)

@csrf_exempt
def get_recommended_plants(request):
    global moist
    global acidity
    global fertility
    plants_list = [
                    {'id':0, 'name':'Banana'},
                    {'id':1, 'name':'Apple'},
                    {'id':2, 'name':'Papaya'}
                ]
    return JsonResponse(plants_list, safe=False)

def public(request):
    return HttpResponse("You don't need to be authenticated to see this")


@api_view(['GET'])
def private(request):
    return HttpResponse("You should not see this message if not authenticated!")


