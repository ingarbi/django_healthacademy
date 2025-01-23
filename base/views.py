import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from base.models import Appointment, Billing, Service
from patient.models import Notification as PatientNotification
from patient.models import Patient
from physician.models import Doctor, Notification


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


@login_required
def checkout_view(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    context = {"billing": billing, "stripe_public_key": stripe_public_key}
    return render(request, "base/checkout.html", context)


@login_required
def stripe_payment(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email=billing.patient.email,
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Оплата" + billing.patient.full_name,
                    },
                    "unit_amount": int(billing.total * 1000),
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("base:stripe_payment_verify", args=[billing.billing_id])
        )
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(
            reverse("base:stripe_payment_verify", args=[billing.billing_id])
        ),
    )
    return JsonResponse({"sessionId": checkout_session.id})


@login_required
def stripe_payment_verify(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == "paid":
        if billing.status == "Не оплачено":
            billing.status = "Оплачено"
            billing.save()

            Notification.objects.create(
                doctor=billing.appointment.doctor,
                appointment=billing.appointment,
                category="Новая запись",
            )

            PatientNotification.objects.create(
                patient=billing.appointment.patient,
                appointment=billing.appointment,
                category="Запись создана",
            )

            return redirect(
                f"/payment_status/{billing.billing_id}/?payment_status=paid"
            )
    else:
        return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")


@login_required
def payment_status_view(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    payment_status = request.GET.get("payment_status")
    context = {"billing": billing, "payment_status": payment_status}
    return render(request, "base/payment_status.html", context)
