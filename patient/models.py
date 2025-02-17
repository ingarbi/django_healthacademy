from django.db import models
from django.utils import timezone

from userauths.models import User

NOTIFICATION_CHOICES = (
    ("Запись создана", "Запись создана"),
    ("Запись отменена", "Запись отменена"),
)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="images", null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    blood_group = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.full_name


class Notification(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.SET_NULL, null=True, blank=True
    )
    appointment = models.ForeignKey(
        "base.Appointment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="patient_appointment_notification",
    )
    category = models.CharField(
        max_length=100,
        choices=NOTIFICATION_CHOICES,
    )
    seen = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Доктор {self.patient.full_name} - Уведомление"
