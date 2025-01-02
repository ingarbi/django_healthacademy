from django.contrib import admin

from .models import Doctor, Notification


class DoctorAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "full_name",
        "specialization",
        "qualification",
        "year_of_exp",
    ]


class NotificationAdmin(admin.ModelAdmin):
    list_display = ["doctor", "appointment", "category", "seen", "date"]


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Notification, NotificationAdmin)
