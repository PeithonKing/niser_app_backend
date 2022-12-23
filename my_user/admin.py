from django.contrib import admin
from .models import School, Course, Profile


# Register your models here.
admin.site.register(Profile)
admin.site.register(School)
admin.site.register(Course)