from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import redirect, render

from base import models as base_models
from patient import models as patient_models


@login_required
def dashboard(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)
    notifications = patient_models.Notification.objects.filter(patient=patient)
    total_spent = base_models.Billing.objects.filter(patient=patient).aggregate(
        total_spent=models.Sum("total")
    )["total_spent"]

    context = {
        "appointments": appointments,
        "notifications": notifications,
        "total_spent": total_spent,
    }
    return render(request, "patient/dashboard.html", context)


@login_required
def appointments(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)

    context = {"appointments": appointments}
    return render(request, "patient/appointments.html", context)


@login_required
def appointment_detail(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, patient=patient
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

    return render(request, "patient/appointment_detail.html", context)


@login_required
def cancel_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, patient=patient
    )
    appointment.status = "Отменено"
    appointment.save()
    messages.success(request, "Прием успешно отменен")

    return redirect("patient:appointment_detail", appointment.appointment_id)


@login_required
def complete_appointment(request, appointment_id):
    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, patient=patient
    )
    appointment.status = "Выполнено"
    appointment.save()
    messages.success(request, "Прием успешно выполнен")

    return redirect("patient:appointment_detail", appointment.appointment_id)


@login_required
def activate_appointment(request, appointment_id):

    patient = patient_models.Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, patient=patient
    )
    appointment.status = "Запланировано"
    appointment.save()
    messages.success(request, "Прием успешно активирован")

    return redirect("patient:appointment_detail", appointment.appointment_id)


@login_required
def payments(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    payments = base_models.Billing.objects.filter(
        appointment__patient=patient, status="Оплачено"
    )
    context = {"payments": payments}
    return render(request, "patient/payments.html", context)


@login_required
def notifications(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    notifications = patient_models.Notification.objects.filter(
        patient=patient, seen=False
    )

    context = {"notifications": notifications}
    return render(request, "patient/notifications.html", context)


@login_required
def mark_as_read_notifications(request, id):
    patient = patient_models.Patient.objects.get(user=request.user)
    notification = patient_models.Notification.objects.get(id=id, patient=patient)
    notification.seen = True
    notification.save()
    messages.success(request, "Уведомление успешно отмечено как прочитанное")
    return redirect("patient:notifications")


@login_required
def profile(request):
    patient = patient_models.Patient.objects.get(user=request.user)
    formatted_dob = patient.dob.strftime("%Y-%m-%d")

    if request.method == "POST":
        image = request.FILES.get("image")
        full_name = request.POST.get("full_name")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")

        gender = request.POST.get("gender")

        blood_group = request.POST.get("blood_group")
        dob = request.POST.get("dob")

        patient.full_name = full_name
        patient.mobile = mobile
        patient.address = address
        patient.gender = gender
        patient.blood_group = blood_group
        patient.dob = dob

        if image is not None:
            patient.image = image

        patient.save()
        messages.success(request, "Профиль успешно обновлен")
        return redirect("patient:profile")

    context = {
        "patient": patient,
        "formatted_dob": formatted_dob,
    }
    return render(request, "patient/profile.html", context)
