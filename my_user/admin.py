from django.contrib import admin
from .models import School, Course, Profile, Batch


# Register your models here.
admin.site.register(Profile)
admin.site.register(School)
admin.site.register(Course)
admin.site.register(Batch)