from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(User)

admin.site.register(Plant)

admin.site.register(PlantMoistLvl)
admin.site.register(PlantPh)
admin.site.register(NpkPerPh)
admin.site.register(SoilType)

admin.site.register(SoilProfile)
admin.site.register(SensorRecord)
admin.site.register(Recommendation)
admin.site.register(RecommendedPlant)
