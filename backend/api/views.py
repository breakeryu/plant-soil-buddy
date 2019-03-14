from django.views.generic import TemplateView
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
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
from pyswip import Prolog

import json
import math
import random
import decimal
import serial
import re
import csv
import xlrd
import os

from .models import *
from django.contrib.auth.models import User

import gzip
from pathlib import Path
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)

import numpy as np
from scipy.spatial.distance import cdist
#from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
#from sklearn.cluster import MeanShift
#from sklearn.mixture import GaussianMixture
#from sklearn.cluster import DBSCAN
from scipy.cluster.hierarchy import fcluster
from scipy.cluster.hierarchy import dendrogram, linkage



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
#fertility = 0

moist_chart_data = {
    'columns': ['time', '%'],
    'rows': []
}

acidity_chart_data = {
    'columns': ['time', 'pH'],
    'rows': []
}

#fertility_chart_data = {
#    'columns': ['time', '%'],
#    'rows': []
#}

avg_moist = 0
avg_acidity = 7
#avg_fertility = 0

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
            return HttpResponseBadRequest("Missing Fields")

        if len(data['username']) > 150 :
            return HttpResponseBadRequest('Username exceeds 150 characters')

        set_of_invalid_characters = re.findall('[^a-zA-Z0-9@/./+-/_]',data['username'])

        if len(set_of_invalid_characters) > 0 :
            return HttpResponseBadRequest('Username contains invalid characters')

        if data['username'] == data['password'] :
            return HttpResponseBadRequest('Password is too similar to your personal information')

        if len(data['password']) < 8 :
            return HttpResponseBadRequest('Password must be at least 8 characters')

        password_list_path=Path(__file__).resolve().parent / 'common-passwords.txt.gz'
        try:
            with gzip.open(str(password_list_path)) as f:
                common_passwords_lines = f.read().decode().splitlines()
        except OSError:
            with open(str(password_list_path)) as f:
                common_passwords_lines = f.readlines()
        passwords = {p.strip() for p in common_passwords_lines}
        if data['password'].lower().strip() in passwords:
            return HttpResponseBadRequest('This Password is too common')

        try:
            pass_num = int(data['password'])
            is_numeric = True
        except ValueError:
            is_numeric = False
        if is_numeric :
            return HttpResponseBadRequest('Password is entirely numeric')

        if not (data['password'] == data['confirm_password']) :
            return HttpResponseBadRequest('Password Confirm Failed')
        
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            user = None

        if user :
            return HttpResponseBadRequest('User Already Exists')
        else :
            #encrypt_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            
            new_user = User(username=data['username'],password=data['password'])
            new_user.save()

            return HttpResponse('Success')
    else:
        return None
    
@csrf_exempt
def change_password(request) :
    if request.method == 'POST':
        data = json.loads(request.body)

        user = User.objects.get(username=data['username'])

        if not user.password == data['old_password'] :
            return HttpResponseBadRequest('Incorrect old password')
    
        if data['username'] == data['password'] :
            return HttpResponseBadRequest('Password is too similar to your personal information')

        if len(data['password']) < 8 :
            return HttpResponseBadRequest('Password must be at least 8 characters')

        password_list_path=Path(__file__).resolve().parent / 'common-passwords.txt.gz'
        try:
            with gzip.open(str(password_list_path)) as f:
                common_passwords_lines = f.read().decode().splitlines()
        except OSError:
            with open(str(password_list_path)) as f:
                common_passwords_lines = f.readlines()
        passwords = {p.strip() for p in common_passwords_lines}
        if data['password'].lower().strip() in passwords:
            return HttpResponseBadRequest('This Password is too common')

        try:
            pass_num = int(data['password'])
            is_numeric = True
        except ValueError:
            is_numeric = False
        if is_numeric :
            return HttpResponseBadRequest('Password is entirely numeric')

        if not (data['password'] == data['confirm_password']) :
            return HttpResponseBadRequest('Password Confirm Failed')

        try:
            User.objects.filter(pk=user.id).update(password=data['password'])
        except User.DoesNotExist:
            return HttpResponseBadRequest('User does not exist')

        return HttpResponse('Success')

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
def user_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return None
        return JsonResponse({'usernmae':data['username'], 'email':user.email, 'is_staff':str(user.is_staff)}, safe=False)
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
            return HttpResponseBadRequest('User does not exist')
        
        name = data['name']
        location = data['location']

        if name == '' or location == '' :
            return HttpResponseBadRequest("Missing Fields")

        SoilProfile.objects.create(owner=owner, name=name, location=location)

        return HttpResponse('Success')

    else:
        return None

