from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render


def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("welcome")

        error = "Identifiants invalides."

    return render(request, "login.html", {"error": error})


def register_view(request):
    error = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        try:
            validate_email(email)
        except ValidationError:
            error = "Les informations sont mal écrites."
        else:
            if not name or not password:
                error = "Les informations sont mal écrites."
            elif User.objects.filter(username=email).exists():
                error = "Les informations sont mal écrites."
            else:
                User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=name,
                )
                return redirect("login")

    return render(request, "register.html", {"error": error})


@login_required
def welcome(request):
    return render(request, "welcome.html")


def logout_view(request):
    logout(request)
    return redirect("login")
