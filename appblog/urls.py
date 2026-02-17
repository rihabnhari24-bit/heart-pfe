from django.urls import path

from .views import (
    account_view,
    charts_view,
    history_view,
    login_view,
    logout_view,
    prediction_view,
    register_view,
    welcome,
)

urlpatterns = [
    path("", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("welcome/", welcome, name="welcome"),
    path("account/", account_view, name="account"),
    path("prediction/", prediction_view, name="prediction"),
    path("history/", history_view, name="history"),
    path("charts/", charts_view, name="charts"),
    path("logout/", logout_view, name="logout"),
]
