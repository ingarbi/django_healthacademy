from django.db import models
from shortuuid.django_fields import ShortUUIDField

from patient.models import Patient
from physician.models import Doctor


class Service(models.Model):
    image = models.FileField(upload_to="images", null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.ManyToManyField(Doctor, blank=True)

    def __str__(self):
        return f"{self.name} - {self.cost}"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ("Запланировано", "Запланировано"),
        ("Выполнено", "Выполнено"),
        ("Рассматривается", "Рассматривается"),
        ("Отменено", "Отменено"),
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_appointment",
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctor_appointment",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patient_appointment",
    )
    appointment_date = models.DateTimeField(null=True, blank=True)
    issues = models.TextField(null=True, blank=True)
    symptoms = models.TextField(null=True, blank=True)
    appointment_id = ShortUUIDField(
        length=6,
        max_length=10,
        unique=True,
        alphabet="0123456789",
    )
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="Рассматривается"
    )

    def __str__(self):
        return f"{self.patient.full_name} - {self.doctor.full_name}"


class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField(null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Медицинская запись для {self.appointment.patient.full_name}"


class LabTest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    test_name = models.CharField(max_length=200, null=True, blank=True)
    test_result = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.test_name


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medication = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Предписание для {self.appointment.patient.full_name}"


class Billing(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patient_billing",
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="appointment_billing",
    )
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=100,
        choices=(("Оплачено", "Оплачено"), ("Не оплачено", "Не оплачено")),
        default="Не оплачено",
    )
    billing_id = ShortUUIDField(
        length=6, max_length=10, unique=True, alphabet="0123456789"
    )
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Счет No {self.id} для {self.appointment.patient.full_name}, сумма: {self.total}"
