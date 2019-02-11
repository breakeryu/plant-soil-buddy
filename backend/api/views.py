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

        if data['username'] == '' or data['password'] == '' or data['confirm_password'] == '' :
            return HttpResponse('Missing Fields')

        if not (data['password'] == data['confirm_password']) :
            return HttpResponse('Password Confirm Failed')
        
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            user = None

        if user :
            return HttpResponse('User Already Exists')
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
def get_soil_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            soil_profile = SoilProfile.objects.get(pk=data['soil_profile_id'])
        except SoilProfile.DoesNotExist:
            return None
                
        return JsonResponse({'id': soil_profile.id, 'name': soil_profile.name, 'location': soil_profile.location}, safe=False)
        
    else:
        return None

@csrf_exempt
def add_soil_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            owner = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return JsonResponse({'status': 400, 'message':'User does not exist'}, safe=False)
        
        name = data['name']
        location = data['location']

        SoilProfile.objects.create(owner=owner, name=name, location=location)

        return JsonResponse({'status': 200, 'message':'OK'}, safe=False)

    else:
        return None

@csrf_exempt
def edit_soil_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        soil_profile_id = data['soil_profile_id']
        name = data['name']
        location = data['location']
        try:
            SoilProfile.objects.filter(pk=soil_profile_id).update(name=name, location=location)
        except SoilProfile.DoesNotExist:
            return JsonResponse({'status': 400, 'message':'Soil Profile does not exist'}, safe=False)

        return JsonResponse({'status': 200, 'message':'OK'}, safe=False)

    else:
        return None

@csrf_exempt
def clear_soil_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        soil_profile_id = data['soil_profile_id']
        try:
            soil_profile = SoilProfile.objects.get(pk=soil_profile_id)
        except SoilProfile.DoesNotExist:
            return JsonResponse({'status': 400, 'message':'Soil Profile does not exist'}, safe=False)

        records = SensorRecord.objects.all()

        for record in records :
            if record.soil_profile == soil_profile :
                record.delete()

        return JsonResponse({'status': 200, 'message':'OK'}, safe=False)

    else:
        return None

@csrf_exempt
def delete_soil_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        soil_profile_id = data['soil_profile_id']
        try:
            soil_profile = SoilProfile.objects.get(pk=soil_profile_id)

            soil_profile.delete()
            
        except SoilProfile.DoesNotExist:
            return JsonResponse({'status': 400, 'message':'Soil Profile does not exist'}, safe=False)

        return JsonResponse({'status': 200, 'message':'OK'}, safe=False)

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
        
        #moist = int(arduino.readline())
        #acidity = float(decimal.Decimal(random.randrange(500, 700))/100)
        #fertility = float(decimal.Decimal(random.randrange(7000, 9000))/100)

        values = str(arduino.readline()).split(" ")

        moist = int(values[0].split("b'")[1])
        acidity = float(values[1])
        fertility = int(values[2].split("\\r\\n")[0])

        if moist < 0:
            moist = 0

        if moist > 100:
            moist = 100

        if acidity < 0:
            acidity = 0

        if acidity > 14:
            acidity = 14

        if fertility < 0:
            fertility = 0

        if fertility > 100:
            fertility = 100
            
        soil_profile_on_use = SoilProfile.objects.get(pk=data['soil_profile_id'])

        record = SensorRecord.objects.create(soil_profile=soil_profile_on_use ,record_time=get_current_time(), moist=moist, ph=acidity, fertility=fertility)

        arduino.close()

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

    data = json.loads(request.body)

    soil_profile_on_use = SoilProfile.objects.get(pk=data['soil_profile_id'])

    records = SensorRecord.objects.all()

    moist_chart_data = {
    'columns': ['time', '%'],
    'rows': []
    }

    for record in records :
        time_record = f"{record.record_time:%Y-%b-%d, %H:%M:%S}"
        if record.soil_profile == soil_profile_on_use :
            moist_chart_data["rows"].append({'time':time_record, '%':record.moist})
    
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

    data = json.loads(request.body)

    soil_profile_on_use = SoilProfile.objects.get(pk=data['soil_profile_id'])

    records = SensorRecord.objects.all()

    acidity_chart_data = {
    'columns': ['time', 'pH'],
    'rows': []
    }

    for record in records :
        time_record = f"{record.record_time:%Y-%b-%d, %H:%M:%S}"
        if record.soil_profile == soil_profile_on_use :
            acidity_chart_data["rows"].append({'time':time_record, 'pH':record.ph})
    
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

    data = json.loads(request.body)

    soil_profile_on_use = SoilProfile.objects.get(pk=data['soil_profile_id'])

    records = SensorRecord.objects.all()

    fertility_chart_data = {
    'columns': ['time', '%'],
    'rows': []
    }

    for record in records :
        time_record = f"{record.record_time:%Y-%b-%d, %H:%M:%S}"
        if record.soil_profile == soil_profile_on_use :
            fertility_chart_data["rows"].append({'time':time_record, '%':record.fertility})
    
    chart_data = fertility_chart_data
    return JsonResponse(chart_data)





