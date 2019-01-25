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

    path('ask-current-temp', get_temp),
    path('get-temp-stats', get_temp_stats),

    path('get_moist_as_value', get_moist_as_value),
    path('get_moist_as_stats', get_moist_as_stats),

    path('get_acidity_as_value', get_acidity_as_value),
    path('get_acidity_as_stats', get_acidity_as_stats),

    path('get_fertility_as_value', get_fertility_as_value),
    path('get_fertility_as_stats', get_fertility_as_stats),

    path('get_recommended_plants', get_recommended_plants),

    path(r'auth/obtain_token/', obtain_jwt_token),
    path(r'auth/refresh_token/', refresh_jwt_token),

    path('public', public),
    path('private', private),

    #url(r'^auth/obtain_token/', obtain_jwt_token),
    
    #url(r'^auth/refresh_token/', refresh_jwt_token),
]


