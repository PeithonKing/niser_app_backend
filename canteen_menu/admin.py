from django.contrib import admin
from .models import Canteen, FoodItem, Due


# Register your models here.
admin.site.register(Canteen)
admin.site.register(FoodItem)
admin.site.register(Due)
