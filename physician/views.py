from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from base import models as base_models
from physician import models as physician_models


@login_required
def dashboard(request):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)
    notifications = physician_models.Notification.objects.filter(doctor=doctor)

    context = {"appointments": appointments, "notifications": notifications}
    return render(request, "physician/dashboard.html", context)


@login_required
def appointments(request):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)

    context = {"appointments": appointments}
    return render(request, "physician/appointments.html", context)


@login_required
def appointment_detail(request, appointment_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, doctor=doctor
    )
    medical_record = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)

    context = {
        "appointment": appointment,
        "medical_record": medical_record,
        "lab_tests": lab_tests,
        "prescriptions": prescriptions,
    }

    return render(request, "physician/appointment_detail.html", context)
