from django.shortcuts import render

from base.models import Service


def index_view(request):
    services = Service.objects.all()
    context = {"services": services}
    return render(request, "base/index.html", context)


def service_detail_view(request, service_id):
    service = Service.objects.get(id=service_id)
    context = {"service": service}
    return render(request, "base/service_detail.html", context)
