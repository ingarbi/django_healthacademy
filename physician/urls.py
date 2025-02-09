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
    path(
        "add-lab-test/<appointment_id>/",
        views.add_lab_test,
        name="add_lab_test",
    ),
    path(
        "edit-lab-test/<appointment_id>/<lab_test_id>/",
        views.edit_lab_test,
        name="edit_lab_test",
    ),
    path(
        "add-prescription/<appointment_id>/",
        views.add_prescription,
        name="add_prescription",
    ),
    path(
        "edit-prescription/<appointment_id>/<prescription_id>/",
        views.edit_prescription,
        name="edit_prescription",
    ),
    path("payments/", views.payments, name="payments"),
    path("notifications/", views.notifications, name="notifications"),
    path("mark-as-read-notifications/<id>/", views.mark_as_read_notifications, name="mark_as_read_notifications"),
    path("profile/", views.profile, name="profile"),
]