@csrf_exempt
def edit_soil_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        soil_profile_id = data['soil_profile_id']
        name = data['name']
        location = data['location']

        if soil_profile_id == '' or name == '' or location == '' :
            return HttpResponseBadRequest("Missing Fields")
        
        try:
            SoilProfile.objects.filter(pk=soil_profile_id).update(name=name, location=location)
        except SoilProfile.DoesNotExist:
            return HttpResponseBadRequest('Soil Profile does not exist')

        return HttpResponse('Success')

    else:
        return None

@csrf_exempt
def clear_soil_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        soil_profile_id = data['soil_profile_id']

        if soil_profile_id == '':
            return HttpResponseBadRequest("Missing Fields")
        
        try:
            soil_profile = SoilProfile.objects.get(pk=soil_profile_id)
        except SoilProfile.DoesNotExist:
            return HttpResponseBadRequest('Soil Profile does not exist')

        records = SensorRecord.objects.all()

        for record in records :
            if record.soil_profile == soil_profile :
                record.delete()

        return HttpResponse('Success')

    else:
        return None

@csrf_exempt
def delete_soil_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        soil_profile_id = data['soil_profile_id']

        if soil_profile_id == '':
            return HttpResponseBadRequest("Missing Fields")

        try:
            soil_profile = SoilProfile.objects.get(pk=soil_profile_id)

            soil_profile.delete()
            
        except SoilProfile.DoesNotExist:
            return HttpResponseBadRequest('Soil Profile does not exist')

        return HttpResponse('Success')

    else:
        return None

@csrf_exempt
def get_all_values(request):
    global moist_chart_data
    global moist
    global acidity_chart_data
    global acidity
    #global fertility_chart_data
    #global fertility
    
    data = json.loads(request.body)
    try :
        arduino = serial.Serial(data['port'], 9600)
        
        #moist = int(arduino.readline())
        #acidity = float(decimal.Decimal(random.randrange(500, 700))/100)
        #fertility = float(decimal.Decimal(random.randrange(7000, 9000))/100)

        values = str(arduino.readline()).split(" ")

        moist = int(values[0].split("b'")[1])
        acidity = float(values[1])
        #fertility = int(values[2].split("\\r\\n")[0])

        if moist < 0:
            moist = 0

        if moist > 100:
            moist = 100

        if acidity < 0:
            acidity = 0

        if acidity > 14:
            acidity = 14

        #if fertility < 0:
        #    fertility = 0

        #if fertility > 100:
        #    fertility = 100
            
        soil_profile_on_use = SoilProfile.objects.get(pk=data['soil_profile_id'])

        record = SensorRecord.objects.create(soil_id=soil_profile_on_use ,record_date=get_current_time(), moist=moist, ph=acidity)

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

    records = SensorRecord.objects.filter(soil_id=soil_profile_on_use)

    moist_chart_data = {
    'columns': ['time', '%'],
    'rows': []
    }

    for record in records :
        time_record = f"{record.record_date:%Y-%b-%d}"
        
        moist_chart_data["rows"].append({'time':str(record.id)+' '+time_record, '%':record.moist})
    
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

    records = SensorRecord.objects.filter(soil_id=soil_profile_on_use)

    acidity_chart_data = {
    'columns': ['time', 'pH'],
    'rows': []
    }

    for record in records :
        time_record = f"{record.record_date:%Y-%b-%d}"
        
        acidity_chart_data["rows"].append({'time':str(record.id)+' '+time_record, 'pH':record.ph})
    
    chart_data = acidity_chart_data
    return JsonResponse(chart_data)







