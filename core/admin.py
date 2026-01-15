# core/admin.py
from django.contrib import admin
from .models import (
    District, Taluka, Subject, School, Student, Assignment, 
    TaskEvaluation, DDPIProfile, BEOProfile, PrincipalProfile
)

admin.site.register(District)
admin.site.register(Taluka)
admin.site.register(Subject)
admin.site.register(School)
admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(TaskEvaluation)
admin.site.register(DDPIProfile)
admin.site.register(BEOProfile)
admin.site.register(PrincipalProfile)