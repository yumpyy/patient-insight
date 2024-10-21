from django.contrib import admin

from .models import Patient, Medications, MedicalHistory, TreatmentPlans

admin.site.register(Patient)
admin.site.register(Medications)
admin.site.register(MedicalHistory)
admin.site.register(TreatmentPlans)