@csrf_exempt
def get_average_moist(request):
    global avg_moist

    data = json.loads(request.body)

    soil_profile_on_use = SoilProfile.objects.get(pk=data['soil_profile_id'])

    records = SensorRecord.objects.filter(soil_id=soil_profile_on_use)
    target_records = []
    
    total_moist_data = 0

    for record in records :
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

    records = SensorRecord.objects.filter(soil_id=soil_profile_on_use)
    target_records = []
    
    total_acidity_data = 0

    for record in records :
        total_acidity_data += record.ph
        target_records.append(record)
            
    if len(target_records) > 0 :
        avg_acidity = total_acidity_data / len(target_records)
    else :
        avg_acidity = 0

    return HttpResponse(round_two_decimal_digits(avg_acidity))



def get_fresh_numpy_data_of_soil_profile(soil_profile_id) :
    
    soil_profile_on_use = SoilProfile.objects.get(pk=soil_profile_id)
    
    records = SensorRecord.objects.filter(soil_id=soil_profile_on_use)

    raw_chart_data = np.array([[float('NaN'),float('NaN')]])

    for record in records :
        values = np.array([[float(record.moist), float(record.ph)]])
        raw_chart_data = np.append(raw_chart_data, values, axis=0)

    fresh_numpy_data = raw_chart_data[~np.isnan(raw_chart_data).any(axis=1)]
    
    return fresh_numpy_data


def get_cluster_group_labels_and_most_frequent(fresh_numpy_data) :
    n = 3
        
    #get clusters
    #cluster = KMeans(n_clusters=3).fit(fresh_numpy_data)
    cluster = AgglomerativeClustering(linkage='ward', affinity='euclidean', n_clusters=n).fit(fresh_numpy_data)
    #cluster = MeanShift(bandwidth=2).fit(fresh_numpy_data)
    #cluster = GaussianMixture(n_components=3).fit(fresh_numpy_data)
    #cluster = DBSCAN(eps=3, min_samples=2).fit(fresh_numpy_data)

    cluster_labels = cluster.labels_
    #cluster_labels = cluster.weights_
    
    cluster_labels_compare = cluster_labels[cluster_labels >= 0]
    
    #print(cluster_labels)
    most_frequent_cluster_index = np.argmax(np.bincount(cluster_labels_compare))

    return cluster_labels, most_frequent_cluster_index


@csrf_exempt
def get_all_values_as_scatter(request):

    data = json.loads(request.body)

    fresh_numpy_data = get_fresh_numpy_data_of_soil_profile(data['soil_profile_id'])

    total_rows = fresh_numpy_data.shape[0]
    if total_rows <= 0 :
        return JsonResponse([], safe=False)

    cluster_labels, most_frequent_cluster_index = get_cluster_group_labels_and_most_frequent(fresh_numpy_data)

    i = 0
    chart_data = []
    for data_row in fresh_numpy_data :
        if cluster_labels[i] == most_frequent_cluster_index :
            good = '1'
        else :
            good = '0'
        chart_data.append({'moist':str(data_row[0]), 'acidity': str(data_row[1]), 'cluster_group': str(cluster_labels[i]), 'good':good})
        i += 1
    
    return JsonResponse(chart_data, safe=False)


@csrf_exempt
def get_good_moist_ph_values(request):
    data = json.loads(request.body)

    fresh_numpy_data = get_fresh_numpy_data_of_soil_profile(data['soil_profile_id'])
    
    total_rows = fresh_numpy_data.shape[0]
    if total_rows <= 0 :
        return JsonResponse([], safe=False)

    cluster_labels, most_frequent_cluster_index = get_cluster_group_labels_and_most_frequent(fresh_numpy_data)

    good_data_moist = []
    good_data_acidity = []
    #good_data_fertility = []

    i = 0
    for data_row in fresh_numpy_data :
        if cluster_labels[i] == most_frequent_cluster_index :
            good_data_moist.append(data_row[0])
            good_data_acidity.append(data_row[1])
            #good_data_fertility.append(data_row[2])
        i += 1
    
    avg_moist = (min(good_data_moist)+max(good_data_moist))/2
    avg_acidity = float((min(good_data_acidity)+max(good_data_acidity))/2)

    print(avg_moist)
    print(avg_acidity)

    return JsonResponse({'avg_good_moist':avg_moist, 'avg_good_acidity':avg_acidity}, safe=False)

