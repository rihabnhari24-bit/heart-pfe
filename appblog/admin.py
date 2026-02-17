from django.contrib import admin

from .models import PatientPrediction


@admin.register(PatientPrediction)
class PatientPredictionAdmin(admin.ModelAdmin):
    list_display = (
        "patient_identifier",
        "patient_name",
        "age",
        "sex",
        "prediction",
        "created_at",
    )
    search_fields = ("patient_identifier", "patient_name")
    list_filter = ("prediction", "created_at")
