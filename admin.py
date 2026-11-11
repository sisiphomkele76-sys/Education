from django.contrib import admin
from .models import UserProfile, MedicationReminder, PrescribedMedication, TreatmentResource, Blog

admin.site.register(UserProfile)
admin.site.register(MedicationReminder)
admin.site.register(PrescribedMedication)
admin.site.register(TreatmentResource)
admin.site.register(Blog)