"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .api.views import *

router = routers.DefaultRouter()
router.register('messages', MessageViewSet)

urlpatterns = [

    # http://localhost:8000/
    path('', home),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),

    path('register', register),

    path('user', user),
    path('user_info', user_info),

    path('change_email', change_email),
    path('change_password', change_password),

    path('get_soil_profiles', get_soil_profiles),
    path('get_soil_profile', get_soil_profile),

    path('add_soil_profile', add_soil_profile),
    path('edit_soil_profile', edit_soil_profile),
    path('clear_soil_profile', clear_soil_profile),
    path('delete_soil_profile', delete_soil_profile),

    path('get_total_records_per_soil', get_total_records_per_soil),

    path('get_all_values_as_scatter', get_all_values_as_scatter),

    path('debug_frequency', debug_frequency),

    path('get_good_moist_ph_values', get_good_moist_ph_values),
    path('get_recommendations', get_recommendations),
    path('load_latest_plants_recommendation', load_latest_plants_recommendation),
    path('load_latest_npk_recommendation', load_latest_npk_recommendation),

    path('get_plant_info', get_plant_info),
    path('load_plant_search_results', load_plant_search_results),

    path('push_ph_to_npk_into_database', push_ph_to_npk_into_database),
    path('push_plants_into_database', push_plants_into_database),
    path('push_soil_types_into_database', push_soil_types_into_database),

    path(r'auth/obtain_token/', obtain_jwt_token),
    path(r'auth/refresh_token/', refresh_jwt_token),

    path('public', public),
    path('private', private),

    #url(r'^auth/obtain_token/', obtain_jwt_token),
    
    #url(r'^auth/refresh_token/', refresh_jwt_token),
]


