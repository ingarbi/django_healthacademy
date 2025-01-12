from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from patient.models import Patient
from physician.models import Doctor

from .forms import UserLoginForm, UserRegisterForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        messages.success(request, "Вы уже вошли в аккаунт")
        return redirect("/")
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data.get("full_name")
            email = form.cleaned_data.get("email")
            password1 = form.cleaned_data.get("password1")
            user_type = form.cleaned_data.get("user_type")
            user = authenticate(email=email, password=password1)
            if user is not None:
                login(request, user)

                if user_type == "Doctor":
                    Doctor.objects.create(user=user, full_name=full_name)
                else:
                    Patient.objects.create(user=user, full_name=full_name, email=email)
                messages.success(request, "Аккаунт успешно создан")
                return redirect("/")
    else:
        form = UserRegisterForm()
    context = {"form": form}
    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, "Вы уже вошли в аккаунт")
        return redirect("/")
    if request.method == "POST":
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            try:
                user_instance = User.objects.get(email=email, is_active=True)
                user_authenticate = authenticate(
                    request, email=email, password=password
                )

                if user_instance is not None:
                    login(request, user_authenticate)
                    messages.success(request, "Вы успешно залогинились")
                    next_url = request.GET.get("next", "/")
                    return redirect(next_url)
                else:
                    messages.error(request, "Ошибка в логине или в пароле")
            except:
                messages.error(request, "Пользователя с такими данными не существует")
    else:
        form = UserLoginForm()
    context = {"form": form}
    return render(request, "userauths/sign-in.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "Вы вышли из аккаунта")
    return redirect("/")
