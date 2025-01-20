from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from base.models import Appointment, Billing, Service
from patient.models import Patient
from physician.models import Doctor


def index_view(request):
    services = Service.objects.all()
    context = {"services": services}
    return render(request, "base/index.html", context)


def service_detail_view(request, service_id):
    service = Service.objects.get(id=service_id)
    context = {"service": service}
    return render(request, "base/service_detail.html", context)


@login_required
def book_appointment(request, service_id, doctor_id):
    service = Service.objects.get(id=service_id)
    doctor = Doctor.objects.get(id=doctor_id)
    patient = Patient.objects.get(user=request.user)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        issues = request.POST.get("issues")
        symptoms = request.POST.get("symptoms")

        patient.full_name = full_name
        patient.email = email
        patient.mobile = mobile
        patient.address = address
        patient.gender = gender
        patient.dob = dob
        patient.save()

        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            service=service,
            appointment_date=doctor.next_appointment_date,
            issues=issues,
            symptoms=symptoms,
        )
        billing = Billing()
        billing.patient = patient
        billing.appointment = appointment
        billing.sub_total = appointment.service.cost
        billing.tax = appointment.service.cost * 13 / 100
        billing.total = billing.sub_total + billing.tax
        billing.status = "Не оплачено"
        billing.save()

        return redirect("base:checkout", billing.billing_id)
    context = {"service": service, "doctor": doctor, "patient": patient}
    return render(request, "base/book_appointment.html", context)


def checkout_view(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    context = {"billing": billing}
    return render(request, "base/checkout.html", context)
