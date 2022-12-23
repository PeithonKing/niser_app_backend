from django.contrib import admin

# Register your models here.

from .models import Location, Condition, Listing, ListingType

admin.site.register(Location)
admin.site.register(Condition)
admin.site.register(ListingType)
admin.site.register(Listing)