from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

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


@login_required
def cancel_appointment(request, appointment_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, doctor=doctor
    )
    appointment.status = "Отменено"
    appointment.save()
    messages.success(request, "Прием успешно отменен")

    return redirect("physician:appointment_detail", appointment.appointment_id)


@login_required
def complete_appointment(request, appointment_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, doctor=doctor
    )
    appointment.status = "Выполнено"
    appointment.save()
    messages.success(request, "Прием успешно выполнен")

    return redirect("physician:appointment_detail", appointment.appointment_id)


@login_required
def activate_appointment(request, appointment_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, doctor=doctor
    )
    appointment.status = "Запланировано"
    appointment.save()
    messages.success(request, "Прием успешно активирован")

    return redirect("physician:appointment_detail", appointment.appointment_id)


@login_required
def add_medical_record(request, appointment_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, doctor=doctor
    )
    if request.method == "POST":
        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")
        base_models.MedicalRecord.objects.create(
            appointment=appointment, diagnosis=diagnosis, treatment=treatment
        )
        messages.success(request, "Медицинская запись успешно добавлена")
        return redirect("physician:appointment_detail", appointment.appointment_id)


@login_required
def edit_medical_record(request, appointment_id, medical_record_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, doctor=doctor
    )
    medical_record = base_models.MedicalRecord.objects.get(
        id=medical_record_id, appointment=appointment
    )
    if request.method == "POST":
        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")
        medical_record.diagnosis = diagnosis
        medical_record.treatment = treatment
        medical_record.save()
        messages.success(request, "Медицинская запись успешно обновлена")
        return redirect("physician:appointment_detail", appointment.appointment_id)


@login_required
def add_lab_test(request, appointment_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, doctor=doctor
    )
    if request.method == "POST":
        test_name = request.POST.get("test_name")
        description = request.POST.get("description")
        result = request.POST.get("result")
        base_models.LabTest.objects.create(
            appointment=appointment,
            test_name=test_name,
            description=description,
            test_result=result,
        )
        messages.success(request, "Лабораторный анализ успешно добавлена")
        return redirect("physician:appointment_detail", appointment.appointment_id)


@login_required
def edit_lab_test(request, appointment_id, lab_test_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, doctor=doctor
    )
    lab_test = base_models.LabTest.objects.get(id=lab_test_id, appointment=appointment)
    
    if request.method == "POST":
        test_name = request.POST.get("test_name")
        description = request.POST.get("description")
        result = request.POST.get("result")
        lab_test.test_name = test_name
        lab_test.description = description
        lab_test.test_result = result
        lab_test.save()
        messages.success(request, "Лабораторный анализ успешно обновлен")
        return redirect("physician:appointment_detail", appointment.appointment_id)
    
@login_required
def add_prescription(request, appointment_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, doctor=doctor
    )
    if request.method == "POST":
        medications = request.POST.get("medications")
        base_models.Prescription.objects.create(
            appointment=appointment, medication=medications
        )
    messages.success(request, "Предписание врача успешно добавлено")
    return redirect("physician:appointment_detail", appointment.appointment_id)
    

@login_required
def edit_prescription(request, appointment_id, prescription_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, doctor=doctor
    )
    prescription = base_models.Prescription.objects.get(
        id=prescription_id, appointment=appointment
    )
    if request.method == "POST":
        medications = request.POST.get("medications")
        prescription.medication = medications
        prescription.save()
    messages.success(request, "Предписание врача успешно обновлено")
    return redirect("physician:appointment_detail", appointment.appointment_id)

@login_required
def payments(request):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    payments = base_models.Billing.objects.filter(appointment__doctor=doctor, status="Оплачено")
    context = {"payments": payments}
    return render(request, "physician/payments.html", context)