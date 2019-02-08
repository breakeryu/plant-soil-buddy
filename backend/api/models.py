from django.db import models
from rest_framework import serializers
from django.contrib import auth
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime 

class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('url', 'subject', 'body', 'pk')

class User(auth.models.User):
    user_ptr = None

class Plant(models.Model):
    name = models.CharField(max_length=100)
    min_moist = models.DecimalField(max_digits=10, decimal_places=2, default=0,validators=[MaxValueValidator(100), MinValueValidator(0)])
    max_moist = models.DecimalField(max_digits=10, decimal_places=2, default=100,validators=[MaxValueValidator(100), MinValueValidator(0)])
    min_ph = models.DecimalField(max_digits=10, decimal_places=2, default=0,validators=[MaxValueValidator(14), MinValueValidator(0)])
    max_ph = models.DecimalField(max_digits=10, decimal_places=2, default=14,validators=[MaxValueValidator(14), MinValueValidator(0)])
    min_fertility = models.DecimalField(max_digits=10, decimal_places=2, default=0,validators=[MaxValueValidator(100), MinValueValidator(0)])
    max_fertility = models.DecimalField(max_digits=10, decimal_places=2, default=100,validators=[MaxValueValidator(100), MinValueValidator(0)])
    def __str__(self):
        return self.name

class SoilProfile(models.Model):
    owner = models.ForeignKey(auth.models.User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location =models.CharField(max_length=256)
    def __str__(self):
        user = auth.models.User.objects.get(pk=self.owner.pk)
        return user.username + " - " + self.name
    
class SensorRecord(models.Model):
    soil_profile = models.ForeignKey(SoilProfile, on_delete=models.CASCADE)
    record_time = models.DateTimeField(default=datetime.now, blank=True)
    moist = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ph = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fertility = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        soil = SoilProfile.objects.get(pk=self.soil_profile.pk)
        return soil.name + " - " + str(self.record_time)