#recommend(PL, NX, PX, KX, S, M, A) :- plant(PL),
    #   recommend_plant(PL, M, A),
    #   recommend_nutrient(A, NX, PX, KX),
    #   recommend_soil_type(PL, S).

@csrf_exempt
def get_recommendations(request):
    data = json.loads(request.body)

    avg_moist = float(data['good_avg_moist'])
    avg_acidity = float(data['good_avg_acidity'])

    soil_profile_on_use = SoilProfile.objects.get(pk=data['soil_profile_id'])

    #plants = Plant.objects.all()

    #Configs Facts

    #lvl(0, very_low).
    #lvl(1, low).
    #lvl(2, mid).
    #lvl(3, high).
    #lvl(4, very_high).

    lvl_config = ['very_low','low','mid','high','very_high']
    lvl_config_to_index = {'very_low':'0','low':'1','mid':'2','high':'3','very_high':'4', 'none': '-1'}

    #moist_range_lvl(0,20,0).
    #moist_range_lvl(21,40,1).
    #moist_range_lvl(41,60,2).
    #moist_range_lvl(61,80,3).
    #moist_range_lvl(81,100,4).

    print(avg_moist)
    print(avg_acidity)

    avg_moist_lvl = -1

    if 0 <= avg_moist and avg_moist <= 20 :
        avg_moist_lvl = 0
    elif 21 <= avg_moist and avg_moist <= 40 :
        avg_moist_lvl = 1
    elif 41 <= avg_moist and avg_moist <= 60 :
        avg_moist_lvl = 2
    elif 61 <= avg_moist and avg_moist <= 80 :
        avg_moist_lvl = 3
    elif 81 <= avg_moist and avg_moist <= 100 :
        avg_moist_lvl = 4
        
    #opposite(low, high).
    #opposite(mid, mid).
    #opposite(high, low).

    opposite_config = {'very_low':'very_high','low':'high', 'mid':'mid', 'high':'low', 'very_high':'very_low', 'none':'none'}

    #Need Rules

    #valid_moist(PL, M) :- plant(PL), plant_moist_lvl(PL, MINL, MAXL),
    #                       lvl(MINI, MINL),  lvl(MAXI, MAXL),
    #                       moist_range_lvl(MIN, MAX, I), M >= MIN, M =< MAX,
    #                       I >= MINI, I =< MAXI.

    valid_moist = [] 

    plants_valid_moist = Plant.objects.filter(moist_data__min_moist_lvl__lte=avg_moist_lvl, moist_data__max_moist_lvl__gte=avg_moist_lvl)

    #print(avg_moist_lvl)

    print(plants_valid_moist)
                                              
    for plant in plants_valid_moist :
    #    minimum = min_moist_config[plant.moist_data.min_moist_lvl]
    #    maximum = max_moist_config[plant.moist_data.max_moist_lvl]
    #    if avg_moist >= minimum and avg_moist <= maximum :
        valid_moist.append(plant)
    

    #valid_acid(PL, A) :- plant(PL), plant_ph(PL, MIN, MAX), A >= MIN, A =< MAX.

    valid_ph = []

    plants_valid_ph = Plant.objects.filter(ph_data__min_ph__lte=avg_acidity, ph_data__max_ph__gte=avg_acidity)

    print(plants_valid_ph)
    
    for plant in plants_valid_ph :
    #    minimum = float(plant.ph_data.min_ph)
    #    maximum = float(plant.ph_data.max_ph)
    #    if avg_acidity >= minimum and avg_acidity <= maximum :
        valid_ph.append(plant)

    
    #recommend_plant(PL, M, A) :- plant(PL), valid_moist(PL, M), valid_acid(PL, A).

    recommended_plants = list(set(valid_moist) & set(valid_ph))

    print(recommended_plants)


    #nutrient_level(A, N, P, K) :- ph_NPK(MIN, MAX, N, P, K), A >= MIN, A =< MAX.

    #dataset = NpkPerPh.objects.all()
    npk_data = NpkPerPh.objects.filter(min_ph__lte=avg_acidity, max_ph__gt=avg_acidity)[0]
    n_lvl = npk_data.n_lvl
    p_lvl = npk_data.p_lvl
    k_lvl = npk_data.k_lvl

    #for data in dataset :
    #    minimum = float(data.min_ph)
    #    maximum = float(data.max_ph)
     #   if minimum <= avg_acidity and avg_acidity <= maximum :
    #        n_lvl = lvl_config[data.n_lvl]
     ##       p_lvl = lvl_config[data.p_lvl]
     #       k_lvl = lvl_config[data.k_lvl]
     #       npk_data = data
      #      break

    #recommend_nutrient(A, NX, PX, KX) :- nutrient_level(A, N, P, K),
    #    opposite(N, NX), opposite(P, PX), opposite(K, KX).

    recommend_n_lvl = int(lvl_config_to_index[opposite_config[lvl_config[n_lvl]]])
    recommend_p_lvl = int(lvl_config_to_index[opposite_config[lvl_config[p_lvl]]])
    recommend_k_lvl = int(lvl_config_to_index[opposite_config[lvl_config[k_lvl]]])

    #recommend(PL, NX, PX, KX, S, M, A) :- plant(PL),
    #   recommend_plant(PL, M, A),
    #   recommend_nutrient(A, NX, PX, KX),
    #   recommend_soil_type(PL, S).

    soils_set = SoilType.objects.all() #Good to do this as long as SoilType has small size, which is normally small

    print(recommend_n_lvl)
    print(recommend_p_lvl)
    print(recommend_k_lvl)
    
    recommendation_obj = Recommendation.objects.create(soil_id=soil_profile_on_use, npk_match_ph=npk_data, recco_time=get_current_time(), recco_n_lvl=recommend_n_lvl, recco_p_lvl=recommend_p_lvl, recco_k_lvl=recommend_k_lvl)

    

    #O(n), as along as soils_set has constant number of members, managed by admins staffs only
    for plant in recommended_plants :
        #plants_list.append({'id':plant.id, 'name':plant.moist_data.plant_name})

        #recommend_soil_type(PL, S) :- plant(PL), soil_type(S),
        #    plant_moist_lvl(PL, MINL, MAXL), moist_lvl(MIN, MINL), moist_lvl(MAX, MAXL),
        #    soil_good_for_moist(S, MINS, MAXS), MINS =< MIN, MAXS >= MAX.

        for soil in soils_set :
            soil_min_id = soil.good_for_min_moist_lvl
            soil_max_id = soil.good_for_max_moist_lvl
            plant_min_id = plant.moist_data.min_moist_lvl
            plant_max_id = plant.moist_data.max_moist_lvl
            if plant_min_id >= soil_min_id  and plant_max_id <= soil_max_id :
                soil_data = soil

        RecommendedPlant.objects.create(recco_id=recommendation_obj, plant_id=plant, recco_soil_type_id=soil_data.id)

    
    return JsonResponse([], safe=False)


