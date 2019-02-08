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

from datetime import datetime 

import json
import math
import random
import decimal
import serial

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

moist_chart_data = {
    'columns': ['time', '%'],
    'rows': []
}

acidity_chart_data = {
    'columns': ['time', 'pH'],
    'rows': []
}

fertility_chart_data = {
    'columns': ['time', '%'],
    'rows': []
}

avg_moist = 0
avg_acidity = 7
avg_fertility = 0

def round_two_decimal_digits(number) :
    return math.ceil(number*100)/100

def get_current_time() :
    return f"{datetime.now():%Y-%m-%d %H:%M:%S}"

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

@csrf_exempt
def get_soil_profiles(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return None

        soil_profiles = SoilProfile.objects.all()
        current_soil_profiles = []

        for soil_profile in soil_profiles :
            if soil_profile.owner == user :
                current_soil_profiles.append({'id': soil_profile.id, 'name': soil_profile.name, 'location': soil_profile.location})
                
        return JsonResponse(current_soil_profiles, safe=False)
        
    else:
        return None

@csrf_exempt
def get_all_values(request):
    global moist_chart_data
    global moist
    global acidity_chart_data
    global acidity
    global fertility_chart_data
    global fertility
    
    data = json.loads(request.body)
    try :
        arduino = serial.Serial(data['port'], 9600)
        
        moist = int(arduino.readline())
        acidity = float(decimal.Decimal(random.randrange(500, 700))/100)
        fertility = float(decimal.Decimal(random.randrange(7000, 9000))/100)

        if moist < 0:
            moist = 0

        if acidity < 0:
            acidity = 0

        if acidity > 14:
            acidity = 14

        if fertility < 0:
            fertility = 0

        soil_profile_on_use = SoilProfile.objects.get(pk=data['soil_profile_id'])

        record = SensorRecord.objects.create(soil_profile=soil_profile_on_use ,record_time=get_current_time(), moist=moist, ph=acidity, fertility=fertility)

        #moist_chart_data["rows"].append({'time':get_current_time(), '%':moist})
        #if len(moist_chart_data["rows"]) > 10 :
        #    moist_chart_data["rows"].pop(0)

        #acidity_chart_data["rows"].append({'time':get_current_time(), 'pH':acidity})
        #if len(acidity_chart_data["rows"]) > 10 :
        #    acidity_chart_data["rows"].pop(0)

        #fertility_chart_data["rows"].append({'time':get_current_time(), '%':fertility})
        #if len(fertility_chart_data["rows"]) > 10 :
        #    fertility_chart_data["rows"].pop(0)

        return HttpResponse(1)
            
    except serial.serialutil.SerialException :
        return HttpResponse(-999)


@csrf_exempt
def get_moist_as_value(request):
    global moist

    value = moist
    return HttpResponse(value)

@csrf_exempt
def get_moist_as_stats(request):
    global moist_chart_data
    
    chart_data = moist_chart_data
    return JsonResponse(chart_data)





@csrf_exempt
def get_acidity_as_value(request):
    global acidity

    value = acidity
    return HttpResponse(value)

@csrf_exempt
def get_acidity_as_stats(request):
    global acidity_chart_data

    chart_data = acidity_chart_data
    return JsonResponse(chart_data)





@csrf_exempt
def get_fertility_as_value(request):
    global fertility

    value = fertility
    return HttpResponse(value)

@csrf_exempt
def get_fertility_as_stats(request):
    global fertility_chart_data

    chart_data = fertility_chart_data
    return JsonResponse(chart_data)





@csrf_exempt
def get_average_moist(request):
    global moist_chart_data
    global avg_moist
    
    total_moist_data = 0
    for moist_data in moist_chart_data["rows"] :
        total_moist_data += moist_data["%"]
        
    if len(moist_chart_data["rows"]) > 0 :
        avg_moist = total_moist_data / len(moist_chart_data["rows"])
    else :
        avg_moist = 0
    
    return HttpResponse(round_two_decimal_digits(avg_moist))

@csrf_exempt
def get_average_acidity(request):
    global acidity_chart_data
    global avg_acidity

    total_acidity_data = 0
    for acidity_data in acidity_chart_data["rows"] :
        total_acidity_data += acidity_data["pH"]
        
    if len(acidity_chart_data["rows"]) > 0 :
        avg_acidity = total_acidity_data / len(acidity_chart_data["rows"])
    else :
        avg_acidity = 0

    return HttpResponse(round_two_decimal_digits(avg_acidity))

@csrf_exempt
def get_average_fertility(request):
    global fertility_chart_data
    global avg_fertility

    total_fertility_data = 0
    for fertility_data in fertility_chart_data["rows"] :
        total_fertility_data += fertility_data["%"]

    if len(fertility_chart_data["rows"]) > 0 : 
        avg_fertility = total_fertility_data / len(fertility_chart_data["rows"])
    else :
        avg_fertility = 0

    return HttpResponse(round_two_decimal_digits(avg_fertility))


@csrf_exempt
def get_recommended_plants(request):
    global avg_moist
    global avg_acidity
    global avg_fertility

    #moist = moist_chart_data["rows"][-1]["%"]
    #acidity = acidity_chart_data["rows"][-1]["pH"]
    #fertility = fertility_chart_data["rows"][-1]["%"]

    moist = avg_moist
    acidity = avg_acidity
    fertility = avg_fertility

    plants_set = Plant.objects.all()
    plants_list = []
    
    for plant in plants_set :
        if moist < plant.min_moist or moist > plant.max_moist or acidity < plant.min_ph or acidity > plant.max_ph or fertility < plant.min_fertility or fertility > plant.max_fertility :
            continue
        plants_list.append({'id':plant.id, 'name':plant.name})

    return JsonResponse(plants_list, safe=False)



@csrf_exempt
def snap_reset(request):
    global moist, acidity, fertility
    global moist_chart_data, acidity_chart_data, fertility_chart_data
    global avg_moist, avg_acidity, avg_fertility
    
    moist = 0
    acidity = 7
    fertility = 0

    moist_chart_data = {
        'columns': ['time', '%'],
        'rows': []
    }

    acidity_chart_data = {
        'columns': ['time', 'pH'],
        'rows': []
    }

    fertility_chart_data = {
        'columns': ['time', '%'],
        'rows': []
    }

    avg_moist = 0
    avg_acidity = 7
    avg_fertility = 0

    return HttpResponse('Reset')

@csrf_exempt
def get_connection_status(request):
    status = 'Unknown'
    
    if request.method == 'POST':
        data = json.loads(request.body)
        
        try :
            arduino = serial.Serial(data['port'], 9600)

            status = 'Connected'
           
        except serial.serialutil.SerialException :
            status = 'Disconnected'

    else :
        status = 'Disconnected'

    return HttpResponse(status)


def public(request):
    return HttpResponse("You don't need to be authenticated to see this")


@api_view(['GET'])
def private(request):
    return HttpResponse("You should not see this message if not authenticated!")


