from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Иван Иванов"}
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "ivan@ivanoff"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "******"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "******"}
        )
    )

    class Meta:
        model = User
        fields = ["full_name", "email", "password1", "password2", "user_type"]


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "ivan@ivanoff"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "******"}
        )
    )

    class Meta:
        model = User
        fields = ["email", "password"]
