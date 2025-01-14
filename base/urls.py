from django.urls import path

from base import views

app_name = "base"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("service/<service_id>", views.service_detail_view, name="service_detail"),

]