@csrf_exempt
def load_latest_plants_recommendation(request):
    data = json.loads(request.body)

    soil_profile_on_use = SoilProfile.objects.get(pk=data['soil_profile_id'])

    #Get latest recommendation for the soil profile
    recommendations = Recommendation.objects.filter(soil_id=soil_profile_on_use)
    if len(recommendations) <= 0:
        return JsonResponse([], safe=False)
    recommendation = recommendations[len(recommendations)-1]

    recommended_plants = RecommendedPlant.objects.filter(recco_id=recommendation)

    plants_list = []

    for recommended_plant in recommended_plants :
        soil_type = SoilType.objects.get(pk=recommended_plant.recco_soil_type_id)
        plants_list.append({'id':recommended_plant.plant_id.id, 'name':recommended_plant.plant_id.moist_data.plant_name, 'soil_type':soil_type.name})

    return JsonResponse(plants_list, safe=False)

@csrf_exempt
def load_latest_npk_recommendation(request):
    data = json.loads(request.body)

    soil_profile_on_use = SoilProfile.objects.get(pk=data['soil_profile_id'])

    lvl_config = ['very_low','low','mid','high','very_high']

    #Get latest recommendation for the soil profile
    recommendations = Recommendation.objects.filter(soil_id=soil_profile_on_use)
    if len(recommendations) <= 0:
        return JsonResponse({'n_lvl':'none', 'p_lvl':'none', 'k_lvl':'none'}, safe=False)
    recommendation = recommendations[len(recommendations)-1]

    n_lvl = lvl_config[recommendation.recco_n_lvl]
    p_lvl = lvl_config[recommendation.recco_p_lvl]
    k_lvl = lvl_config[recommendation.recco_k_lvl]
        

    return JsonResponse({'n_lvl':n_lvl, 'p_lvl':p_lvl, 'k_lvl':k_lvl}, safe=False)


