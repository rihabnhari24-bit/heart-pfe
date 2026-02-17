import joblib
from pathlib import Path

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from heartsite.settings import BASE_DIR

from .models import PatientPrediction

FEATURE_FIELDS = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
]

MODEL_PATH = Path(BASE_DIR) / "module.pkl"


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


@login_required
def account_view(request):
    error = None
    success = None

    if request.method == "POST":
        if request.POST.get("action") == "logout":
            return redirect("logout")

        password = request.POST.get("password", "")
        password_repeat = request.POST.get("password_repeat", "")

        if not password or password != password_repeat:
            error = "Les deux mots de passe ne correspondent pas."
        else:
            request.user.set_password(password)
            request.user.save()
            logout(request)
            return redirect("login")

    return render(request, "account.html", {"error": error, "success": success})


def _predict_with_model(feature_values):
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
        result = model.predict([feature_values])[0]
        return int(result)

    return 1 if feature_values[7] < 130 or feature_values[4] > 250 else 0


@login_required
def prediction_view(request):
    error = None
    prediction_text = None

    if request.method == "POST":
        patient_identifier = request.POST.get("patient_identifier", "").strip()
        patient_name = request.POST.get("patient_name", "").strip()

        try:
            if not patient_identifier or not patient_name:
                raise ValueError

            input_values = []
            for field in FEATURE_FIELDS:
                raw_value = request.POST.get(field, "").strip()
                if field == "oldpeak":
                    input_values.append(float(raw_value))
                else:
                    input_values.append(int(raw_value))

            predicted_value = _predict_with_model(input_values)
            prediction_text = (
                "Maladie cardiaque probable" if predicted_value == 1 else "Pas de maladie cardiaque"
            )

            PatientPrediction.objects.create(
                patient_identifier=patient_identifier,
                patient_name=patient_name,
                age=input_values[0],
                sex=input_values[1],
                cp=input_values[2],
                trestbps=input_values[3],
                chol=input_values[4],
                fbs=input_values[5],
                restecg=input_values[6],
                thalach=input_values[7],
                exang=input_values[8],
                oldpeak=input_values[9],
                slope=input_values[10],
                ca=input_values[11],
                thal=input_values[12],
                prediction=prediction_text,
            )
        except (TypeError, ValueError):
            error = "Veuillez remplir correctement tous les champs patient."

    return render(
        request,
        "prediction.html",
        {
            "error": error,
            "prediction_text": prediction_text,
            "model_file_found": MODEL_PATH.exists(),
        },
    )


@login_required
def history_view(request):
    records = PatientPrediction.objects.all()
    return render(request, "history.html", {"records": records})


@login_required
def charts_view(request):
    return render(request, "charts.html")


def logout_view(request):
    logout(request)
    return redirect("login")
