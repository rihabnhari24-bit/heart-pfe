from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import PatientPrediction


class AuthenticationFlowTests(TestCase):
    def test_register_success_creates_user_and_redirects_to_login(self):
        response = self.client.post(
            reverse("register"),
            {
                "name": "Ali",
                "email": "ali@example.com",
                "password": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="ali@example.com").exists())

    def test_register_invalid_data_shows_error_message(self):
        response = self.client.post(
            reverse("register"),
            {
                "name": "",
                "email": "not-an-email",
                "password": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Les informations sont mal écrites.")
        self.assertEqual(User.objects.count(), 0)


class PredictionFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="doc@example.com",
            email="doc@example.com",
            password="StrongPass123!",
        )
        self.client.login(username="doc@example.com", password="StrongPass123!")

    def test_prediction_creates_history_row(self):
        payload = {
            "patient_identifier": "P-100",
            "patient_name": "Test Patient",
            "age": "52",
            "sex": "1",
            "cp": "0",
            "trestbps": "125",
            "chol": "212",
            "fbs": "0",
            "restecg": "1",
            "thalach": "168",
            "exang": "0",
            "oldpeak": "1",
            "slope": "2",
            "ca": "2",
            "thal": "3",
        }
        response = self.client.post(reverse("prediction"), payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PatientPrediction.objects.count(), 1)

    def test_account_password_change(self):
        response = self.client.post(
            reverse("account"),
            {"password": "NewPass123!", "password_repeat": "NewPass123!"},
        )

        self.assertRedirects(response, reverse("login"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPass123!"))