@csrf_exempt
def get_plant_info(request):
    data = json.loads(request.body)

    plant = Plant.objects.get(pk=data['plant_id'])

    lvl_config = ['very_low','low','mid','high','very_high']

    name = plant.moist_data.plant_name
    min_moist = lvl_config[plant.moist_data.min_moist_lvl]
    max_moist = lvl_config[plant.moist_data.max_moist_lvl]
    min_ph = plant.ph_data.min_ph
    max_ph = plant.ph_data.max_ph

    return JsonResponse({'name':name, 'min_moist':min_moist, 'max_moist':max_moist, 'min_ph':str(min_ph), 'max_ph':str(max_ph)}, safe=False)


@csrf_exempt
def snap_reset(request):
    global moist, acidity#, fertility
    global moist_chart_data, acidity_chart_data#, fertility_chart_data
    global avg_moist, avg_acidity#, avg_fertility
    
    moist = 0
    acidity = 7
    #fertility = 0

    moist_chart_data = {
        'columns': ['time', '%'],
        'rows': []
    }

    acidity_chart_data = {
        'columns': ['time', 'pH'],
        'rows': []
    }

    #fertility_chart_data = {
    #    'columns': ['time', '%'],
    #    'rows': []
    #}

    avg_moist = 0
    avg_acidity = 7
    #avg_fertility = 0

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

@csrf_exempt
def push_ph_to_npk_into_database(request):

    lvl_config = {'very_low':0,'low':1,'mid':2,'high':3,'very_high':4}
    
    excel_dataset = xlrd.open_workbook(os.path.dirname(os.path.abspath(__file__))+'\kb\pH-to-NPK.xlsx').sheet_by_index(0) 

    ph_to_npk_dataset = []

    for i in range(excel_dataset.nrows) :
    
        ph_to_npk_dataset.append([])
    
        for j in range(excel_dataset.ncols) :
        
            ph_to_npk_dataset[i].append(excel_dataset.cell_value(i,j))

        if i > 0 :
            print(ph_to_npk_dataset[i][0])

            new_n = lvl_config[ph_to_npk_dataset[i][2]]
            new_p = lvl_config[ph_to_npk_dataset[i][3]]
            new_k = lvl_config[ph_to_npk_dataset[i][4]]

            try:
                exist = NpkPerPh.objects.get(min_ph=ph_to_npk_dataset[i][0], max_ph=ph_to_npk_dataset[i][1])
                NpkPerPh.objects.filter(min_ph=ph_to_npk_dataset[i][0], max_ph=ph_to_npk_dataset[i][1]).update(n_lvl=new_n, p_lvl=new_p, k_lvl=new_k)
            except NpkPerPh.DoesNotExist:
                NpkPerPh.objects.create(min_ph=ph_to_npk_dataset[i][0], max_ph=ph_to_npk_dataset[i][1], n_lvl=new_n, p_lvl=new_p, k_lvl=new_k)

    return HttpResponse('')

