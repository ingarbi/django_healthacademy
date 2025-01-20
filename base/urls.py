from django.urls import path

from base import views

app_name = "base"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("service/<service_id>", views.service_detail_view, name="service_detail"),
    path(
        "book-appointment/<service_id>/<doctor_id>",
        views.book_appointment,
        name="book_appointment",
    ),
    path("checkout/<billing_id>", views.checkout_view, name="checkout"),
]
