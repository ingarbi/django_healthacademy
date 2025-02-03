from django.urls import path

from physician import views

app_name = "physician"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("appointments/", views.appointments, name="appointments"),
    path(
        "appointments/<appointment_id>/",
        views.appointment_detail,
        name="appointment_detail",
    ),
    path(
        "cancel-appointment/<appointment_id>/",
        views.cancel_appointment,
        name="cancel_appointment",
    ),
    path(
        "activate-appointment/<appointment_id>/",
        views.activate_appointment,
        name="activate_appointment",
    ),
    path(
        "complete-appointment/<appointment_id>/",
        views.complete_appointment,
        name="complete_appointment",
    ),
    path(
        "add-medical-record/<appointment_id>/",
        views.add_medical_record,
        name="add_medical_record",
    ),
    path(
        "edit_medical_record/<appointment_id>/<medical_record_id>/",
        views.edit_medical_record,
        name="edit_medical_record",
    ),
]