@csrf_exempt
def push_plants_into_database(request):

    lvl_config = {'very_low':0,'low':1,'mid':2,'high':3,'very_high':4}

    moist_excel_dataset = xlrd.open_workbook(os.path.dirname(os.path.abspath(__file__))+'\kb\Moist-to-plant.xlsx').sheet_by_index(0) 
    ph_excel_dataset = xlrd.open_workbook(os.path.dirname(os.path.abspath(__file__))+'\kb\pH-to-plant.xlsx').sheet_by_index(0) 

    #Push Plant name first
    #No duplicate names
    #Push ph according to matched Plant name
    #Push moist_lvl according to matched Plant name
    #done

    inserted_moist_plant = []
    inserted_ph_plant = []
    

    moist_to_plant_dataset = []
    
    for i in range(moist_excel_dataset.nrows) :
    
        moist_to_plant_dataset.append([])
    
        for j in range(moist_excel_dataset.ncols) :
        
            moist_to_plant_dataset[i].append(moist_excel_dataset.cell_value(i,j))

        if i > 0 :
            print(moist_to_plant_dataset[i][0])

            new_min = lvl_config[moist_to_plant_dataset[i][1]]
            new_max = lvl_config[moist_to_plant_dataset[i][2]]

            try:
                data = PlantMoistLvl.objects.get(plant_name=moist_to_plant_dataset[i][0])
                PlantMoistLvl.objects.filter(plant_name=moist_to_plant_dataset[i][0]).update(min_moist_lvl=new_min, max_moist_lvl=new_max)
            except PlantMoistLvl.DoesNotExist:
                data = PlantMoistLvl.objects.create(plant_name=moist_to_plant_dataset[i][0], min_moist_lvl=new_min, max_moist_lvl=new_max)

            inserted_moist_plant.append(data.plant_name)

    ph_to_plant_dataset = []
    for i in range(ph_excel_dataset.nrows) :
    
        ph_to_plant_dataset.append([])
    
        for j in range(ph_excel_dataset.ncols) :
        
            ph_to_plant_dataset[i].append(ph_excel_dataset.cell_value(i,j))

        if i > 0 :
            print(ph_to_plant_dataset[i][0])
             
            try:
                data = PlantPh.objects.get(plant_name=ph_to_plant_dataset[i][0])
                PlantPh.objects.filter(plant_name=ph_to_plant_dataset[i][0]).update(min_ph=ph_to_plant_dataset[i][1], max_ph=ph_to_plant_dataset[i][2])
            except PlantPh.DoesNotExist:
                data = PlantPh.objects.create(plant_name=ph_to_plant_dataset[i][0], min_ph=ph_to_plant_dataset[i][1], max_ph=ph_to_plant_dataset[i][2])

            inserted_ph_plant.append(data.plant_name)

    for moist_data_name in inserted_moist_plant :
        for ph_data_name in inserted_ph_plant :
            if moist_data_name == ph_data_name :
                try:
                    moist_data = PlantMoistLvl.objects.get(plant_name=moist_data_name)
                    ph_data = PlantPh.objects.get(plant_name=ph_data_name)
                    plant = Plant.objects.get(moist_data=moist_data, ph_data=ph_data)
                except Plant.DoesNotExist:
                    plant = Plant.objects.create(moist_data=moist_data, ph_data=ph_data)

    return HttpResponse('')

@csrf_exempt
def push_soil_types_into_database(request):

    lvl_config = {'very_low':0,'low':1,'mid':2,'high':3,'very_high':4}
    
    excel_dataset = xlrd.open_workbook(os.path.dirname(os.path.abspath(__file__))+'\kb\Soil_type_to_moist.xlsx').sheet_by_index(0) 

    soil_to_moist_dataset = []

    for i in range(excel_dataset.nrows) :
    
        soil_to_moist_dataset.append([])
    
        for j in range(excel_dataset.ncols) :
        
            soil_to_moist_dataset[i].append(excel_dataset.cell_value(i,j))

        if i > 0 :
            print(soil_to_moist_dataset[i][0])

            new_good_min = lvl_config[soil_to_moist_dataset[i][1]]
            new_good_max = lvl_config[soil_to_moist_dataset[i][2]]

            try:
                exist = SoilType.objects.get(name=soil_to_moist_dataset[i][0])
                SoilType.objects.filter(name=soil_to_moist_dataset[i][0]).update(good_for_min_moist_lvl=new_good_min, good_for_max_moist_lvl=new_good_max)
            except SoilType.DoesNotExist:
                SoilType.objects.create(name=soil_to_moist_dataset[i][0], good_for_min_moist_lvl=new_good_min, good_for_max_moist_lvl=new_good_max)

    return HttpResponse('')


def public(request):
    return HttpResponse("You don't need to be authenticated to see this")


@api_view(['GET'])
def private(request):
    return HttpResponse("You should not see this message if not authenticated!")
