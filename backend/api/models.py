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

class PlantMoistLvl(models.Model):
    VERY_LOW = 'very_low'
    LOW = 'low'
    MID = 'mid'
    HIGH = 'high'
    VERY_HIGH = 'very_high'
    LEVEL_CHOICES = (
        (VERY_LOW, 'Very Low'),
        (LOW, 'Low'),
        (MID, 'Medium'),
        (HIGH, 'High'),
        (VERY_HIGH, 'Very High'),
    )
    plant_name = models.CharField(max_length=100, default='')
    min_moist_lvl = models.CharField(
        max_length=10,
        choices= LEVEL_CHOICES,
        default= VERY_LOW
    )
    max_moist_lvl = models.CharField(
        max_length=10,
        choices= LEVEL_CHOICES,
        default= VERY_HIGH
    )
    def __str__(self):
        return self.plant_name

class PlantPh(models.Model):
    plant_name = models.CharField(max_length=100, default='')
    min_ph = models.DecimalField(max_digits=10, decimal_places=2, default=0,validators=[MaxValueValidator(14), MinValueValidator(0)])
    max_ph = models.DecimalField(max_digits=10, decimal_places=2, default=14,validators=[MaxValueValidator(14), MinValueValidator(0)])
    def __str__(self):
        return self.plant_name

class Plant(models.Model):
    moist_data = models.ForeignKey(PlantMoistLvl, on_delete=models.CASCADE, default=0)
    ph_data = models.ForeignKey(PlantPh, on_delete=models.CASCADE, default=0)
    def __str__(self):
        data = PlantMoistLvl.objects.get(pk=self.moist_data.pk)
        return data.plant_name



class NpkPerPh(models.Model):
    LOW = 'low'
    MID = 'mid'
    HIGH = 'high'
    LEVEL_CHOICES = (
        (LOW, 'Low'),
        (MID, 'Medium'),
        (HIGH, 'High'),
    )
    min_ph = models.DecimalField(max_digits=10, decimal_places=2,validators=[MaxValueValidator(14), MinValueValidator(0)], default=0)
    max_ph = models.DecimalField(max_digits=10, decimal_places=2,validators=[MaxValueValidator(14), MinValueValidator(0)], default=0)
    n_lvl = models.CharField(
        max_length=10,
        choices= LEVEL_CHOICES
    )
    p_lvl = models.CharField(
        max_length=10,
        choices= LEVEL_CHOICES
    )
    k_lvl = models.CharField(
        max_length=10,
        choices= LEVEL_CHOICES
    )
    def __str__(self):
        return str(self.ph)

class SoilType(models.Model):
    VERY_LOW = 'very_low'
    LOW = 'low'
    MID = 'mid'
    HIGH = 'high'
    VERY_HIGH = 'very_high'
    LEVEL_CHOICES = (
        (VERY_LOW, 'Very Low'),
        (LOW, 'Low'),
        (MID, 'Medium'),
        (HIGH, 'High'),
        (VERY_HIGH, 'Very High'),
    )
    name = models.CharField(max_length=100)
    good_for_min_moist_lvl = models.CharField(
        max_length=10,
        choices= LEVEL_CHOICES
    )
    good_for_max_moist_lvl = models.CharField(
        max_length=10,
        choices= LEVEL_CHOICES
    )
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
    soil_id = models.ForeignKey(SoilProfile, on_delete=models.CASCADE)
    moist = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ph = models.DecimalField(max_digits=10, decimal_places=2, default=7)
    record_date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        soil = SoilProfile.objects.get(pk=self.soil_id.pk)
        return soil.name + " - " + str(self.record_date)

class Recommendation(models.Model):
    LOW = 'low'
    MID = 'mid'
    HIGH = 'high'
    LEVEL_CHOICES = (
        (LOW, 'Low'),
        (MID, 'Medium'),
        (HIGH, 'High'),
    )
    soil_id = models.ForeignKey(SoilProfile, on_delete=models.CASCADE)
    recco_soil_type = models.ForeignKey(SoilType, on_delete=models.CASCADE)
    npk_match_ph = models.ForeignKey(NpkPerPh, on_delete=models.CASCADE)
    recco_n_lvl = models.CharField(
        max_length=10,
        choices= LEVEL_CHOICES
    )
    recco_p_lvl = models.CharField(
        max_length=10,
        choices= LEVEL_CHOICES
    )
    recco_k_lvl = models.CharField(
        max_length=10,
        choices= LEVEL_CHOICES
    )
    def __str__(self):
        soil = SoilProfile.objects.get(pk=self.soil_id.pk)
        return soil.name

class RecommendedPlant(models.Model):
    recco_id = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE)
    def __str__(self):
        plant = Plant.objects.get(pk=self.plant_id.pk)
        recco = Recommendation.objects.get(pk=self.recco_id.pk)
        soil = SoilProfile.objects.get(pk=self.recco.soil_id.pk)
        return plant.name + ", " + soil.name
