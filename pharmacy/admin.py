from django.contrib import admin

# Register your models here.
from pharmacy.models import Medicine, Prescription


class MedicineInline(admin.TabularInline):
    model = Medicine


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    inlines = [
        MedicineInline
    ]


admin.site.register(Medicine)
