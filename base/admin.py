from django.contrib import admin

from .models import (Appointment, Billing, LabTest, MedicalRecord,
                     Prescription, Service)


class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 1


class MedicalRecordInline(admin.TabularInline):
    model = MedicalRecord
    extra = 1


class LabTestInline(admin.TabularInline):
    model = LabTest
    extra = 1


class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 1


class BillingInline(admin.TabularInline):
    model = Billing
    extra = 1


class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "cost"]
    search_fields = ["name", "description"]
    filter_horizontal = ["available"]


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["patient", "doctor", "appointment_date", "status"]
    search_fields = ["patient__username", "doctor__user__username"]
    inlines = [MedicalRecordInline, LabTestInline, PrescriptionInline, BillingInline]


class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ["appointment", "diagnosis"]


class LabTestAdmin(admin.ModelAdmin):
    list_display = ["appointment", "test_name"]


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ["appointment", "medication"]


class BillingAdmin(admin.ModelAdmin):
    list_display = ["patient", "total", "status", "date"]


admin.site.register(Service, ServiceAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(LabTest, LabTestAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(Billing, BillingAdmin)
