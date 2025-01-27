from django.urls import path

from physician import views

app_name = "physician"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("appointments/", views.appointments, name="appointments"),
    path(
        "appointments/<appointment_id>",
        views.appointment_detail,
        name="appointment_detail",
    ),
]
