from django.shortcuts import render


def index_view(request):
    return render(request, "base/index.html")

def service_detail_view(request):
    return render(request, "base/service_detail.html")