@csrf_exempt
def get_average_moist(request):
    global avg_moist

    data = json.loads(request.body)

    soil_profile_on_use = SoilProfile.objects.get(pk=data['soil_profile_id'])

    records = SensorRecord.objects.all()
    target_records = []
    
    total_moist_data = 0

    for record in records :
        if record.soil_profile == soil_profile_on_use :
            total_moist_data += record.moist
            target_records.append(record)
            
    if len(target_records) > 0 :
        avg_moist = total_moist_data / len(target_records)
    else :
        avg_moist = 0
    
    return HttpResponse(round_two_decimal_digits(avg_moist))

@csrf_exempt
def get_average_acidity(request):
    global avg_acidity

    data = json.loads(request.body)

    soil_profile_on_use = SoilProfile.objects.get(pk=data['soil_profile_id'])

    records = SensorRecord.objects.all()
    target_records = []
    
    total_acidity_data = 0

    for record in records :
        if record.soil_profile == soil_profile_on_use :
            total_acidity_data += record.ph
            target_records.append(record)
            
    if len(target_records) > 0 :
        avg_acidity = total_acidity_data / len(target_records)
    else :
        avg_acidity = 0

    return HttpResponse(round_two_decimal_digits(avg_acidity))

@csrf_exempt
def get_average_fertility(request):
    global avg_fertility

    data = json.loads(request.body)

    soil_profile_on_use = SoilProfile.objects.get(pk=data['soil_profile_id'])

    records = SensorRecord.objects.all()
    target_records = []
    
    total_fertility_data = 0

    for record in records :
        if record.soil_profile == soil_profile_on_use :
            total_fertility_data += record.fertility
            target_records.append(record)
            
    if len(target_records) > 0 :
        avg_fertility = total_fertility_data / len(target_records)
    else :
        avg_fertility = 0

    return HttpResponse(round_two_decimal_digits(avg_fertility))


@csrf_exempt
def get_recommended_plants(request):
    data = json.loads(request.body)

    soil_profile_on_use = SoilProfile.objects.get(pk=data['soil_profile_id'])

    records = SensorRecord.objects.all()
    target_records = []

    total_moist_data = 0
    total_acidity_data = 0
    total_fertility_data = 0

    for record in records :
        if record.soil_profile == soil_profile_on_use :
            total_moist_data += record.moist
            total_acidity_data += record.ph
            total_fertility_data += record.fertility
            target_records.append(record)
            
    if len(target_records) > 0 :
        avg_moist = total_moist_data / len(target_records)
        avg_acidity = total_acidity_data / len(target_records)
        avg_fertility = total_fertility_data / len(target_records)
    else :
        avg_moist = 0
        avg_acidity = 0
        avg_fertility = 0

    plants_set = Plant.objects.all()
    plants_list = []
    
    for plant in plants_set :
        if avg_moist < plant.min_moist or avg_moist > plant.max_moist or avg_acidity < plant.min_ph or avg_acidity > plant.max_ph or avg_fertility < plant.min_fertility or avg_fertility > plant.max_fertility :
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

            arduino.close()
           
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


