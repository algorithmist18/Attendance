from django.contrib import admin
from .models import Subject, Profile, Schedule_Blob, Semester

# Register your models here.

admin.site.register(Subject)
admin.site.register(Profile)
admin.site.register(Schedule_Blob)
admin.site.register(Semester)